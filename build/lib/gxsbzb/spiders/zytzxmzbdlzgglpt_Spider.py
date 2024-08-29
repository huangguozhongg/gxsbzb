# -*- coding: utf-8 -*-
import  json
from scrapy import *
from ..items import *
from ..utile.HTTPUtile import *

## 中央投资项目招标代理资格管理平台 ##

# 最新发布，政策法规
class zytzxmzbdlzgglpt_zc_Spider(Spider):

    # 爬虫名
    name = 'zytzxmzbdlzgglpt_zc'
    # 网站标题
    __WebTitle = '中央投资项目招标代理资格管理平台'
    # 网站地址
    __WebUrl = 'http://www.ctba.org.cn/zt/zgglpt/index.jsp.htm'
    # 网站节点
    __WebNodes = ['最新发布',
                  '政策法规'
                  ]
    # 网站定位
    __Websites = __WebNodes
    # 网站节点地址
    __WebNodeUrls = ['http://www.ctba.org.cn/zt/zgglpt/list.jsp-offset=%d&&tb2=ZXFB&defaultClickValue=.htm',
                     'http://www.ctba.org.cn/zt/zgglpt/list.jsp-offset=%d&&tb2=ZCFG&defaultClickValue=.htm'
                     ]

    # 第一个Rqeust请求
    def start_requests(self):
        return [Request(url= self.__WebUrl, callback=self.parse, method='GET',meta={'cookiejar':1})]


    def parse(self, response):
        # 请求队列
        for WebNode,WebNodeUrl in zip(range(len(self.__WebNodes)),self.__WebNodeUrls):
            yield Request(WebNodeUrl % 0, callback=self.__page_parse, method='GET', meta={'cookiejar': response.meta['cookiejar'], 'WebNode': WebNode, 'page':1})

    # 第一个Response响应
    def __page_parse(self, response):
        try:
            # 首先抽取所有的文章
            papers = response.xpath('//table//tr')
            # 从每篇文章中抽取数据
            for paper in papers:
                # 标题
                Title = paper.xpath('.//td/li//a/@title').extract()[0].strip()
                # url
                Url = response.urljoin(paper.xpath('.//td/li//a/@href').extract()[0].strip())
                # 日期
                Time = paper.xpath('.//td/li/h2[@class="t_center left"]/text()').extract()[0].strip()
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
            yield Request(url= self.__WebNodeUrls[response.meta['WebNode']] % (response.meta['page'] * 15), callback=self.__page_parse, method='GET', meta={'cookiejar': response.meta['cookiejar'], 'WebNode': response.meta['WebNode'], 'page':(response.meta['page'] + 1)})