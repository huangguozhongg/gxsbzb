# -*- coding: utf-8 -*-
import  json
from scrapy import *
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup
from lxml import etree
from ..items import *
from ..utile.HTTPUtile import *

## 广西壮族自治区政府采购网 ##

# 信息公告
class gxzfcgw_xxgg_Spider(Spider):

    # 爬虫名
    name = 'gxzfcgw_xxgg'
    # 网站标题
    __WebTitle = '广西壮族自治区政府采购网'
    # 网站地址
    __WebUrl = 'http://zfcg.gxzf.gov.cn/home.html'
    # 网站节点
    __WebNodes = [
                  '信息公告采购公告',
                  '信息公告结果公告',
                  '信息公告合同公告',
                  '信息公告更正公告',
                  '信息公告招标文件预公示',
                  '信息公告单一来源公示',
                  '信息公告电子卖场公告',
                  '信息公告其他公告'
                  ]
    # 网站定位
    __Websites = __WebNodes
    # 网站节点参数
    __WebNodeParams = [1, 2, 3, 4, 5, 6, 7, 9]
    # Post 请求头
    __post_headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Cookie': 'acw_tc=76b20fe315716486515978375e1622a94de5d3cce7d304eac4f89cc6fafe19',
        'Host': 'zfcg.gxzf.gov.cn',
        'Origin': 'http://zfcg.gxzf.gov.cn',
        'Referer': 'http://zfcg.gxzf.gov.cn/ZcyAnnouncement/ZcyAnnouncement1/index.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    # 第一个Request请求
    def start_requests(self):
        return  [Request('http://zfcg.gxzf.gov.cn/ZcyAnnouncement/index.html', callback=self.parse, method='GET', meta={'cookiejar':1})]

    # 第一个Response响应
    def parse(self, response):
        # 请求队列
        for WebNode in range(len(self.__WebNodes)):
            yield  self.__post_request(WebNode=WebNode, page=1, meta ={'cookiejar': response.meta['cookiejar'], 'WebNode': WebNode, 'page': 1})


    # 生成Request
    def __post_request(self, WebNode, page, meta):
        postData = {"categoryCode": "ZcyAnnouncement%d" %  self.__WebNodeParams[WebNode], "pageSize": "15", "pageNo": '%d' % page, 'utm': "sites_group_front.7370538b.0.0.1acc087009d311eaa89f852105e78a02"}
        return Request(url='http://zfcg.gxzf.gov.cn/front/search/category',
                       callback=self.__page_parse,
                       headers=self.__post_headers,
                       body=json.dumps(postData),
                       method='POST',
                       meta= meta)

    # 页面解析
    def __page_parse(self,response):
        try:
            # json解析
            papers = json.loads(response.text, encoding='utf-8')['hits']['hits']
            for paper in papers:
                # 标题
                Title = paper['_source']['title']
                # Url
                Url = response.urljoin(paper['_source']['url'])
                # 日期
                Time = datetime.fromtimestamp(int(str(paper['_source']['publishDate'])[:-3])).strftime('%Y-%m-%d %H:%M:%S')
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
            # 提交Request跟进
            yield self.__post_request(WebNode=response.meta['WebNode'], page=(response.meta['page'] + 1), meta ={'cookiejar': response.meta['cookiejar'], 'WebNode': response.meta['WebNode'],  'page': (response.meta['page'] + 1)})




