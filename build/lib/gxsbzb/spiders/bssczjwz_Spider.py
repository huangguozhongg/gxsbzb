from scrapy import *
from ..items import *
from ..utile.HTTPUtile import *

# 广西百色市财政局网站 #

# 通知公告
class bssczjwz_tzgg_Spider(Spider):

    # 爬虫名
    name = 'bssczjwz_tzgg'
    # 网站标题
    __WebTitle = '广西百色市财政局网站'
    # 网站地址
    __WebUrl = 'http://czj.baise.gov.cn/'
    # 网站节点
    __WebNodes = ['工作动态通知公告']
    # 网站定位
    __Websites = __WebNodes
    # 网站节点地址
    __WebNodeUrls = [ 'http://czj.baise.gov.cn/list-26-%d.html']

    # 第一个Request请求
    def start_requests(self):
        return  [Request(self.__WebNodeUrls[0] % 1, callback=self.parse, method='GET', meta={'cookiejar':1, 'page':1})]

    # 第一个响应
    def parse(self, response):
        # 页面解析
        try:
            # 抽取所有页面
            papers = response.xpath('//ul[@class="label_ul_b new_li6"]/li[not(@class)]')
            # 抽取页面每一
            for paper in papers:
                # 标题
                Title = paper.xpath('./a/text()').extract()[0]
                # url
                Url = response.urljoin(paper.xpath('./a/@href').extract()[0])
                # 日期
                Time = paper.xpath('./span/text()').extract()[0][1:-1]
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
            # 跟进Request
            yield Request(self.__WebNodeUrls[0] % (response.meta['page'] + 1), callback=self.parse, meta={'cookiejar': response.meta['cookiejar'], 'page':(response.meta['page'] +1)})

