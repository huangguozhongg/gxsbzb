import re
from scrapy import *
from ..items import *
from ..utile.HTTPUtile import *
## 广西建设网 ##

# 招标信息
class gxjsw_zbxx_Spider(Spider):

    # 爬虫名
    name = 'gxjsw_zbxx'
    # 网站标题
    __WebTitle = '广西建设网'
    # 网站地址
    __WebUrl = 'http://www.gxcic.net/default.aspx'
    # 网站节点
    __WebNodes = ['招标信息施工招标',
                  '招标信息勘察招标',
                  '招标信息城乡规划',
                  '招标信息设计招标',
                  '招标信息监理招标',
                  '招标信息材料设备招标',
                  '招标信息其它招标']
    # 网站定位
    __Websites = __WebNodes
    # 网站节点地址
    __WebNodeUrls = ['http://www.gxcic.net/ztb/ztblist.aspx?ZGZbfl=%CA%A9%B9%A4%D5%D0%B1%EA',
                     'http://www.gxcic.net/ztb/ztblist.aspx?ZGZbfl=%BF%B1%B2%EC%D5%D0%B1%EA',
                     'http://www.gxcic.net/ztb/ztblist.aspx?ZGZbfl=%B3%C7%CF%E7%B9%E6%BB%AE',
                     'http://www.gxcic.net/ztb/ztblist.aspx?ZGZbfl=%C9%E8%BC%C6%D5%D0%B1%EA',
                     'http://www.gxcic.net/ztb/ztblist.aspx?ZGZbfl=%BC%E0%C0%ED%D5%D0%B1%EA',
                     'http://www.gxcic.net/ztb/ztblist.aspx?ZGZbfl=%B2%C4%C1%CF%C9%E8%B1%B8%D5%D0%B1%EA',
                     'http://www.gxcic.net/ztb/ztblist.aspx?ZGZbfl=%C6%E4%CB%FC%D5%D0%B1%EA'
                     ]

    # 第一个Request请求
    def start_requests(self):
        return  [Request(self.__WebUrl, callback=self.parse, method='GET', meta={'cookiejar':1})]

    # 第一个Request响应
    def parse(self, response):
        # 请求队列
        for WebNode,WebNodeUrl in zip(range(len(self.__WebNodes)),self.__WebNodeUrls):
            yield Request(WebNodeUrl, callback=self.__page_parse, method='GET', meta={'cookiejar': response.meta['cookiejar'], 'WebNode': WebNode, 'page':1})


    # 页面解析
    def __page_parse(self, response):
        try:
            # 抽取所有页面
            papers = response.xpath('//*[@id="page-right0"]/div[2]/table[3]/tbody/tr[@bgcolor="#ffffff"]')
            # 抽取页面每一
            for paper in papers:
                # 标题
                Title = paper.xpath('.//a/text()').extract()[0]
                # url
                Url = response.urljoin(paper.xpath('.//a/@href').extract()[0])
                # 日期
                Time = re.search('(\d{2}).(\d{2}).(\d{2})',paper.xpath('.//td[last()]/text()').extract()[0]).group(0)
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
            # 跟进Request
            formdata = {'__EVENTTARGET': 'AspNetPager1',
                        '__EVENTARGUMENT': '%d' % (response.meta['page'] +1),
                        'searchword': '输入关键字',
                        'keyword': '',
                        'ZGZbfl': '',
                        'ChannelId1': '450000',
                        'ChannelId2': '0',
                        'ChannelId3': '0',
                        'starttime': '',
                        'endtime': '',
                        'AspNetPager1_input': '%d' % response.meta['page']
                        }
            yield FormRequest.from_response(response, callback=self.__page_parse, formdata=formdata, meta={'cookiejar': response.meta['cookiejar'], 'WebNode':response.meta['WebNode'], 'page':(response.meta['page'] +1)})


