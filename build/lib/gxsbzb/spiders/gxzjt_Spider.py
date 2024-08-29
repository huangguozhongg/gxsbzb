import re, requests
from scrapy import *
from ..items import *
from ..utile.HTTPUtile import *

## 广西住房和城乡建设厅网站 ##

# 文件通知，公示公告，政策法规，政策解读
class gxzjt_wgzz_Spider(Spider):

    # 爬虫名
    name = 'gxzjt_wgzz'
    # 网站标题
    __WebTitle = '广西住房和城乡建设厅网站'
    # 网站地址
    __WebUrl = 'http://www.gxzjt.gov.cn/'
    # 网站节点
    __WebNodes = ['政务公开文件通知',
                  '公示公告',
                  '政务公开政策法规',
                  '政务公开政策解读'
                  ]
    # 网站定位
    __Websites = __WebNodes
    # 网站节点地址
    __WebNodeUrls = [  'http://www.gxzjt.gov.cn/news/wjtz.aspx?InfoLabelID=218&Area=450000',
                       'http://www.gxzjt.gov.cn/news/newslist.aspx?InfoLabelID=247&Area=450000',
                       'http://www.gxzjt.gov.cn/twgk/xxgkml.aspx?SubjectID=102',
                       'http://www.gxzjt.gov.cn/news/Subject.aspx?ZTID=400&ZT=400'
                    ]
    # 网络节点参数
    __WebNodeParams = [218, 247, 102, 400]

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
            papers = response.xpath('//*[@id="form1"]/div[4]/div[1]/div[2]/div[3]/table[2]/tbody/tr[@bgcolor="#ffffff"]')
            if not papers:
                papers = response.xpath('//*[@id="form1"]/div[4]/div[1]/div[2]/div[3]/table[1]/tbody/tr[@bgcolor="#ffffff"]')
            # 抽取页面每一
            for paper in papers:
                # 标题
                Title = ''
                try:
                    Title = paper.xpath('.//a/text()').extract()[0].strip()
                except:
                    Title = paper.xpath('.//font/text()').extract()[0].strip()
                # Url
                Url = response.urljoin(paper.xpath('.//a/@href').extract()[0].strip())
                # 日期
                Time = re.search('(\d{4}).(\d{2}).(\d{2})',paper.xpath('.//td[last()]/text()').extract()[0]).group(0)
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
            formdata = {}
            if self.__WebNodeParams[response.meta['WebNode']] in [218,247]:
                InfoLabelID_formdata = {'__EVENTTARGET': 'AspNetPager1',
                                        '__EVENTARGUMENT': '%d' % (response.meta['page'] + 1),
                                        'searchword': '输入关键字',
                                        'keyword': '',
                                        'InfoLabel': '%d' % self.__WebNodeParams[response.meta['WebNode']],
                                        'Area': '450000',
                                        'starttime': '',
                                        'endtime': '',
                                        'AspNetPager1_input': '%d' % response.meta['page']
                                        }
                formdata.update(InfoLabelID_formdata)
            elif self.__WebNodeParams[response.meta['WebNode']] in [102]:
                SubjectID_formdata = {'__EVENTTARGET': 'AspNetPager1',
                                        '__EVENTARGUMENT': '%d' % (response.meta['page'] + 1),
                                        'searchword': '输入关键字',
                                        'keyword': '',
                                        'ddlThemecat': '',
                                        'ddlSubcat': '',
                                        'ddlSubjectID': '%d' % self.__WebNodeParams[response.meta['WebNode']],
                                        'starttime': '',
                                        'endtime': ''
                                        }
                formdata.update(SubjectID_formdata)
            else:
                ZTID_formdata = {'__EVENTTARGET': 'AspNetPager1',
                                '__EVENTARGUMENT': '%d' % (response.meta['page'] + 1),
                                'searchword': '输入关键字'
                            }
                formdata.update(ZTID_formdata)
            yield FormRequest.from_response(response, callback=self.__page_parse, formdata=formdata, meta={'cookiejar': response.meta['cookiejar'], 'WebNode':response.meta['WebNode'], 'page':(response.meta['page'] +1)})
