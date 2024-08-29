from scrapy import *
from ..items import *
from ..utile.HTTPUtile import *

# 广西防城港市公共资源交易中心 #

# 通知公告，工作动态，政策法规,交易信息
class fcgsggzyjyzx_tgzj_Spider(Spider):

    # 爬虫名
    name = 'fcgsggzyjyzx_tgzj'
    # 网站标题
    __WebTitle = '广西防城港市公共资源交易中心'
    # 网站地址
    __WebUrl = 'http://www.fcgggzy.cn/gxfcgzbw/default.aspx'
    # 网站节点
    __WebNodes = ['招投标交易动态中心动态',
                  '招投标交易动态行业动态',

                  '政策法规政府采购国家法规',
                  '政策法规政府采购省级规章',
                  '政策法规政府采购市级文件',
                  '政策法规政府采购中心制度',

                  '政策法规房建市政工程国家法规',
                  '政策法规房建市政工程省级规章',
                  '政策法规房建市政工程市级文件',
                  '政策法规房建市政工程中心制度',

                   '政策法规水利工程国家法规',
                   '政策法规水利工程市级文件',
                   '政策法规水利工程中心制度',

                   '政策法规交通工程国家法规',
                   '政策法规交通工程省级规章',
                   '政策法规交通工程市级文件',
                   '政策法规交通工程中心制度',

                   '交易信息政府采购采购公告',
                   '交易信息房建市政工程招标公告',
                   '交易信息水利工程招标公告',
                   '交易信息交通工程招标公告'
                  ]
    # 网站定位
    __Websites = __WebNodes
    # 网站节点地址
    __WebNodeUrls = [  'https://www.nnggzy.org.cn/nnzbwmanger/ShowInfo/more.aspx?categoryNum=009001',
                       'http://www.fcgggzy.cn/gxfcgzbw/ztbdt/009002/MoreInfo.aspx?CategoryNum=009002',

                       'http://www.fcgggzy.cn/gxfcgzbw/zcfg/003002/003002001/MoreInfo.aspx?CategoryNum=003002001',
                       'http://www.fcgggzy.cn/gxfcgzbw/zcfg/003002/003002002/MoreInfo.aspx?CategoryNum=003002002',
                       'http://www.fcgggzy.cn/gxfcgzbw/zcfg/003002/003002003/MoreInfo.aspx?CategoryNum=003002003',
                       'http://www.fcgggzy.cn/gxfcgzbw/zcfg/003002/003002004/MoreInfo.aspx?CategoryNum=003002004',

                       'http://www.fcgggzy.cn/gxfcgzbw/zcfg/003001/003001001/MoreInfo.aspx?CategoryNum=003001001',
                       'http://www.fcgggzy.cn/gxfcgzbw/zcfg/003001/003001002/MoreInfo.aspx?CategoryNum=003001002',
                       'http://www.fcgggzy.cn/gxfcgzbw/zcfg/003001/003001003/MoreInfo.aspx?CategoryNum=003001003',
                       'http://www.fcgggzy.cn/gxfcgzbw/zcfg/003001/003001004/MoreInfo.aspx?CategoryNum=003001004',

                       'http://www.fcgggzy.cn/gxfcgzbw/zcfg/003004/003004001/MoreInfo.aspx?CategoryNum=003004001',
                       'http://www.fcgggzy.cn/gxfcgzbw/zcfg/003004/003004003/MoreInfo.aspx?CategoryNum=003004003',
                       'http://www.fcgggzy.cn/gxfcgzbw/zcfg/003004/003004004/MoreInfo.aspx?CategoryNum=003004004',

                       'http://www.fcgggzy.cn/gxfcgzbw/zcfg/003007/003007001/MoreInfo.aspx?CategoryNum=003007001',
                       'http://www.fcgggzy.cn/gxfcgzbw/zcfg/003007/003007002/MoreInfo.aspx?CategoryNum=003007002',
                       'http://www.fcgggzy.cn/gxfcgzbw/zcfg/003007/003007003/MoreInfo.aspx?CategoryNum=003007003',
                       'http://www.fcgggzy.cn/gxfcgzbw/zcfg/003007/003007004/MoreInfo.aspx?CategoryNum=003007004',

                       'http://www.fcgggzy.cn/gxfcgzbw/jyxx/001004/001004001/MoreInfo.aspx?CategoryNum=001004001',
                       'http://www.fcgggzy.cn/gxfcgzbw/jyxx/001001/001001001/MoreInfo.aspx?CategoryNum=001001001',
                       'http://www.fcgggzy.cn/gxfcgzbw/jyxx/001011/001011001/MoreInfo.aspx?CategoryNum=001011001',
                       'http://www.fcgggzy.cn/gxfcgzbw/jyxx/001010/001010001/MoreInfo.aspx?CategoryNum=001010001'
                       ]

    # 第一个Request请求
    def start_requests(self):
        return  [Request(self.__WebUrl, callback=self.parse, method='GET', meta={'cookiejar':1})]

    # 第一个响应
    def parse(self, response):
        # 请求队列
        for WebNode,WebNodeUrl in zip(range(len(self.__WebNodes)),self.__WebNodeUrls):
            yield Request(WebNodeUrl, callback=self.__page_parse, method='GET', meta={'cookiejar': response.meta['cookiejar'], 'WebNode': WebNode, 'page':1})

    # 页面解析
    def __page_parse(self, response):
        try:
            # 抽取所有页面
            papers = response.xpath('//table[@id="MoreInfoList1_DataGrid1"]//tr')
            if not papers:
                papers = response.xpath('//table[@id="MoreInfoListZbgs1_DataGrid1"]//tr')
            # 抽取页面每一
            for paper in papers:
                # 标题
                Title = paper.xpath('./td[@align="left"]/a/@title').extract()[0]
                # url
                Url = response.urljoin(paper.xpath('./td[@align="left"]/a/@href').extract()[0])
                # 日期
                Time = paper.xpath('./td[last()]/text()').extract()[0]
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
            formdata = {'__EVENTTARGET': 'MoreInfoList1$Pager',
                        '__EVENTARGUMENT': '%d' % (response.meta['page'] + 1),
                        '__VIEWSTATEENCRYPTED':''
                        }
            yield FormRequest.from_response(response=response, callback=self.__page_parse, formdata=formdata, meta={'cookiejar': response.meta['cookiejar'], 'WebNode':response.meta['WebNode'], 'page':(response.meta['page'] +1)})

