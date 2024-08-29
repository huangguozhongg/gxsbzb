# -*- coding: utf-8 -*-
from scrapy import *
from ..items import *
from ..utile.HTTPUtile import *

## 7.广西壮族自治区自然资源厅网站##

# 国土要闻，国内资讯，本顶通知，公示公告
class gxzrzytwz_ggbg_Spider(Spider):

    # 爬虫名
    name = 'gxzrzytwz_ggbg'
    # 网站标题
    __WebTitle = '广西壮族自治区自然资源厅网站'
    # 网站地址
    __WebUrl = 'http://dnr.gxzf.gov.cn/'
    # 网站节点
    __WebNodes = [
                  '新闻中心国土要闻',
                  '新闻中心国内资讯',
                  '通知公告',
                  '通知公告'
                  ]
    # 网站定位
    __Websites = __WebNodes
    # 网站节点地址
    __WebNodeParam = [154, 155, 113, 114]

    # POST请求头
    __post_headers ={'Accept': 'text/html, */*; q=0.01',
                     'Accept-Encoding': 'gzip, deflate',
                     'Accept-Language': 'zh-CN,zh;q=0.9',
                     'Cache-Control': 'max - age = 0',
                     'Connection': 'keep-alive',
                     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                     'Host': 'dnr.gxzf.gov.cn',
                     'Origin': 'http://dnr.gxzf.gov.cn',
                     'Referer': 'http://dnr.gxzf.gov.cn/columnShow?id=154',
                     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
                     'X-Requested-With': 'XMLHttpRequest'
                     }


    # 第一个Rqeust请求
    def start_requests(self):
        return  [Request(self.__WebUrl, callback=self.parse, meta={'cookiejar':1})]

    # 第一个Request响应
    def parse(self, response):
        # Request请求队列
        for WebNode in range(len(self.__WebNodes)):
            yield self.__post_request(WebNode, 1 ,meta={'cookiejar':response.meta['cookiejar'], 'WebNode': WebNode, 'page': 1})


    # Request构造
    def __post_request(self, WebNode, page, meta):
        return  FormRequest('http://dnr.gxzf.gov.cn/columnNewsList',
                               callback=self.__page_parse,
                               headers=self.__post_headers,
                               formdata={'pageNum':'%d' % page, 'id':'%d' % self.__WebNodeParam[WebNode], 'tags':''},
                               method='POST',
                               meta=meta)

    # 页面解析
    def __page_parse(self, response):
        try:
            # 首先抽取所有的文章
            papers = response.xpath('//ul[@class="txt-list"]/li[@style]')
            # 从每篇文章中抽取数据
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
        except Exception as e:
            print(e)
        else:
            # Request跟进
            yield  self.__post_request(response.meta['WebNode'], (response.meta['page'] + 1), meta={'cookiejar':response.meta['cookiejar'], 'WebNode': response.meta['WebNode'], 'page': (response.meta['page']+1)})