# 政策法规
class gxzfcgw_zcfg_Spider(Spider):

    # 爬虫名
    name = 'gxzfcgw_zcfg'
    # 网站标题
    __WebTitle = '广西壮族自治区政府采购网'
    # 网站地址
    __WebUrl = 'http://zfcg.gxzf.gov.cn/home.html'
    # 网站节点
    __WebNodes = ['政策法规国家',
                  '政策法规自治区'
                  ]
    # 网站定位
    __Websites = __WebNodes
    # 网站节点参数
    __WebNodeParams = ['Country',
                       'AutonomousRegion'
                       ]
    # Post 请求头
    __post_headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Cookie': 'acw_tc=76b20fe315716486515978375e1622a94de5d3cce7d304eac4f89cc6fafe19',
        'Host': 'zfcg.gxzf.gov.cn',
        'Origin': 'http://zfcg.gxzf.gov.cn',
        'Referer': 'http://zfcg.gxzf.gov.cn/ZcyAnnouncement/ZcyAnnouncement1/index.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    # 第一个Request请求
    def start_requests(self):
        return [Request('http://zfcg.gxzf.gov.cn/AdministrativeRegulations/index.html', callback=self.parse, method='GET', meta={'cookiejar':1})]

    # 构造Request
    def __post_request(self, WebNode, page, meta):
        postData = {"utm":"sites_group_front.728a6b5e.0.0.e5c8c5a006bc11eaa0ccb139d12c2a22","categoryCode":self.__WebNodeParams[WebNode],"pageSize":"15","pageNo":"%d" % page}
        return Request(url='http://zfcg.gxzf.gov.cn/front/search/category',
                             callback=self.__page_parse,
                             headers=self.__post_headers,
                             body=json.dumps(postData),
                             method='POST',
                             meta=meta)

    # 第一个Response响应
    def parse(self, response):
        # 提交Request队列
        for WebNode in range(len(self.__WebNodes)):
            yield self.__post_request(WebNode=WebNode, page=1, meta={'cookiejar': response.meta['cookiejar'], 'WebNode': WebNode,'page':1})


    # 页面解析
    def __page_parse(self,response):
        try:
            # json解析
            papers = json.loads(response.text, encoding='utf-8')['hits']['hits']
            for paper in papers:
                # 标题
                Title = paper['_source']['title']
                # Url
                Url = response.urljoin(paper['_source']['url'])
                # 日期
                Time = datetime.fromtimestamp(int(str(paper['_source']['publishDate'])[:-3])).strftime('%Y-%m-%d %H:%M:%S')
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
            # 提交Request跟进
            yield self.__post_request(WebNode=response.meta['WebNode'], page=(response.meta['page'] + 1), meta={'cookiejar': response.meta['cookiejar'], 'WebNode': response.meta['WebNode'] , 'page': (response.meta['page'] +1)})



# 监督检查
class gxzfcgw_jdjc_Spider(Spider):

    # 爬虫名
    name = 'gxzfcgw_jdjc'
    # 网站标题
    __WebTitle = '广西壮族自治区政府采购网'
    # 网站地址
    __WebUrl = 'http://zfcg.gxzf.gov.cn/home.html'
    # 网站节点
    __WebNodes = ['监督检查投诉处理信息公告',
                  '监督检查行政处罚信息公告',
                  '监督检查质疑回复公告',
                  '监督检查行政处理信息公告'
                  ]
    # 网站定位
    __Websites = __WebNodes
    # 网站节点参数
    __WebNodeParams = ["ZcyAnnouncement7003",
                       "ZcyAnnouncement7004",
                       "ZcyAnnouncement1004",
                       "ZcyAnnouncement7005"
                       ]

    # Post 请求头
    __post_headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Cookie': 'acw_tc=76b20fe315716486515978375e1622a94de5d3cce7d304eac4f89cc6fafe19',
        'Host': 'zfcg.gxzf.gov.cn',
        'Origin': 'http://zfcg.gxzf.gov.cn',
        'Referer': 'http://zfcg.gxzf.gov.cn/ZcyAnnouncement/ZcyAnnouncement1/index.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    # 第一个Request请求
    def start_requests(self):
        return [Request('http://zfcg.gxzf.gov.cn/SupervisionAndInspection/index.html',callback=self.parse, method='GET', meta={'cookiejar':1})]

    # 构造Request
    def __post_request(self, WebNode, page, meta):
        postData = {"utm":"sites_group_front.314a189b.0.0.e51fccb006c211ea88229df00fa67c87","categoryCode":self.__WebNodeParams[WebNode],"pageSize":"15","pageNo":"%d" % page}
        return Request(url='http://zfcg.gxzf.gov.cn/front/search/category',
                             callback=self.__page_parse,
                             headers=self.__post_headers,
                             body=json.dumps(postData),
                             method='POST',
                             meta=meta)

    # 第一个Response响应
    def parse(self, response):
        # 提交Request队列
        for WebNode in range(len(self.__WebNodes)):
            yield self.__post_request(WebNode=WebNode, page=1, meta={'cookiejar': response.meta['cookiejar'], 'WebNode': WebNode,'page':1})

    ## 页面解析
    def __page_parse(self,response):
        try:
            # json解析
            papers = json.loads(response.text, encoding='utf-8')['hits']['hits']
            for paper in papers:
                # 标题
                Title = paper['_source']['title']
                #Url
                Url = response.urljoin(paper['_source']['url'])
                # 日期
                Time = datetime.fromtimestamp(int(str(paper['_source']['publishDate'])[:-3])).strftime('%Y-%m-%d %H:%M:%S')
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
            # 提交Request跟进
            yield self.__post_request(WebNode=response.meta['WebNode'], page=(response.meta['page'] + 1), meta={'cookiejar': response.meta['cookiejar'], 'WebNode': response.meta['WebNode'] , 'page': (response.meta['page'] +1)})



