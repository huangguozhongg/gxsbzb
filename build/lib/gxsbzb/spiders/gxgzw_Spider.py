# -*- coding: utf-8 -*-
import  json
from scrapy import *
from ..items import *
from ..utile.HTTPUtile import *

## 广西壮族自治区人民政府国有资产监督管理委员会网站 ##

# 采购公告，办事指南
class gxgzw_cb_Spider(Spider):

    # 爬虫的名称
    name = 'gxgzw_cb'
    # 网站标题
    __WebTitle = '广西壮族自治区人民政府国有资产监督管理委员会网站'
    # 网站地址
    __WebUrl = 'http://gzw.gxzf.gov.cn/'
    # 网站节点
    __WebNodes = ['信息公开政府采购公告',
                  '信息公开办事指南'
                  ]
    # 网站定位
    __Websites = __WebNodes
    # 网站节点地址
    __WebNodeUrls = ['http://gzw.gxzf.gov.cn/html/xinxigongkai/guapaixiangmu/%s.html',
                     'http://gzw.gxzf.gov.cn/html/xinxigongkai/bszn/%s.html',
                    ]

    # 第一个Rqeust请求
    def start_requests(self):
        return  [Request(self.__WebUrl, callback=self.parse, method='GET', meta={'cookiejar':1})]

    # 第一个Response响应
    def parse(self, response):
        # 请求队列
        for WebNode,WebNodeUrl in zip(range(len(self.__WebNodes)),self.__WebNodeUrls):
            yield Request(WebNodeUrl % 'index', callback=self.__page_parse, method='GET', meta={'cookiejar': response.meta['cookiejar'], 'WebNode': WebNode, 'page':1})

    # 页面解析
    def __page_parse(self,response):
        try:
            # 首先抽取所有的文章
            papers = response.xpath('//div[@class="newslist3 font14"]/ul/li')
            # 从每篇文章中抽取数据
            for paper in papers:
                # 标题
                Title = paper.xpath('.//a/@title').extract()[0].strip()
                # url
                Url = response.urljoin(paper.xpath('.//a/@href').extract()[0].strip())
                # 日期
                Time = paper.xpath('./font/text()').extract()[0].replace('.','-').strip()
                # 保持到Item（编号，有效性，创建时间，标题，链接，日期，模块，网址地址，网址标题，网站节点，爬取次数）
                item = gxykdx_Item(Id=str(uuid.uuid1()), IsValid=1, CreateDate='DEFAULT', Title=Title, Url=Url, Time=Time, Website=self.__Websites[response.meta['WebNode']], WebUrl=self.__WebUrl, WebTitle=self.__WebTitle, WebNode=self.__WebNodes[response.meta['WebNode']], Count=0)
                # 提交Item，判断URL是否重复
                if hasattr(self, 'mysql_config'):
                    if Url in getattr(self, 'mysql_config'):
                        raise Exception('URL重复，抛出异常！')
                yield item
        except Exception as e:
            print(e)
        else:
            yield Request(self.__WebNodeUrls[response.meta['WebNode']] % (response.meta['page'] +1), callback=self.__page_parse,  method='GET', meta={'WebNode': response.meta['WebNode'], 'page': (response.meta['page'] +1)})
