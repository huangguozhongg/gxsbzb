from scrapy import *
from ..items import *
from ..utile.HTTPUtile import *

# 广西贵港市公共资源 #

# 通知公告，政策法规，交易信息
class ggsggzy_tzj_Spider(Spider):

    # 爬虫名
    name = 'ggsggzy_tzj'
    # 网站标题
    __WebTitle = '广西贵港市公共资源'
    # 网站地址
    __WebUrl = 'http://ggggjy.gxgg.gov.cn:9005/'
    # 网站节点
    __WebNodes = [
                  '通知公告',

                  '政策法规贵港市',
                  '政策法规桂平市',
                  '政策法规平南县',

                  '交易信息贵港市房建市政招标公告',
                  '交易信息贵港市水利交通招标公告',
                  '交易信息贵港市政府采购招标公告',

                  '交易信息桂平市房建市政招标公告',
                  '交易信息桂平市水利交通招标公告',
                  '交易信息桂平市政府采购招标公告',

                  '交易信息平南县房建市政招标公告'
                  '交易信息平南县水利交通招标公告',
                  '交易信息平南县政府采购招标公告'
                  ]
    # 网站定位
    __Websites = __WebNodes
    # 网站节点地址
    __WebNodeUrls = [
                       'http://ggggjy.gxgg.gov.cn:9005/zxdt/{:s}.html',

                       'http://ggggjy.gxgg.gov.cn:9005/zcfg/006001/{:s}.html',
                       'http://ggggjy.gxgg.gov.cn:9005/zcfg/006002/{:s}.html',
                       'http://ggggjy.gxgg.gov.cn:9005/zcfg/006003/{:s}.html',

                       'http://ggggjy.gxgg.gov.cn:9005/zbxx/002001/002001001/002001001001/{:s}.html',
                       'http://ggggjy.gxgg.gov.cn:9005/zbxx/002001/002001002/002001002001/{:s}.html',
                       'http://ggggjy.gxgg.gov.cn:9005/zbxx/002001/002001003/002001003001/{:s}.html',

                       'http://ggggjy.gxgg.gov.cn:9005/zbxx/002002/002002001/002002001001/{:s}.html',
                       'http://ggggjy.gxgg.gov.cn:9005/zbxx/002002/002002002/002002002001/{:s}.html',
                       'http://ggggjy.gxgg.gov.cn:9005/zbxx/002002/002002003/002002003001/{:s}.html',

                       'http://ggggjy.gxgg.gov.cn:9005/zbxx/002003/002003001/002003001001/{:s}.html',
                       'http://ggggjy.gxgg.gov.cn:9005/zbxx/002003/002003002/002003002001/{:s}.html',
                       'http://ggggjy.gxgg.gov.cn:9005/zbxx/002003/002003003/002003003001/{:s}.html'
                    ]

    # 第一个Request请求
    def start_requests(self):
        return  [Request(self.__WebUrl, callback=self.parse, method='GET', meta={'cookiejar':1})]

    # 第一个响应
    def parse(self, response):
        # 请求队列
        for WebNode,WebNodeUrl in zip(range(len(self.__WebNodes)),self.__WebNodeUrls):
            yield Request(WebNodeUrl.format('about'), callback=self.__page_parse, method='GET', meta={'cookiejar': response.meta['cookiejar'], 'WebNode': WebNode, 'page':1})

    # 页面解析
    def __page_parse(self, response):
        try:
            # 抽取所有页面
            papers = response.xpath('//ul[@class="wb-data-item"]/li')
            # 抽取页面每一
            for paper in papers:
                # 标题
                Title = paper.xpath('.//a/@title').extract()[0]
                # url
                Url = response.urljoin(paper.xpath('.//a/@href').extract()[0])
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
            # 跟进请求
            yield Request(self.__WebNodeUrls[response.meta['WebNode']].format(str(response.meta['page'] + 1)), callback=self.__page_parse, method='GET',meta={'cookiejar': response.meta['cookiejar'], 'WebNode': response.meta['WebNode'], 'page':(response.meta['page'] +1)})
