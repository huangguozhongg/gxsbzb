from scrapy import *
from ..items import *
from ..utile.HTTPUtile import *

## 广西政协网 ##

# 广西政协动态,政协会议,通知公告
class gxzx_tht_Spider(Spider):

    # 爬虫名
    name = 'gxzx_tht'
    # 网站标题
    __WebTitle = '广西政协网'
    # 网站地址
    __WebUrl = 'http://www.gxzx.gov.cn/index.html'
    # 网站节点
    __WebNodes = ['广西政协动态',
                  '政协会议',
                  '通知公告']
    # 网站定位
    __Websites = __WebNodes
    # 网站节点地址
    __WebNodeUrls = ['http://www.gxzx.gov.cn/index.php?m=content&c=index&a=lists&catid=14&page=%d',
                     'http://www.gxzx.gov.cn/index.php?m=content&c=index&a=lists&catid=86&page=%d',
                     'http://www.gxzx.gov.cn/index.php?m=content&c=index&a=lists&catid=39&page=%d']

    # 第一个Request请求
    def start_requests(self):
        return  [Request(self.__WebUrl, callback=self.parse, method='GET', meta={'cookiejar':1})]

    # 第一个Request响应
    def parse(self, response):
        # 请求队列
        # 请求队列
        for WebNode,WebNodeUrl in zip(range(len(self.__WebNodes)),self.__WebNodeUrls):
            yield Request(WebNodeUrl.replace('&page=%d',''), callback=self.__page_parse, method='GET', meta={'cookiejar': response.meta['cookiejar'], 'WebNode': WebNode, 'page':1})

    # 页面解析
    def __page_parse(self, response):
        try:
            # 抽取所有页面
            papers = response.xpath('//ul[@class="list_ul"]/li')
            # 抽取页面每一
            for paper in papers:
                # 标题
                Title = paper.xpath('./a/text()').extract()[0].strip()
                # url
                Url = response.urljoin(paper.xpath('./a/@href').extract()[0])
                # 日期
                Time = paper.xpath('./span/text()').extract()[0]
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
            yield  Request(self.__WebNodeUrls[response.meta['WebNode']] % (response.meta['page'] + 1), callback=self.__page_parse, method='GET', meta={'cookiejar': response.meta['cookiejar'], 'WebNode': response.meta['WebNode'],'page': (response.meta['page'] + 1)})

