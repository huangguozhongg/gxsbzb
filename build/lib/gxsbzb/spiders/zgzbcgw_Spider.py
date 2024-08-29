import re
from scrapy import *
from ..items import *
from ..utile.HTTPUtile import *

## 中国招标采购网 ##

# 招标信息，招标预告，采购信息
class zgzbcgw_zzc_Spider(Spider):

    # 爬虫名
    name = 'zgzbcgw_zzc'
    # 网站标题
    __WebTitle = '中国招标采购网'
    # 网站地址
    __WebUrl = 'https://www.chinabidding.cn/'
    # # 网站节点
    __WebNodes = {'招标公告':'招标信息招标公告','中标公告':'招标信息中标公告','中标预告':'招标信息中标预告','政府采购':'采购信息政府采购','企业采购':'采购信息企业采购'}
    # 网站定位
    __Websites = __WebNodes
    # 网站节点地址
    __WebNodeUrls = [ 'https://www.chinabidding.cn/search/searchzbw/search2?areaid=21&keywords=&page=%d&categoryid=&rp=22&table_type=1000&b_date=',
                      'https://www.chinabidding.cn/search/searchzbw/search2?areaid=21&keywords=&page=%d&categoryid=&rp=22&table_type=1030&b_date=',
                      'https://www.chinabidding.cn/search/searchzbw/search2?areaid=21&keywords=&page=%d&categoryid=&rp=22&table_type=2000&b_date=']

    # 第一个Request请求
    def start_requests(self):
        return  [Request(self.__WebUrl, callback=self.parse, method='GET', meta={'cookiejar':1})]

    # 第一个Request响应
    def parse(self, response):
        # 请求队列
        for WebNodeUrl in self.__WebNodeUrls:
            yield Request(WebNodeUrl % 1, callback=self.__page_parse, method='GET', meta={'cookiejar': response.meta['cookiejar'], 'page':1})


    # 页面解析
    def __page_parse(self, response):
        try:
            # 抽取所有页面
            papers = response.xpath('//table[@class="table_body"]//tr[@class="listrow1"]')
            # 抽取页面每一
            for paper in papers:
                # 标题
                Title = paper.xpath('./td[2]/a/text()').extract()[0]
                # url
                Url = response.urljoin(paper.xpath('./td[2]/a/@href').extract()[0])
                # 日期
                Time = paper.xpath('./td[last()]/text()').extract()[0]
                # 网站节点
                WebNode = paper.xpath('./td[4]/text()').extract()[0]
                # 保持到Item（编号，有效性，创建时间，标题，链接，日期，模块，网址地址，网址标题，网站节点，爬取次数）
                item = gxykdx_Item(Id=str(uuid.uuid1()), IsValid=1, CreateDate='DEFAULT', Title=Title, Url=Url, Time=Time, Website=self.__Websites[WebNode], WebUrl=self.__WebUrl, WebTitle=self.__WebTitle, WebNode=self.__WebNodes[WebNode], Count=0)
                # 提交Item，判断URL是否重复
                if hasattr(self, 'mysql_config'):
                    if Url in getattr(self, 'mysql_config'):
                        raise Exception('URL重复，抛出异常！')
                yield item
        except Exception as  e:
            print(e)
        else:
            yield Request(response.urljoin(response.xpath('//a[contains(text(),"后一页")]/@href').extract()[0]), callback=self.__page_parse, meta={'cookiejar': response.meta['cookiejar']})

