from scrapy import *
from ..items import *
from ..utile.HTTPUtile import *
import requests
from bs4 import BeautifulSoup

# 广西财经学院 #

# 采购信息
class gxcjxy_c_Spider(Spider):

    # 爬虫名
    name = 'gxcjxy_c'
    # 网站标题
    __WebTitle = '广西财经学院'
    # 网站地址
    __WebUrl = 'http://www.gxufe.edu.cn/www/myweb/home.xhtml'
    # 网站节点
    __WebNodes = [
                  '采购信息'
                  ]
    # 网站定位
    __Websites = __WebNodes
    # 网站节点地址
    __WebNodeUrls = [
                       'http://www.gxufe.edu.cn/www/myweb/level_2.xhtml?typeid=www010e&typeid0=www01'
                       ]
    # Post请求头
    __post_headers = {
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'zh-CN,zh;q=0.9',
                        'Cache-Control': 'max-age=0',
                        'Connection': 'keep-alive',
                        # 'Content-Length': '174',
                        'Content-Type': 'application/x-www-form-urlencoded',
                        # 'Cookie': 'JSESSIONID=w0E1EUNhYitshGlDJVdmDlerSFMthN2NVxViOhLE.wwwnode02; route=a22d069db8d3c2020449038a917305f8',
                        'Host': 'www.gxufe.edu.cn',
                        'Origin': 'http://www.gxufe.edu.cn',
                        'Referer': 'http://www.gxufe.edu.cn/www/myweb/informationSearch.xhtml',
                        'Upgrade-Insecure-Requests': '1',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
                        }

    # 第一个Request请求
    def start_requests(self):
        return  [Request(self.__WebUrl, callback=self.parse, method='GET', meta={'cookiejar':1})]

    # 第一个Response响应
    def parse(self, response):
        # 请求队列
        for WebNode,WebNodeUrl in zip(range(len(self.__WebNodes)),self.__WebNodeUrls):
            yield Request(WebNodeUrl, callback=self.__page_parse, method='GET', meta={'cookiejar': response.meta['cookiejar'], 'WebNode': WebNode, 'page':1})

    # 页面解析
    def __page_parse(self, response):
        try:
            # 抽取所有页面
            papers = response.xpath('//div[@class="news_bb"]/ul/li')
            # 抽取页面每一
            for paper in papers:
                # 标题
                Title = paper.xpath('./span[@class="n_bb"]/a[last()]/@title').extract()[0]
                # url
                Url = response.urljoin(paper.xpath('./span[@class="n_bb"]/a[last()]/@href').extract()[0])
                # 日期
                Time = paper.xpath('./span[last()]/text()').extract()[0]
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
            pass
            # formdata = {
            #             # 'j_idt62': 'j_idt62',
            #             # 'j_idt62-j_idt101': 'www010e',
            #             'j_idt62-j_idt137': 'j_idt62-j_idt137'
            #             }
            # # 跟进请求
            # yield FormRequest.from_response(response=response, callback=self.__page_parse, headers = self.__post_headers, formdata=formdata, meta={'cookiejar': response.meta['cookiejar'], 'WebNode':response.meta['WebNode'], 'page':(response.meta['page'] +1)})

