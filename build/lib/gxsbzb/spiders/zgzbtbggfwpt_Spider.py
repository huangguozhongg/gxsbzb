import re
from scrapy import *
from ..items import *
from ..utile.HTTPUtile import *

## 中国招标投标公共服务平台 ##

# 资格预审，招标公告，中标候选人公示，中标结果公示，更正公告公示
class zgzbtbggfwpt_zzzzg_Spider(Spider):

    # 爬虫名
    name = 'zgzbtbggfwpt_zzzzg'
    # 网站标题
    __WebTitle = '中国招标投标公共服务平台'
    # 网站地址
    __WebUrl = 'http://bulletin.cebpubservice.com/'
    # 网站节点
    __WebNodes = ['资格预审',
                  '招标公告',
                  '中标候选人公示',
                  '中标结果公示',
                  '更正公告公示']
    # 网站定位
    __Websites = __WebNodes
    # 网站节点地址
    __WebNodeUrls = [ 'http://bulletin.cebpubservice.com/xxfbcmses/search/qualify.html?searchDate=1994-11-13&dates=300&categoryId=92&industryName=&area=450000&status=&publishMedia=&sourceInfo=&showStatus=&word=&page=%d',
                      'http://bulletin.cebpubservice.com/xxfbcmses/search/bulletin.html?searchDate=1994-11-13&dates=300&categoryId=88&industryName=&area=450000&status=&publishMedia=&sourceInfo=&showStatus=&word=&page=%d',
                      'http://bulletin.cebpubservice.com/xxfbcmses/search/candidate.html?searchDate=1994-11-13&dates=300&categoryId=91&industryName=&area=450000&status=&publishMedia=&sourceInfo=&showStatus=&word=&page=%d',
                      'http://bulletin.cebpubservice.com/xxfbcmses/search/result.html?searchDate=1994-11-13&dates=300&categoryId=90&industryName=&area=450000&status=&publishMedia=&sourceInfo=&showStatus=&word=&page=%d',
                      'http://bulletin.cebpubservice.com/xxfbcmses/search/change.html?searchDate=1994-11-13&dates=300&categoryId=89&industryName=&area=450000&status=&publishMedia=&sourceInfo=&showStatus=&word=&page=%d']


    # 第一个Request请求
    def start_requests(self):
        return  [Request(self.__WebUrl, callback=self.parse, method='GET', meta={'cookiejar':1})]

    # 第一个Request响应
    def parse(self, response):
        # 请求队列
        for WebNode,WebNodeUrl in zip(range(len(self.__WebNodes)),self.__WebNodeUrls):
            yield Request(WebNodeUrl % 1, callback=self.__page_parse, method='GET', meta={'cookiejar': response.meta['cookiejar'], 'WebNode': WebNode, 'page':1})

    # 页面解析
    def __page_parse(self, response):
        try:
            # 抽取所有页面
            papers = response.xpath('//table[@class="table_text"]//tr[position()>1]')
            # 抽取页面每一
            for paper in papers:
                # 标题
                Title = paper.xpath('./td[1]/a/@title').extract()[0].strip()
                # url
                Url = re.findall(r"(?<=javascript:urlOpen\(').*(?='\))", paper.xpath('./td[1]/a/@href').extract()[0])[0]
                # 日期
                Time = paper.xpath('./td[5]/text()').extract()[0]
                if not Time:
                    Time = paper.xpath('./td[4]/text()').extract()[0]
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
            yield Request(self.__WebNodeUrls[response.meta['WebNode']] % (response.meta['page'] + 1), callback=self.__page_parse, meta={'cookiejar': response.meta['cookiejar'], 'WebNode':response.meta['WebNode'], 'page':(response.meta['page'] +1)})

