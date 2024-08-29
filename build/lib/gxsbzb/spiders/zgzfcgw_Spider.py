# -*- coding: utf-8 -*-
from scrapy import *
from ..items import *
from ..utile.HTTPUtile import *
import re, json
from datetime import *

## 中国政府采购网 ##

# 政策法规
class zgzfcgw_zcfg_Spider(Spider):

    # 爬虫名
    name = 'zgzfcgw_zcfg'
    # 网站标题
    __WebTitle = '中国政府采购网'
    # 网站地址
    __WebUrl = 'http://www.ccgp.gov.cn/'
    # 网站节点
    __WebNodes = ['政采法规国务院文件',
                  '政采法规财政部规章',
                  '政采法规财政部规范性文件',
                  '政采法规其他部委文件',
                  '政采法规政策解读',
                  '政采法规地方规章办法',
                  '政采法规相关法规',
                  '政采法规国际法规'
                  ]
    # 网站定位
    __Websites = __WebNodes
    # 网站节点地址
    __WebNodeUrls = [ 'http://www.ccgp.gov.cn/zcfg/gwywj/index_%d.htm',
                    'http://www.ccgp.gov.cn/zcfg/mofgz/index_%d.htm',
                    'http://www.ccgp.gov.cn/zcfg/mof/index_%d.htm',
                    'http://www.ccgp.gov.cn/zcfg/bwfile/index_%d.htm',
                    'http://www.ccgp.gov.cn/zcfg/zcjd/index_%d.htm',
                    'http://www.ccgp.gov.cn/zcfg/dffg/index_%d.htm',
                    'http://www.ccgp.gov.cn/zcfg/gjfg/index_%d.htm',
                    'http://www.ccgp.gov.cn/zcfg/guojifg/index_%d.htm']

    # 第一个Request请求
    def start_requests(self):
        return [Request(self.__WebUrl, callback=self.parse, meta={'cookiejar':1})]

    ## 第一个Response响应
    def parse(self, response):
        # 请求队列
        for WebNode,WebNodeUrl in zip(range(len(self.__WebNodes)),self.__WebNodeUrls):
            yield Request(WebNodeUrl.replace('_%d',''), callback=self.__page_parse, method='GET', meta={'cookiejar': response.meta['cookiejar'], 'WebNode': WebNode, 'page':1})

    ## 页面解析
    def __page_parse(self,response):
        try:
            # 首先抽取所有的文章
            papers = response.xpath('//div[@class="vF_detail_relcontent_lst"]//ul//li')
            # 从每篇文章中抽取数据
            for paper in papers:
                # 标题
                Title = paper.xpath('./a/@title').extract()[0]
                # url
                Url = response.urljoin(paper.xpath('./a/@href').extract()[0])
                # 日期
                Time = paper.xpath('./span[1]/text()').extract()[0]
                if not Time:
                    Time = paper.xpath('./td[last()]/text()').extract()[0]
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
            yield Request(url=self.__WebNodeUrls[response.meta['WebNode'] ]  % response.meta['page'], callback=self.parse, method='GET',meta={'cookiejar': response.meta['cookiejar'], 'WebNode': response.meta['WebNode'], 'page': (response.meta['page'] + 1)})


# 采购公告
class zgzfcgw_cggg_Spider(Spider):

    # 爬虫名
    name = 'zgzfcgw_cggg'
    # 网站标题
    __WebTitle = '广西南宁市公共资源交易中心'
    # 网站地址
    __WebUrl = 'http://www.ccgp.gov.cn'
    # 网站节点
    __WebNodes = ['采购公告公开招标',
                  '采购公告询价公告',
                  '采购公告竞争性谈判',
                  '采购公告单一来源',
                  '采购公告资格预审',
                  '采购公告邀请公告',
                  '采购公告中标公告',
                  '采购公告更正公告',
                  '采购公告其它公告',
                  '采购公告竞争性磋商',
                  '采购公告成交公告',
                  '采购公告废标流标']
    # 网站定位
    __Websites = __WebNodes
    # 网站节点参数
    __WebNodeParams = [1,2,3,4,5,6,7,8,9,10,11,12]

    # 第一个Request请求
    def start_requests(self):
        return [Request(self.__WebUrl, callback=self.parse, meta={'cookiejar':1})]

    # 第一个Response响应
    def parse(self, response):
        # 请求队列
        for WebNode in range(len(self.__WebNodes)):
            yield self.__get_Request(WebNode=WebNode, page=1, meta={'cookiejar': response.meta['cookiejar'], 'WebNode':WebNode, 'page': 1})


    ## 构造Request
    def __get_Request(self, WebNode, page, meta):
        formdata ={'searchtype': '1',
                    'page_index': '%d' % page,
                    'bidSort': '0',
                    'buyerName': '',
                    'projectId': '',
                    'pinMu': '',
                    'bidType': '%d' %  self.__WebNodeParams[WebNode],
                    'dbselect': 'bidx',
                    'kw': '',
                    'start_time': '%s' % (datetime.today() - timedelta(days=3)).strftime('%Y:%m:%d'),
                    'end_time': '%s' % datetime.today().strftime('%Y:%m:%d'),
                    'timeType': '1',
                    'displayZone': '广西省',
                    'zoneId': '45',
                    'pppStatus': '0',
                    'agentName': ''
                    }
        return  FormRequest(url='http://search.ccgp.gov.cn/bxsearch',callback=self.__page_parse, formdata=formdata,method='GET', meta=meta)

    ## 页面解析
    def __page_parse(self,response):
        try:
            # 首先抽取所有的文章
            papers = response.xpath('//ul[@class="vT-srch-result-list-bid"]//li')
            # 从每篇文章中抽取数据
            for paper in papers:
                # 标题
                Title = paper.xpath('./a/text()').extract()[0]
                # url
                Url = response.urljoin(paper.xpath('./a/@href').extract()[0])
                # 日期
                Time = re.search('\d{4}\.\d{2}\.\d{2}\s*\d{2}:\d{2}:\d{2}',paper.xpath('./span/text()').extract()[0]).group(0)
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
            yield self.__get_Request(response.meta['WebNode'], page=(response.meta['page'] + 1),meta={'cookiejar': response.meta['cookiejar'], 'WebNode':response.meta['WebNode'], 'page': (response.meta['page']+1)})
