from scrapy import *
from ..items import *
from ..utile.HTTPUtile import *
import requests

# 广西百色市住房和城乡建设局 #

# 工作动态，通知文件
class bsszcxj_gt_Spider(Spider):

    # 爬虫名
    name = 'bsszcxj_gt'
    # 网站标题
    __WebTitle = '广西百色市住房和城乡建设局'
    # 网站地址
    __WebUrl = 'http://zjw.baise.gov.cn/'
    # 网站节点
    __WebNodes = ['政务公开工作动态',
                  '政务公开通知文件'
                  ]
    # 网站定位
    __Websites = __WebNodes
    # 网站节点地址
    __WebNodeUrls = [  'http://zjw.baise.gov.cn/list-19-%s.html',
                       'http://zjw.baise.gov.cn/list-16-%s.html'
                    ]

    __cookies = {'security_session_mid_verify':'764921e7eec461834328141491879c80',
                'srcurl':'687474703a2f2f7a6a772e62616973652e676f762e636e2f6c6973742d31362d322e68746d6c',
                'yunsuo_session_verify':'c870e71cb9514650aefc0748fc869a32'}

    # 第一个Request请求
    def start_requests(self):
        ses = requests.Session()
        ses.get('http://zjw.baise.gov.cn/list-16-1.html')
        ses.get('http://zjw.baise.gov.cn/list-16-1.html?security_verify_data=313533362c383634')
        ses.get('http://zjw.baise.gov.cn/list-16-1.html')
        cookie = Cookieler(ses).get_cookie()
        cookie.update({'srcurl':'687474703a2f2f7a6a772e62616973652e676f762e636e2f6c6973742d31362d322e68746d6c'})

        return  [Request(self.__WebUrl, callback=self.parse, method='GET', meta={'cookie':cookie})]

    # 第一个响应
    def parse(self, response):
        # 请求队列
        for WebNode,WebNodeUrl in zip(range(len(self.__WebNodes)),self.__WebNodeUrls):
            yield Request(WebNodeUrl % 1, callback=self.__page_parse, cookies= response.meta['cookie'], method='GET', meta={'cookie': response.meta['cookie'], 'WebNode': WebNode, 'page': 1} )


    # 页面解析
    def __page_parse(self, response):
        try:
            # 抽取所有页面
            papers = response.xpath('//div[@class="lismain"]/ul/li')
            # 抽取页面每一
            for paper in papers:
                # 标题
                Title = paper.xpath('./a/text()').extract()[0]
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
            yield Request(self.__WebNodeUrls[response.meta['WebNode']] % (response.meta['page'] + 1), callback=self.__page_parse, cookies= response.meta['cookie'], meta={'cookie': response.meta['cookie'], 'WebNode': response.meta['WebNode'], 'page': (response.meta['page'] + 1)})



# 其他公示
class bsszcxj_q_Spider(Spider):

    # 爬虫名
    name = 'bsszcxj_q'
    # 网站标题
    __WebTitle = '广西百色市住房和城乡建设局'
    # 网站地址
    __WebUrl = 'http://zjw.baise.gov.cn/'
    # 网站节点
    __WebNodes = ['网上公示其他公示']
    # 网站定位
    __Websites = __WebNodes
    # 网站节点地址
    __WebNodeUrls = [  'http://zjw.baise.gov.cn/list-7-%s.html']

    __cookies = {'security_session_mid_verify':'764921e7eec461834328141491879c80',
                'srcurl':'687474703a2f2f7a6a772e62616973652e676f762e636e2f6c6973742d31362d322e68746d6c',
                'yunsuo_session_verify':'c870e71cb9514650aefc0748fc869a32'}

    # 第一个Request请求
    def start_requests(self):
        ses = requests.Session()
        ses.get('http://zjw.baise.gov.cn/list-7-1.html')
        ses.get('http://zjw.baise.gov.cn/list-16-1.html?security_verify_data=313533362c383634')
        ses.get('http://zjw.baise.gov.cn/list-7-1.html')
        cookie = Cookieler(ses).get_cookie()
        cookie.update({'srcurl':'687474703a2f2f7a6a772e62616973652e676f762e636e2f6c6973742d31362d322e68746d6c'})
        return  [Request(self.__WebUrl, callback=self.parse, method='GET', meta={'cookie':cookie})]

    # 第一个响应
    def parse(self, response):
        # 请求队列
        for WebNode,WebNodeUrl in zip(range(len(self.__WebNodes)),self.__WebNodeUrls):
            yield Request(WebNodeUrl % 1, callback=self.__page_parse, cookies= response.meta['cookie'], method='GET', meta={'cookie': response.meta['cookie'], 'WebNode': WebNode, 'page': 1} )


    # 页面解析
    def __page_parse(self, response):
        try:
            # 抽取所有页面
            papers = response.xpath('//div[@class="con"]/ul/li')
            # 抽取页面每一
            for paper in papers:
                # 标题
                Title = paper.xpath('./div[@class="xm"]/a/text()').extract()[0]
                # url
                Url = response.urljoin(paper.xpath('./div[@class="xm"]/a/@href').extract()[0])
                # 日期
                Time = paper.xpath('./div[@class="gs"]/text()').extract()[0]
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
            yield Request(self.__WebNodeUrls[response.meta['WebNode']] % (response.meta['page'] + 1), callback=self.__page_parse, cookies= response.meta['cookie'], meta={'cookie': response.meta['cookie'], 'WebNode': response.meta['WebNode'], 'page': (response.meta['page'] + 1)})

