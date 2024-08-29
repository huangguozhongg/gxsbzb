# -*- coding: utf-8 -*-
from scrapy import Spider, Item, Request, FormRequest
from scrapy.exceptions import IgnoreRequest
from ..items import gxykdx_Item
from ..utile.HTTPUtile import *
from datetime import datetime, timedelta
import re, json

## 中国国际招标网 ##

# 政策服务,行业资讯
class zggjzbw_zh_Spider(Spider):

    # 爬虫名
    name = 'zggjzbw_zh'
    # 网站标题
    __WebTitle = '中国国际招标网'
    # 网站地址
    __WebUrl = 'http://chinabidding.mofcom.gov.cn/'
    # 网站节点
    __WebNodes = ['政务服务通知公告',
                  '政务服务政策法规',
                  '政务服务政策解读',
                  '政务服务地方动态',
                  '行业资讯行业聚焦',
                  '行业资讯新闻资讯',
                  '行业资讯专家观点',
                  '行业资讯案例分析'
                  ]
    # 网站定位
    __Websites = __WebNodes
    # 网站节点参数
    __WebNodeParam = [83, 86, 87, 85, 63, 66, 89, 90]

    # 第一个请求
    def start_requests(self):
        return  [Request(self.__WebUrl,callback=self.parse,meta={'cookiejar':1})]

    # 构造Request
    def __get_request(self,WebNode, page, meta):
        formdata = {
            'column': '%d' % self.__WebNodeParam[WebNode],
            's':'',
            'p': '%d' % page,
            'timeType': '',
            'ps': 'zx',
        }
        return  FormRequest(url='http://chinabidding.mofcom.gov.cn/channel/column/articleSearch.shtml',
                            callback=self.__page_parse,
                            formdata=formdata,
                            method='GET',
                            meta=meta)

    ## 第一个Response响应
    def parse(self, response):
        # 请求队列
        for WebNode in range(len(self.__WebNodes)):
            yield self.__get_request(WebNode=WebNode, page=1,meta={'cookiejar': response.meta['cookiejar'], 'WebNode':WebNode, 'page':1})

    ## 页面解析
    def __page_parse(self,response):
        try:
            # 首先抽取所有的文章
            papers = response.xpath('//ul[@class="menu_list"]/li')
            # 从每篇文章中抽取数据
            for paper in papers:
                # 标题
                Title = paper.xpath('./div[@class="tit_04 mt20 pp"]/a/text()').extract()[0]
                # url
                Url = response.urljoin(paper.xpath('./div[@class="tit_04 mt20 pp"]/a/@href').extract()[0])
                # 日期
                Time = paper.xpath('.//span[@class="time01"]/text()').extract()[0].strip()[-10:]
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
            # 提交Request跟进
            yield self.__get_request(WebNode=response.meta['WebNode'], page=(response.meta['page'] + 1), meta={'cookiejar': response.meta['cookiejar'], 'WebNode':response.meta['WebNode'], 'page':(response.meta['page']+1)})


# 业务信息
class zggjzbw_ywxx_Spider(Spider):

    # 爬虫名
    name = 'zggjzbw_ywxx'
    # 网站标题
    __WebTitle = '中国国际招标网'
    # 网站地址
    __WebUrl = 'http://chinabidding.mofcom.gov.cn/'
    # 网站节点
    __WebNodes = ['业务信息招标公告',
                  '业务信息招标变更公告',
                  '业务信息评标结果公示',
                  '业务信息中标结果公告']
    # 网站定位
    __Websites = __WebNodes
    # 网站节点参数
    __WebNodeParam = [1,2,3,4]

    # 第一个请求
    def start_requests(self):
        return [Request("http://chinabidding.mofcom.gov.cn/channel/business/bulletinList.shtml?type=0",callback=self.parse, meta={'cookiejar':1})]

    # 构造Request
    def __post_request(self, WebNode, page, meta):
        formdata = {
            'pageNumber':'%d' % page,
            'keyWord':'',
            'timeType': '2',
            'rangeCode': '',
            'typeCode': '%d' % self.__WebNodeParam[WebNode],
            'capitalSourceCode':'',
            'industryCode':'',
            'provinceCode': '450000'
        }
        return  Request(url='http://chinabidding.mofcom.gov.cn/zbwcms/front/bidding/bulletinInfoList',
                        callback=self.__page_parse,
                        body=json.dumps(formdata),
                        method='POST',
                        meta= meta)

    ## 第一个Response响应
    def parse(self, response):
        # 请求队列
        for WebNode in range(len(self.__WebNodes)):
            yield  self.__post_request(WebNode=WebNode,page=1,meta={'cookiejar':response.meta['cookiejar'],'WebNode': WebNode, 'page': 1})


    ## 页面解析
    def __page_parse(self,response):
        try:
            # 首先抽取所有的文章
            papers = json.loads(response.text, encoding='utf-8')["rows"]
            # 从每篇文章中抽取数据
            for paper in papers:
                # 标题
                Title = paper["name"]
                # url
                Url = response.urljoin(paper["filePath"])
                # 日期
                Time = paper["createTime"]
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
            # 提交Request跟进
            yield self.__post_request(response.meta['WebNode'],(response.meta['page'] + 1),meta={'cookiejar':response.meta['cookiejar'], 'WebNode':response.meta['WebNode'], 'page': response.meta['cookiejar']})