# 信息公告结果公告中标（成交）结果公告二级
class gxzfcgw_xxgg_jggg_zbjggg_second_Spider(Spider):
    # 爬虫名称
    name = 'gxzfcgw_xxgg_jggg_zbjggg_second'
    # 查询条件
    queue = {'tablename': 'gxykdx', 'columns':'Id,Url', 'where': 'Website="广西政府采购结果公告"'}
    # 网站标题
    __WebTitle = '广西壮族自治区政府采购网'
    # 网站地址
    __WebUrl = 'http://zfcg.gxzf.gov.cn/home.html'

    # 第一个请求
    def start_requests(self):
        return [Request(self.__WebUrl, callback=self.queue_url, method='GET', meta={'cookiejar':1})]

    # 第一个响应
    def queue_url(self, response):
        # 获取数据库URL
        self.__QueueUrl = getattr(self, 'QUEUE_URL', [])
        # 判断是否有值
        if self.__QueueUrl:
            # 取出一条记录
            record = self.__QueueUrl.pop()
            # 提交请求
            yield Request(record[1], callback=self.parse, meta={'cookiejar':response.meta['cookiejar'], 'Id': record[0]})

    # 页面解析
    def parse(self, response):
        try:
            # Json解析
            papers = json.loads(response.xpath('//input[@name="articleDetail"]/@value').extract()[0], encoding='utf-8')
            # 判断是否
            if papers['categories'][0]['name'] == '中标（成交）结果公告':
                # html标准化
                html = etree.tostring(etree.HTML(papers['content']))
                HP = HtmlResponse(url=response.url, body=html, encoding='utf-8', request=response.request)
                # 创建填充器
                I = ItemLoader(item=resultannouncement_Item(), response=HP)
                # 编号
                I.add_value('Id', response.meta['Id'])
                # 是否有效
                I.add_value('IsValid', 1)
                # 创建时间
                I.add_value('CreateDate', 'DEFAULT')
                # 网站名称
                I.add_value('WebName', self.__WebTitle)
                # 区域
                I.add_value('Area', json.loads(papers['announcementJson'])['districtName'])
                # 项目类型
                I.add_value('ProjectType' , json.loads(papers['announcementJson'])['gpCatalogName'])
                # 项目名称
                I.add_value('ProjectName', json.loads(papers['announcementJson'])['projectName'])
                # 项目编号
                I.add_value('ProjectCode', papers['projectCode'])
                # 成交人名称
                I.add_xpath('CJ_CompanyName', '/html/body/p[8]/span[3]/span/text()')
                I.add_xpath('CJ_CompanyName', '/html/body/p[11]/span[2]/span/text()')
                I.add_xpath('CJ_CompanyName', '/html/body/p[11]/span/span/text()')
                I.add_xpath('CJ_CompanyName', '/html/body/p[14]/span[2]/text()')
                I.add_xpath('CJ_CompanyName', '/html/body/p[14]/text()')
                I.add_xpath('CJ_CompanyName', '/html/body/p[16]/span/span/text()')
                I.add_xpath('CJ_CompanyName', '/html/body/p[17]/span[3]/span/text()')
                I.add_xpath('CJ_CompanyName', '/html/body/table[1]/tbody/tr[2]/td[9]/text()')
                I.add_xpath('CJ_CompanyName', '/html/body/table[2]/tbody/tr[2]/td[1]/p/span/text()')
                I.add_xpath('CJ_CompanyName', '/html/body/table/tbody/tr[8]/td[2]/p/span/text()')
                I.add_xpath('CJ_CompanyName', '/html/body/table/tbody/tr[9]/td[2]/p/span/text()')
                I.add_xpath('CJ_CompanyName', '/html/body/ol[2]/li[3]/p[2]/span[5]/span/span/text()')
                I.add_value('CJ_CompanyName', 'NULL')
                # 成交金额
                I.add_xpath('CJ_Money', '/html/body/p[13]/span/text()')
                I.add_xpath('CJ_Money', '/html/body/p[13]/span[2]/text()')
                I.add_xpath('CJ_Money', '/html/body/p[15]/text()')
                I.add_xpath('CJ_Money', '/html/body/p[18]/span[5]/text()')
                I.add_xpath('CJ_Money', '/html/body/p[37]/span[3]/text()')
                I.add_xpath('CJ_Money', '/html/body/table[1]/tbody/tr[2]/td[8]/text()')
                I.add_xpath('CJ_Money', '/html/body/table[2]/tbody/tr[2]/td[3]/p[2]/span/text()')
                I.add_xpath('CJ_Money', '/html/body/table[2]/tbody/tr[2]/td[5]/p/span/text()')
                I.add_xpath('CJ_Money', '/html/body/table/tbody/tr[2]/td[4]/p/span[1]/text()')
                I.add_xpath('CJ_Money', '/html/body/table/tbody/tr[9]/td[2]/p/span[2]/text()')
                I.add_xpath('CJ_Money', '/html/body/table/tbody/tr[10]/td[2]/p/span/text()')
                I.add_xpath('CJ_Money', '/html/body/ol[2]/li[3]/p[4]/span[5]/span/span/text()')
                I.add_value('CJ_Money', 'NULL')
                # 采购单位
                I.add_value('CG_CompanyName', papers['author'])
                I.add_xpath('CG_CompanyName', '/html/body/p[20]/span[2]/text()')
                I.add_value('CG_CompanyName', 'NULL')
                # 采购代理机构
                I.add_value('ZBDL_CompanyName', json.loads(papers['announcementJson']).get('agencyOrgName', None))
                I.add_xpath('ZBDL_CompanyName', '/html/body/p[25]/span/text()')
                I.add_value('ZBDL_CompanyName', 'NULL')
                # 附件链接
                I.add_xpath('Url', '/html/body/ul/li/p[1]/a/@href')
                I.add_value('Url', 'NULL')
                # 文本
                I.add_value('Content', papers['content'])
                # 提交Item
                yield I.load_item()
            else:
                print('非中标（成交）结果公告！')
        except Exception as e:
            print(e)
        else:
            # 判断是否有值
            if self.__QueueUrl:
                # 取出一条记录
                record = self.__QueueUrl.pop()
                # 提交请求
                yield Request(record[1], callback=self.parse, meta={'cookiejar': response.meta['cookiejar'], 'Id': record[0]})


