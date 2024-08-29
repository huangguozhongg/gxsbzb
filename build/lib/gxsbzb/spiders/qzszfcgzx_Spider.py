from scrapy import *
from ..items import *
from ..utile.HTTPUtile import *

# 广西钦州市政府采购中心 #

# 采购信息，工作动态，公告通知，政策法规
class qzszfcgzx_cgtz_Spider(Spider):

    # 爬虫名
    name = 'qzszfcgzx_cgtz'
    # 网站标题
    __WebTitle = '广西钦州市政府采购中心'
    # 网站地址
    __WebUrl = 'http://www.qzzfcg.cn/'
    # 网站节点
    __WebNodes = [
                  '采购信息采购公告',

                  '工作动态政采新闻',
                  # '工作动态>采购动态',

                  '公告通知通知公告',
                  '公告通知信息公开',

                  '政策法规国家',
                  '政策法规广西',
                  '政策法规钦州'
                  ]
    # 网站定位
    __Websites = __WebNodes
    # 网站节点地址
    __WebNodeUrls = [
                       'http://www.qzzfcg.cn/xl/?l=%E9%87%87%E8%B4%AD%E4%BF%A1%E6%81%AF%2C%E9%87%87%E8%B4%AD%E5%85%AC%E5%91%8A&page={}',

                       'http://www.qzzfcg.cn/xl/?l=%E5%B7%A5%E4%BD%9C%E5%8A%A8%E6%80%81%2C%E6%94%BF%E9%87%87%E6%96%B0%E9%97%BB&page={}',
                       # 'http://www.qzzfcg.cn/xl/?l=%E5%B7%A5%E4%BD%9C%E5%8A%A8%E6%80%81%2C%E9%87%87%E8%B4%AD%E5%8A%A8%E6%80%81&page=%d',

                       'http://www.qzzfcg.cn/xl/?l=%E5%85%AC%E5%91%8A%E9%80%9A%E7%9F%A5%2C%E9%80%9A%E7%9F%A5%E5%85%AC%E5%91%8A&page={}',
                       'http://www.qzzfcg.cn/xl/?l=%E5%85%AC%E5%91%8A%E9%80%9A%E7%9F%A5%2C%E4%BF%A1%E6%81%AF%E5%85%AC%E5%BC%80&page={}',

                       'http://www.qzzfcg.cn/xl/?l=%E6%94%BF%E7%AD%96%E6%B3%95%E8%A7%84%2C%E5%9B%BD%E5%AE%B6&&page={}',
                       'http://www.qzzfcg.cn/xl/?l=%E6%94%BF%E7%AD%96%E6%B3%95%E8%A7%84%2C%E5%B9%BF%E8%A5%BF&&page={}',
                       'http://www.qzzfcg.cn/xl/?l=%E6%94%BF%E7%AD%96%E6%B3%95%E8%A7%84%2C%E9%92%A6%E5%B7%9E&page={}'
                    ]

    # 第一个Request请求
    def start_requests(self):
        return  [Request(self.__WebUrl, callback=self.parse, method='GET', meta={'cookiejar':1})]

    # 第一个Response响应
    def parse(self, response):
        # 请求队列
        for WebNode,WebNodeUrl in zip(range(len(self.__WebNodes)),self.__WebNodeUrls):
            yield Request(WebNodeUrl.format(1), callback=self.__page_parse, method='GET', meta={'cookiejar': response.meta['cookiejar'], 'WebNode': WebNode, 'page':1})

    # 页面解析
    def __page_parse(self, response):
        try:
            # 抽取所有页面
            papers = response.xpath('//li[@class="xx"]/ol[@class="list"]')
            # 抽取页面每一
            for paper in papers:
                # 标题
                Title = paper.xpath('.//a/text()').extract()[0]
                # url
                Url = response.urljoin(paper.xpath('.//a/@href').extract()[0])
                # 日期
                Time = paper.xpath('./li[@class="xd"]/text()').extract()[0][1:-1]
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
            # 跟进请求
            yield Request(self.__WebNodeUrls[response.meta['WebNode']].format(response.meta['page'] + 1), callback=self.__page_parse, meta={'cookiejar': response.meta['cookiejar'], 'WebNode':response.meta['WebNode'], 'page':(response.meta['page'] +1)})
