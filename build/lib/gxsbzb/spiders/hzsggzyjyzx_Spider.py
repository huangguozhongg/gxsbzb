from scrapy import *
from ..items import *
from ..utile.HTTPUtile import *

# 广西贺州市公共资源交易中心 #

# 工作动态，政策法规，招标公告
class hzsggzyjyzx_gzz_Spider(Spider):

    # 爬虫名
    name = 'hzsggzyjyzx_gzz'
    # 网站标题
    __WebTitle = '广西贺州市公共资源交易中心'
    # 网站地址
    __WebUrl = 'http://ggzyjy.gxhz.gov.cn/page__gp_portal/frame_home.aspx?id=5134ee3c-a037-43b3-a3ca-7e8c6effcd68'
    # 网站节点
    __WebNodes = [
                  '工作动态',

                  '政策法规法律法规',
                  '政策法规政策解读',
                  '政策法规中心文件',

                  '招标公告',
                  ]
    # 网站定位
    __Websites = __WebNodes
    # 网站节点地址
    __WebNodeUrls = [  'http://ggzyjy.gxhz.gov.cn/page__gp_portal/list_article.aspx?id=4ecf1343-8f00-493e-9b28-821c86db972a',

                       'http://ggzyjy.gxhz.gov.cn/page__gp_portal/list_article.aspx?id=16f8fd70-c1a7-4e25-b691-8b8a4f7b84c4',
                       'http://ggzyjy.gxhz.gov.cn/page__gp_portal/list_article.aspx?id=ce058db7-b8bc-4def-be94-1c218d606368',
                       'http://ggzyjy.gxhz.gov.cn/page__gp_portal/list_article.aspx?id=7340cb6f-83ce-4038-9acd-3ac71de67593',

                       'http://ggzyjy.gxhz.gov.cn/page__gp_portal/list_article.aspx?id=9ba20408-67c2-4f11-bc77-13d0dd4c8748',
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
            papers = response.xpath('//table[@id="Main_unitList_lstMain"]//tr[contains(@class,"grid-item")]')
            # 抽取页面每一
            for paper in papers:
                # 标题
                Title = paper.xpath('./td[3]/a/text()').extract()[0]
                # url
                Url = response.urljoin(re.search('(?<="window\.open\(").*？(?=")',paper.xpath('./td[3]/a/@onclick').extract()[0]))
                # 日期
                tmp_Time = paper.xpath('./td[4]/span/text()').extract()[0]
                Time = '20' + tmp_Time[0:5] +  '-' + tmp_Time[6:8]
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
            formdata = {
                        'ctl00$Main$unitList$ctl00$ddl_fField': 'fEntityName',
                        'ctl00$Main$unitList$ctl00$ddl_fType': '_3_Equal',
                        'ctl00$Main$unitList$unitPager$lstMain$ctl02$btnPage': '%d' % (response.meta['page']+1),
                        'ctl00$Main$noB$noB_NoBotExtender_ClientState': '-793'
                        }
            yield FormRequest.from_response(response=response, callback=self.__page_parse, formdata=formdata, meta={'cookiejar': response.meta['cookiejar'], 'WebNode':response.meta['WebNode'], 'page':(response.meta['page'] +1)})

