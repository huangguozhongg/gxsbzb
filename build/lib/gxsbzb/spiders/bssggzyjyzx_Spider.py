from scrapy import *
from ..items import *
from ..utile.HTTPUtile import *

# 广西百色市公共资源交易中心网 #

#  招投标交易动态,通知公告，政策法规,交易信息
class bssggzyjyzx_ztzj_Spider(Spider):

    # 爬虫名
    name = 'bssggzyjyzx_ztzj'
    # 网站标题
    __WebTitle = '广西百色市公共资源交易中心网'
    # 网站地址
    __WebUrl = 'http://www.bsggzy.cn/gxbszbw/default.aspx'
    # 网站节点
    __WebNodes = [
                  '招投标交易动态工作动态',
                  '招投标交易动态行业动态',
                  '通知公告',

                  '政策法规工程建设国家法规',
                  '政策法规工程建设省级规章',
                  '政策法规工程建设市级文件',
                  '政策法规工程建设中心制度',

                  '政策法规政府采购国家法规',
                  '政策法规政府采购省级规章',
                  '政策法规政府采购市级文件',
                  '政策法规政府采购中心制度',

                  '政策法规产权交易国家法规',
                  '政策法规产权交易省级规章',
                  '政策法规产权交易市级文件',
                  '政策法规产权交易中心制度',

                  '政策法规水利交通国家法规',
                  '政策法规水利交通省级规章',
                  '政策法规水利交通市级文件',
                  '政策法规水利交通中心制度',

                  ' 政策法规土地交易国家法规',
                  ' 政策法规土地交易省级规章',
                  ' 政策法规土地交易市级文件',
                  ' 政策法规土地交易中心制度',

                  '交易信息工程建设招标公告',
                  '交易信息政府采购采购公告'
                  ]
    # 网站定位
    __Websites = __WebNodes
    # 网站节点地址
    __WebNodeUrls = [
                       'http://www.bsggzy.cn/gxbszbw/ztbdt/009001/MoreInfo.aspx?CategoryNum=009001',
                       'http://www.bsggzy.cn/gxbszbw/ztbdt/009002/MoreInfo.aspx?CategoryNum=009002',
                       'http://www.bsggzy.cn/gxbszbw/tzgg/MoreInfo.aspx?CategoryNum=008',

                       'http://www.bsggzy.cn/gxbszbw/zcfg/003001/003001001/MoreInfo.aspx?CategoryNum=003001001',
                       'http://www.bsggzy.cn/gxbszbw/zcfg/003001/003001002/MoreInfo.aspx?CategoryNum=003001002',
                       'http://www.bsggzy.cn/gxbszbw/zcfg/003001/003001003/MoreInfo.aspx?CategoryNum=003001003',
                       'http://www.bsggzy.cn/gxbszbw/zcfg/003001/003001004/MoreInfo.aspx?CategoryNum=003001004',

                       'http://www.bsggzy.cn/gxbszbw/zcfg/003002/003002001/MoreInfo.aspx?CategoryNum=003002001',
                       'http://www.bsggzy.cn/gxbszbw/zcfg/003002/003002002/MoreInfo.aspx?CategoryNum=003002002',
                       'http://www.bsggzy.cn/gxbszbw/zcfg/003002/003002003/MoreInfo.aspx?CategoryNum=003002003',
                       'http://www.bsggzy.cn/gxbszbw/zcfg/003002/003002004/MoreInfo.aspx?CategoryNum=003002004',

                       'http://www.bsggzy.cn/gxbszbw/zcfg/003003/003003001/MoreInfo.aspx?CategoryNum=003003001',
                       'http://www.bsggzy.cn/gxbszbw/zcfg/003003/003003002/MoreInfo.aspx?CategoryNum=003003002',
                       'http://www.bsggzy.cn/gxbszbw/zcfg/003003/003003003/MoreInfo.aspx?CategoryNum=003003003',
                       'http://www.bsggzy.cn/gxbszbw/zcfg/003003/003003004/MoreInfo.aspx?CategoryNum=003003004',

                       'http://www.bsggzy.cn/gxbszbw/zcfg/003004/003004001/MoreInfo.aspx?CategoryNum=003004001',
                       'http://www.bsggzy.cn/gxbszbw/zcfg/003004/003004002/MoreInfo.aspx?CategoryNum=003004002',
                       'http://www.bsggzy.cn/gxbszbw/zcfg/003004/003004003/MoreInfo.aspx?CategoryNum=003004003',
                       'http://www.bsggzy.cn/gxbszbw/zcfg/003004/003004004/MoreInfo.aspx?CategoryNum=003004004',

                       'http://www.bsggzy.cn/gxbszbw/zcfg/003005/003005001/MoreInfo.aspx?CategoryNum=003005001',
                       'http://www.bsggzy.cn/gxbszbw/zcfg/003005/003005002/MoreInfo.aspx?CategoryNum=003005002',
                       'http://www.bsggzy.cn/gxbszbw/zcfg/003005/003005003/MoreInfo.aspx?CategoryNum=003005003',
                       'http://www.bsggzy.cn/gxbszbw/zcfg/003005/003005004/MoreInfo.aspx?CategoryNum=003005004',

                       'http://www.bsggzy.cn/gxbszbw/jyxx/001001/001001001/MoreInfo.aspx?CategoryNum=001001001',
                       'http://www.bsggzy.cn/gxbszbw/jyxx/001004/001004001/MoreInfo.aspx?CategoryNum=001004001'
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

