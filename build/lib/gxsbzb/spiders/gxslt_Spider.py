# -*- coding: utf-8 -*-
import  json
from scrapy import *
from ..items import *
from ..utile.HTTPUtile import *

## 广西壮族自治区水利厅网站 ##

# 通知公告
class gxslt_tzgg_Spider(Spider):

    # 爬虫名
    name = 'gxslt_tzgg'
    # 网站标题
    __WebTitle = '广西壮族自治区水利厅网站'
    # 网站地址
    __WebUrl = 'http://slt.gxzf.gov.cn/index.html'
    # 网站节点
    __WebNodes = ['动态信息通知公告公示']
    # 网站定位
    __Websites = __WebNodes
    # 网站节点地址
    __WebNodeUrls = ['http://slt.gxzf.gov.cn/dtxx/tzgg3/index_%s.html']

    # 第一个Rqeust请求
    def start_requests(self):
        return [Request(url=self.__WebNodeUrls[0].replace('_%s','') , callback=self.parse, method='GET',meta={'cookiejar':1, 'page':1})]

    # 第一个Response响应
    def parse(self, response):
        try:
            # 首先抽取所有的文章
            papers = response.xpath('//ul[@class="list_c"]/li')
            # 从每篇文章中抽取数据
            for paper in papers:
                # 标题
                Title = paper.xpath('.//a/text()').extract()[0].strip()
                # url
                Url = response.urljoin(paper.xpath('.//a/@href').extract()[0].strip())
                # 日期
                Time = re.search('(\d{4})-(\d{2})-(\d{2})(\s*?)(\d{2}):(\d{2})',paper.xpath('.//span/text()').extract()[0]).group(0)
                # 保持到Item（编号，有效性，创建时间，标题，链接，日期，模块，网址地址，网址标题，网站节点，爬取次数）
                item = gxykdx_Item(Id=str(uuid.uuid1()), IsValid=1, CreateDate='DEFAULT', Title=Title, Url=Url, Time=Time, Website=self.__Websites[0], WebUrl=self.__WebUrl, WebTitle=self.__WebTitle, WebNode=self.__WebNodes[0], Count=0)
                # 提交Item，判断URL是否重复
                if hasattr(self, 'mysql_config'):
                    if Url in getattr(self, 'mysql_config'):
                        raise Exception('URL重复，抛出异常！')
                yield item
        except Exception as e:
            print(e)
        else:
            # 跟进请求
            yield Request(self.__WebNodeUrls[0] % (response.meta['page'] + 1), callback=self.parse, method='GET',meta={'cookiejar': response.meta['cookiejar'], 'page':(response.meta['page'] +1)})