# 热点信息
class gxjsw_rdxx_Spider(Spider):

    # 爬虫名
    name = 'gxjsw_rdxx'
    # 网站标题
    __WebTitle = '广西建设网'
    # 网站地址
    __WebUrl = 'http://www.gxcic.net/default.aspx'
    # 网站节点
    __WebNodes = ['文件通知',
                  '公示公告',
                  '政策法规',
                  '培训考试',
                  '监督检查'
                  ]
    # 网站定位
    __Websites = __WebNodes
    # 网站节点地址
    __WebNodeUrls = ['http://www.gxcic.net/news/newslist.aspx?InfoLabelID=218&Area=450000',
                     'http://www.gxcic.net/news/newslist.aspx?InfoLabelID=247&Area=450000',
                     'http://www.gxcic.net/twgk/xxgkml.aspx?SubjectID=102',
                     'http://www.gxcic.net/news/newsclass.aspx?ClassID=6',
                     'http://www.gxcic.net/twgk/xxgkml.aspx?SubjectID=106'
                     ]
    # 网站节点参数
    __WebNodeParam = [218, 247, 102, 6, 106]
    # Post请求头
    __post_headers ={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'Cache-Control': 'max-age=0',
                    'Connection': 'keep-alive',
                    'Content-Type': 'application/x-www-form-urlencoded',
                     'Host': 'www.gxcic.net',
                    'Origin': 'http://www.gxcic.net',
                    'Referer': 'http://www.gxcic.net/news/newslist.aspx?InfoLabelID=218&Area=450000',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'}

    # 第一个Request请求
    def start_requests(self):
        return [Request(self.__WebUrl, callback=self.parse, method='GET', meta={'cookiejar': 1})]

    # 第一个Request响应
    def parse(self, response):
        # 请求队列
        for WebNode,WebNodeUrl in zip(range(len(self.__WebNodes)),self.__WebNodeUrls):
            yield Request(WebNodeUrl, callback=self.__page_parse, method='GET', meta={'cookiejar': response.meta['cookiejar'], 'WebNode': WebNode, 'page':1})

    # 页面解析
    def __page_parse(self, response):
        try:
            # 抽取所有页面
            papers = response.xpath('//*[@id="form1"]/div[4]/div/div[2]/div[3]/table[2]/tbody/tr')
            # 抽取页面每一
            for paper in papers:
                # 标题
                Title = paper.xpath('.//font/text()').extract()[0]
                # url
                Url = response.urljoin(paper.xpath('.//a/@href').extract()[0])
                # 日期
                Time = re.search('(\d{2}).(\d{2}).(\d{2})', paper.xpath('.//td[last()]/text()').extract()[0]).group(0)
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
            # 跟进Request
            InfoLabelID_formdata = {'__EVENTTARGET': 'AspNetPager1',
                                    '__EVENTARGUMENT': '%d' % (response.meta['page']+1),
                                    'searchword': '输入关键字',
                                    'keyword': '',
                                    'InfoLabel': '%d' % self.__WebNodeParam[response.meta['WebNode']],
                                    'Area': '450000',
                                    'starttime': '',
                                    'endtime': '',
                                    'AspNetPager1_input': '%d' % response.meta['page']
                                    }

            SubjectID_formadata = {'__EVENTTARGET': 'AspNetPager1',
                                    '__EVENTARGUMENT': '%d' % (response.meta['page'] + 1),
                                    'searchword': '',
                                    'keyword': '',
                                    'ddlThemecat': '',
                                    'ddlSubcat': '',
                                    'ddlSubjectID': '%d' % self.__WebNodeParam[response.meta['WebNode']],
                                    'starttime': '',
                                    'endtime': ''
                                   }
            if self.__WebNodeParam[response.meta['WebNode']] in [218,247]:
                yield FormRequest.from_response(response,callback=self.__page_parse, headers=self.__post_headers,formdata=InfoLabelID_formdata , meta={'cookiejar': response.meta['cookiejar'], 'WebNode': response.meta['WebNode'], 'page': (response.meta['page'] + 1)}, formxpath='//*[@id="form1"]')
            else:
                yield FormRequest.from_response(response, callback=self.__page_parse, headers=self.__post_headers, formdata=SubjectID_formadata, meta={'cookiejar': response.meta['cookiejar'], 'WebNode': response.meta['WebNode'], 'page': (response.meta['page'] + 1)}, formxpath='//*[@id="form1"]')

