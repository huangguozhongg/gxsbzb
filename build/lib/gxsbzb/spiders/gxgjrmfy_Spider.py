import re
from scrapy import *
from ..items import *
from ..utile.HTTPUtile import *
## 广西壮族自治区高级人民法院 ##

# 通知公告
class gxgjrmfy_tzgg_Spider(Spider):

    name = 'gxgjrmfy_tzgg'   # 爬虫名
    # 网站标题
    __WebTitle = '广西壮族自治区高级人民法院'
    # 网站地址
    __WebUrl = 'http://www.gxcourt.gov.cn/fygk.htm'
    # 网站节点
    __WebNodes = ['公告公告栏']
    # 模块
    __Websites = __WebNodes
    # 网站节点地址
    __WebNodeUrls = ['http://www.gxcourt.gov.cn/gg.htm']

    # 第一个Request请求
    def start_requests(self):
        return  [Request(self.__WebNodeUrls[0], callback=self.parse, method='GET', meta={'cookiejar':1})]

    # 第一个Request响应
    def parse(self, response):
        try:
            # 抽取所有页面
            papers = response.xpath('//tr[starts-with(@id,"lineu")]')
            # 抽取页面每一
            for paper in papers:
                # 标题
                Title = paper.xpath('.//a/text()').extract()[0].strip()
                # url
                Url = response.urljoin(paper.xpath('.//a/@href').extract()[0].strip())
                # 日期
                Time = paper.xpath('.//td[@class="newstime news_line"]/text()').extract()[0]
                # 保持到Item（编号，有效性，创建时间，标题，链接，日期，模块，网址地址，网址标题，网站节点，爬取次数）
                item = gxykdx_Item(Id=str(uuid.uuid1()), IsValid=1, CreateDate='DEFAULT', Title=Title, Url=Url, Time=Time, Website=self.__Websites[0], WebUrl=self.__WebUrl, WebTitle=self.__WebTitle, WebNode=self.__WebNodes[0], Count=0)
                # 提交Item，判断URL是否重复
                if hasattr(self, 'mysql_config'):
                    if Url in getattr(self, 'mysql_config'):
                        raise Exception('URL重复，抛出异常！')
                yield item
        except Exception as  e:
            print(e)
        else:
            yield Request(response.urljoin(response.xpath('.//a[contains(text(),"下页")]/@href').extract()[0]), callback=self.parse, meta={'cookiejar': response.meta['cookiejar']})