# 信息公告合同公告一级
class gxzfcgw_xxgg_htgg_first_Spider(Spider):

    # 爬虫名
    name = 'gxzfcgw_xxgg_htgg_first'
    # 去重规则
    dupefilter = {'tablename': 'contractcon_config', 'columns':'Website'}
    # 网站标题
    __WebTitle = '广西壮族自治区政府采购网'
    # 网站地址
    __WebUrl = 'http://zfcg.gxzf.gov.cn/home.html'
    # 网站定位
    __Website = '信息公告合同公告'
    # Post 请求头
    __post_headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Cookie': 'acw_tc=76b20fe315716486515978375e1622a94de5d3cce7d304eac4f89cc6fafe19',
        'Host': 'zfcg.gxzf.gov.cn',
        'Origin': 'http://zfcg.gxzf.gov.cn',
        'Referer': 'http://zfcg.gxzf.gov.cn/ZcyAnnouncement/ZcyAnnouncement1/index.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    # 第一个Request请求
    def start_requests(self):
        return  [Request(self.__WebUrl, callback=self.parse, method='GET', meta={'cookiejar':1})]

    # 第一个Response响应
    def parse(self, response):
        yield  self.__post_request(page=1, meta ={'cookiejar': response.meta['cookiejar'], 'page': 1})

    # 生成Request
    def __post_request(self, page, meta):
        postData = {"utm":"sites_group_front.7c640a24.0.0.d344f740207b11ea8f9a6bd2cf62cb53", "categoryCode":"ZcyAnnouncement3010", "pageSize":"15", "pageNo":"%d" % page}
        return Request(url='http://zfcg.gxzf.gov.cn/front/search/category', callback=self.__page_parse, method='POST', headers=self.__post_headers, body=json.dumps(postData), meta= meta)

    # 页面解析
    def __page_parse(self,response):
        try:
            # json解析
            papers = json.loads(response.text, encoding='utf-8')['hits']['hits']
            for paper in papers:
                # 标题
                Title = paper['_source']['title']
                # Url
                Url = response.urljoin(paper['_source']['url'])
                # 日期
                Time = datetime.fromtimestamp(int(str(paper['_source']['publishDate'])[:-3])).strftime('%Y-%m-%d %H:%M:%S')
                # 区域
                Area = paper['_source']['districtName']
                # 保持到Item（编号，有效性，创建时间，标题，链接，日期，模块，所属地区，爬取次数）
                item = contractcon_onelevel_Item(Id=str(uuid.uuid1()), IsValid=1, CreateDate='DEFAULT', Title=Title, Url=Url, Time=Time, Website=self.__Website, Area=Area, Count=0)
                # 提交Item，判断URL是否重复
                if hasattr(self, 'DUPEFILTER_URL'):
                    if Url in getattr(self, 'DUPEFILTER_URL'):
                        raise Exception('URL重复，抛出异常！')
                yield item
        except Exception as e:
            print(e)
        else:
            # 提交Request跟进
            yield self.__post_request(page=(response.meta['page'] + 1), meta ={'cookiejar': response.meta['cookiejar'], 'page': (response.meta['page'] + 1)})


