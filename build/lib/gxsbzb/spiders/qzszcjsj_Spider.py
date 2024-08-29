from scrapy import *
from ..items import *
from ..utile.HTTPUtile import *

# 广西钦州市住房和城乡建设局 #

# 政务公开，行业管理
class qzszcjsj_zh_Spider(Spider):

    # 爬虫名
    name = 'qzszcjsj_zh'
    # 网站标题
    __WebTitle = '广西钦州市住房和城乡建设局'
    # 网站地址
    __WebUrl = 'http://zjj.qinzhou.gov.cn/sy_12787/'
    # 网站节点
    __WebNodes = [
                  '政务公开文件通知',
                  '政务公开公示公告',
                  '政务公开政策法规及解读',
                  '行业管理招标公告'
                  ]
    # 网站定位
    __Websites = __WebNodes
    # 网站节点地址
    __WebNodeUrls = [
                       'http://zjj.qinzhou.gov.cn/zwgk_12788/wjtz/index_%s.html',
                       'http://zjj.qinzhou.gov.cn/zwgk_12788/gsgg_12861/index_%s.html',
                       'http://zjj.qinzhou.gov.cn/zwgk_12788/zcfg_12815/index_%s.html',
                       'http://zjj.qinzhou.gov.cn/hygl/zbgg/index_%s.html'
                       ]

    # 第一个Request请求
    def start_requests(self):
        return  [Request(self.__WebUrl, callback=self.parse, method='GET', meta={'cookiejar':1})]

    # 第一个Response响应
    def parse(self, response):
        # 请求队列
        for WebNode,WebNodeUrl in zip(range(len(self.__WebNodes)),self.__WebNodeUrls):
            yield Request(WebNodeUrl.replace('_%s',''), callback=self.__page_parse, method='GET', meta={'cookiejar': response.meta['cookiejar'], 'WebNode': WebNode, 'page':1})

    # 页面解析
    def __page_parse(self, response):
        try:
            # 抽取所有页面
            papers = response.xpath('//ul[@class="ul5_list mt20"]/li[not(@style)]')
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
            # 跟进请求
            yield Request(self.__WebNodeUrls[response.meta['WebNode']] % response.meta['page'], callback=self.__page_parse, meta={'cookiejar': response.meta['cookiejar'], 'WebNode': response.meta['WebNode'], 'page': (response.meta['page'] + 1)})
