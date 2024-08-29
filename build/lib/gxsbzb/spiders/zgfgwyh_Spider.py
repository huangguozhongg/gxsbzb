import re
from scrapy import *
from ..items import *
from ..utile.HTTPUtile import *
## 中华人民共和国国家发展和改革委员会 ##

# 发展改革委令,规范性文件，通知公告，规划文件，通知公告
class zgfgwyh_fgwg_Spider(Spider):

    # 爬虫名
    name = 'zgfgwyh_fgwg'
    # 网站标题
    __WebTitle = '中华人民共和国国家发展和改革委员会'
    # 网站地址
    __WebUrl = 'http://www.ndrc.gov.cn/'
    # 网站节点
    __WebNodes = ['政策发布中心发展改革委令',
                  '政策发布中心规范性文件',
                  '政策发布中心公告',
                  '政策发布中心规划文本',
                  '政策发布中心通知',
                  '政策发布中心政策解读']
    # 网站定位
    __Websites = __WebNodes
    # 网站节点地址
    __WebNodeUrls = [ 'http://www.ndrc.gov.cn/zcfb/zcfbl/index_%d.html',
                      'http://www.ndrc.gov.cn/zcfb/gfxwj/index_%d.html',
                      'http://www.ndrc.gov.cn/zcfb/zcfbgg/index_%d.html',
                      'http://www.ndrc.gov.cn/zcfb/zcfbghwb/index_%d.html',
                      'http://www.ndrc.gov.cn/zcfb/zcfbtz/index_%d.html',
                      'http://www.ndrc.gov.cn/zcfb/zcjd/index_%d.html']

    # 第一个Request请求
    def start_requests(self):
        return  [Request(self.__WebUrl, callback=self.parse, method='GET', meta={'cookiejar':1})]

    # 第一个Request响应
    def parse(self, response):
        # 请求队列
        for WebNode,WebNodeUrl in zip(range(len(self.__WebNodes)),self.__WebNodeUrls):
            yield Request(WebNodeUrl.replace('index_%d.html',''), callback=self.__page_parse, method='GET', meta={'cookiejar': response.meta['cookiejar'], 'WebNode': WebNode, 'page':1})

    # 页面解析
    def __page_parse(self, response):
        try:
            # 抽取所有页面
            papers = response.xpath('//ul[contains(@class,"list_02 clearfix")]/li[@class="li"]')
            # 抽取页面每一
            for paper in papers:
                # 标题
                Title = paper.xpath('.//a/text()').extract()[0]
                # url
                Url = response.urljoin(paper.xpath('./a/@href').extract()[0])
                # 日期
                Time = paper.xpath('./font[@class="date"]/text()').extract()[0]
                # 保持到Item（编号，有效性，创建时间，标题，链接，日期，模块，网址地址，网址标题，网站节点，爬取次数）
                item = gxykdx_Item(Id=str(uuid.uuid1()), IsValid=1, CreateDate='DEFAULT', Title=Title, Url=Url, Time=Time, Website=self.__Websites[response.meta['WebNode']], WebUrl=self.__WebUrl, WebTitle=self.__WebTitle, WebNode=self.__WebNodes[response.meta['WebNode']], Count=0)
                # 提交Item，判断URL是否重复
                if hasattr(self, 'mysql_config'):
                    if Url in getattr(self, 'mysql_config'):
                        raise Exception('URL重复，抛出异常！')
                yield item
        except Exception as  e:
            print(e)
        else:
            yield Request(self.__WebNodeUrls[response.meta['WebNode']] % response.meta['page'], callback=self.__page_parse,meta={'cookiejar': response.meta['cookiejar'], 'WebNode': response.meta['WebNode'], 'page': (response.meta['page'] + 1)})