# 信息公告合同公告二级
class gxzfcgw_xxgg_htgg_second_Spider(Spider):

    # 爬虫名称
    name = 'gxzfcgw_xxgg_htgg_second'
    # 查询条件
    queue = {'tablename': 'contractcon_onelevel', 'columns':'Id,Url','orderby':'Time DESC'}
    # 网站标题
    __WebTitle = '广西壮族自治区政府采购网'
    # 网站地址
    __WebUrl = 'http://zfcg.gxzf.gov.cn/home.html'

    # 第一个请求
    def start_requests(self):
        return [Request(self.__WebUrl, callback=self.queue_url, method='GET', meta={'cookiejar':1})]

    # 第一个响应
    def queue_url(self, response):
        # 获取数据库URL
        self.__QueueUrl = getattr(self, 'QUEUE_URL', [])
        # 判断是否有值
        if self.__QueueUrl:
            # 取出一条记录
            record = self.__QueueUrl.pop()
            # 提交请求
            yield Request(record[1], callback=self.parse, meta={'cookiejar':response.meta['cookiejar'], 'Id': record[0]})

    # 第一个响应
    def parse(self, response):
        try:
            # Json解析
            papers = json.loads(response.xpath('//input[@name="articleDetail"]/@value').extract()[0], encoding='utf-8')
            # html标准化
            html = etree.tostring(etree.HTML(papers['content']))
            HP = HtmlResponse(url=response.url, body=html, encoding='utf-8', request=response.request)
            # 创建填充器
            I = ItemLoader(item=contract_twolevel_Item(), response=HP)
            # 编号
            I.add_value('Id', response.meta['Id'])
            # 是否有效
            I.add_value('IsValid', 1)
            # 创建时间
            I.add_value('CreateDate', 'DEFAULT')
            # 合同标题
            I.add_value('ContractTitle', papers['title'])
            # 合同链接
            I.add_xpath('ContractUrl', '/html/body/ul/li/p[1]/a/@href')
            I.add_xpath('ContractUrl', '/html/body/ul/li/p/a/@href')
            I.add_value('ContractUrl', 'NULL')
            # 采购人名称
            I.add_value('Purchaser', papers['author'])
            # 供应商名称
            I.add_xpath('Supplier', '/html/body/p[1]/span/span/span/text()')
            I.add_xpath('Supplier', '/html/body/p[3]/span/span/span/text()')
            I.add_xpath('Supplier', '/html/body/p[4]/span/span/span/text()')
            I.add_xpath('Supplier', '/html/body/p[2]/span/span/text()')
            I.add_xpath('Supplier', '/html/body/table/tbody/tr[7]/td[2]/p/strong/span/text()')
            I.add_xpath('Supplier', '/html/body/table/tbody/tr[7]/td[2]/p/span/text()')
            I.add_xpath('Supplier', '/html/body/table/tbody/tr[9]/td[2]/p/span/text()')
            I.add_xpath('Supplier', '/html/body/table/tbody/tr[9]/td[2]/p/text()')
            I.add_xpath('Supplier', '//*[@id="template-center-mark"]/table/tbody/tr[7]/td[2]/p/span/text()')
            I.add_xpath('Supplier', '//*[@id="template-center-mark"]/p[3]/span/span/span/text()')
            I.add_value('Supplier', 'NULL')
            # 代理机构名称
            I.add_value('Agency_Name', json.loads(papers['announcementJson'])['agencyOrgName'])
            # 采购项目名称
            I.add_value('ProjectName', json.loads(papers['announcementJson'])['projectName'])
            # 采购项目编号
            I.add_value('ProjectCode', papers['projectCode'])
            # 合同编号
            I.add_xpath('ContractCode', '/html/body/p[4]/span/span/span/text()')
            I.add_xpath('ContractCode', '/html/body/p[5]/span/span/span/text()')
            I.add_xpath('ContractCode', '/html/body/p[5]/span/text()')
            I.add_xpath('ContractCode', '/html/body/p[6]/span/span/span/text()')
            I.add_xpath('ContractCode', '/html/body/table/tbody/tr[2]/td[2]/p/strong/span/text()')
            I.add_xpath('ContractCode', '/html/body/table/tbody/tr[2]/td[2]/p/span/text()')
            I.add_xpath('ContractCode', '/html/body/table/tbody/tr[2]/td[2]/text()')
            I.add_xpath('ContractCode', '/html/body/table/tbody/tr[3]/td[2]/p/span/text()')
            I.add_xpath('ContractCode', '//*[@id="template-center-mark"]/table/tbody/tr[2]/td[2]/p/span/text()')
            I.add_xpath('ContractCode', '//*[@id="template-center-mark"]/p[6]/span/span/span/text()')
            I.add_value('ContractCode', 'NULL')
            # 合同金额
            I.add_xpath('ContractPrice', '/html/body/table/tbody/tr[2]/td[7]/text()')
            I.add_xpath('ContractPrice', '/html/body/table/tbody/tr[2]/td[8]/p/span/text()')
            I.add_xpath('ContractPrice', '/html/body/table/tbody/tr[6]/td[2]/p/span/text()')
            I.add_xpath('ContractPrice', '/html/body/table/tbody/tr[7]/td[2]/p/span/text()')
            I.add_xpath('ContractPrice', '/html/body/table/tbody/tr[9]/td[2]/p/span[1]/text()')
            I.add_xpath('ContractPrice', '/html/body/table/tbody/tr[9]/td[2]/p/span[2]/text()')
            I.add_xpath('ContractPrice', '/html/body/table/tbody/tr[9]/td[2]/p/span/text()')
            I.add_xpath('ContractPrice', '/html/body/table/tbody/tr[9]/td[2]/p/span[2]/text()')
            I.add_xpath('ContractPrice', '//*[@id="template-center-mark"]/table/tbody/tr[2]/td[7]/text()')
            I.add_xpath('ContractPrice', '//*[@id="template-center-mark"]/table/tbody/tr[9]/td[2]/p/span/span[1]/text()')
            I.add_value('ContractPrice', 'NULL')
            # 预算金额
            I.add_xpath('BudgetPrice', '/html/body/table/tbody/tr[2]/td[7]/p/span/text()')
            I.add_xpath('BudgetPrice', '/html/body/table/tbody/tr[2]/td[8]/text()')
            I.add_xpath('BudgetPrice', '/html/body/table/tbody/tr[6]/td[2]/p/span/text()')
            I.add_xpath('BudgetPrice', '/html/body/table/tbody/tr[8]/td[2]/p/span[2]/text()')
            I.add_xpath('BudgetPrice', '/html/body/table/tbody/tr[8]/td[2]/p/span/text()')
            I.add_xpath('BudgetPrice', '/html/body/table/tbody/tr[8]/td[2]/p/span[3]/text()')
            I.add_xpath('BudgetPrice', '/html/body/table/tbody/tr[9]/td[2]/p/span/text()')
            I.add_xpath('BudgetPrice', '//*[@id="template-center-mark"]/table/tbody/tr[2]/td[8]/text()')
            I.add_xpath('BudgetPrice', '//*[@id="template-center-mark"]/table/tbody/tr[8]/td[2]/p/span/span[1]/text()')
            I.add_value('BudgetPrice', 'NULL')
            # 合同发布时间
            I.add_value('ReleaseTime', papers['publishDate'])
            # 提交Item
            yield I.load_item()
        except Exception as e:
            print(e)
        else:
            # 判断是否有值
            if self.__QueueUrl:
                # 取出一条记录
                record = self.__QueueUrl.pop()
                # 提交请求
                yield Request(record[1], callback=self.parse, meta={'cookiejar': response.meta['cookiejar'], 'Id': record[0]})
