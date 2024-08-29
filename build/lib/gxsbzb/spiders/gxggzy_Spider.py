# -*- coding: utf-8 -*-
from scrapy import *
from ..items import *
from ..utile.HTTPUtile import *

## 广西壮族自治区公共资源交易中心##

# 招标交易动态和通知公告
class gxggzy_zbjydt_Spider(Spider):

    # 爬虫的名称
    name = 'gxggzy_zbjydt'
    # 网站标题
    __WebTitle = '广西壮族自治区公共资源交易中心'
    # 网站地址
    __WebUrl = 'http://gxggzy.gxzf.gov.cn/gxzbw/default.aspx'
    # 网站节点
    __WebNodes = ['招投标交易动态中心动态',
                  '招投标交易动态行业动态',
                  '招投标交易动态综合新闻',
                  '通知公告'
                  ]
    # 网站定位
    __Websites = __WebNodes
    # 网站节点地址
    __WebNodeUrls = ['http://gxggzy.gxzf.gov.cn/gxzbw/ztbdt/009001/MoreInfo.aspx?CategoryNum=009001',
                    'http://gxggzy.gxzf.gov.cn/gxzbw/ztbdt/009002/MoreInfo.aspx?CategoryNum=009002',
                    'http://gxggzy.gxzf.gov.cn/gxzbw/ztbdt/009003/MoreInfo.aspx?CategoryNum=009003',
                    'http://gxggzy.gxzf.gov.cn/gxzbw/tzgg/MoreInfo.aspx?CategoryNum=008'
                    ]

    # 第一个Request请求
    def start_requests(self):
        return  [Request(self.__WebUrl, callback=self.parse, method='GET', meta={'cookiejar':1})]

    # POST请求头
    __post_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'gxggzy.gxzf.gov.cn',
        'Origin': 'http://gxggzy.gxzf.gov.cn',
        'Referer': 'http://gxggzy.gxzf.gov.cn/gxzbw/ztbdt/009001/MoreInfo.aspx?CategoryNum=009001',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
    }

    ## 第一个Response响应
    def parse(self, response):
        # 请求队列
        for WebNode,WebNodeUrl in zip(range(len(self.__WebNodes)),self.__WebNodeUrls):
            yield Request(WebNodeUrl, callback=self.__page_parse, method='GET',headers=self.__post_headers, meta={'cookiejar': response.meta['cookiejar'], 'WebNode': WebNode, 'page':1})

    # 页面解析
    def __page_parse(self,response):
        try:
            # 首先抽取所有的文章
            papers = response.xpath('//table[@id="MoreInfoList1_DataGrid1"]//tr')
            # 从每篇文章中抽取数据
            for paper in papers:
                # 标题
                Title = paper.xpath('./td[2]/a/@title').extract()[0].strip()
                # url
                Url = response.urljoin(paper.xpath('./td[2]/a/@href').extract()[0].strip())
                # 日期
                Time = paper.xpath('./td[last()]/text()').extract()[0].strip()
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
            # 提交request
            formdata = {'__EVENTTARGET': 'MoreInfoList1$Pager', '__EVENTARGUMENT': '%d' % (response.meta['page'] + 1), '__VIEWSTATEENCRYPTED':'' }
            yield FormRequest.from_response(response=response, callback=self.__page_parse, headers=self.__post_headers, formdata=formdata, meta={'cookiejar': response.meta['cookiejar'], 'WebNode':response.meta['WebNode'], 'page':(response.meta['page']+1)})