# -*- coding: utf-8 -*-
import  json, copy
from scrapy import *
from ..items import *
from ..utile.HTTPUtile import *

## 广西贵港市政府采购网 ##

# 重要通知,采购公告,政策法规
class ggszfcgw_zcz_Spider(Spider):

    # 爬虫名
    name = 'ggszfcgw_zcz'
    # 网站标题
    __WebTitle = '广西贵港市政府采购网'
    # 网站地址
    __WebUrl = 'http://zfcg.czj.gxgg.gov.cn/home.html'
    # 网站节点
    __WebNodes = [
                  '采购资讯重要通知',

                  '采购公告采购项目公告公开招标公告',
                  '采购公告采购项目公告竞争性谈判公告',
                  '采购公告采购项目公告询价公告',
                  '采购公告采购项目公告竞争性磋商公告',

                  ' 政策法规 > 市县文件'
                  ]
    # 网站定位
    __Websites = __WebNodes
    # 网站节点参数
    __WebNodeParams = [
                       "*6ggcgnoticenews6*",

                       "*6zcyannouncement30016*",
                       "*6zcyannouncement30026*",
                       "*6zcyannouncement30036*",
                       "*6zcyannouncement30116*",

                       "*6ggcgpolicieandrgulation6*"
                       ]
    # post 请求头
    __post_headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            # 'Content-Length': '460',
            'Content-Type': 'application/json',
            'Cookie': 'acw_tc=76b20ff215755074736356344e247ef19d19e73bf2f54df6ff64765446516d; _zcy_log_client_uuid=457b3940-16fa-11ea-b829-c18177d4af45; _dg_playback.bbc15f7dfd2de351.45a1=1; _dg_abtestInfo.bbc15f7dfd2de351.45a1=1; _dg_check.bbc15f7dfd2de351.45a1=-1; _dg_id.bbc15f7dfd2de351.45a1=dade6b948402bd41%7C%7C%7C1575507474%7C%7C%7C1%7C%7C%7C1575507537%7C%7C%7C1575507519%7C%7C%7C%7C%7C%7Cc22dcef7984ffb62%7C%7C%7C%7C%7C%7C%7C%7C%7C1%7C%7C%7Cundefined',
            'Host': 'zfcg.czj.gxgg.gov.cn',
            'Origin': 'http://zfcg.czj.gxgg.gov.cn',
            'Referer': 'http://zfcg.czj.gxgg.gov.cn/ggcgBuyNews/ggcgNoticeNews/index.html?utm=sites_group_front.5b1ba037.0.0.092e6fb0167e11eab1195373a39ad24e',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
            }
    # Post 请求参数
    __post_params ={"from":0,"size":"15","query":{"bool":{"must":[{"term":{"siteId":{"value":"29","boost":1}}},{"wildcard":{"path":{"wildcard":"*6ggcgnoticenews6*","boost":1}}}],"adjust_pure_negative":True,"boost":1,"should":[]}},"sort":[{"publishDate":{"order":"desc"}},{"_id":{"order":"desc"}}],"_source":{"includes":["title","articleId","siteId","cover","url","pathName","publishDate","attachmentUrl","districtName","gpCatalogName","author","remark"],"excludes":["content"]}}


    # 第一个Request请求
    def start_requests(self):
        return  [Request(self.__WebUrl, callback=self.parse, method='GET', meta={'cookiejar':1})]

    # 第一个响应
    def parse(self, response):
        # 请求队列
        for WebNode in range(len(self.__WebNodes)):
            body = copy.deepcopy(self.__post_params)
            body["query"]["bool"]["must"][1]["wildcard"]["path"].update({"wildcard":self.__WebNodeParams[WebNode]})
            yield Request('http://zfcg.czj.gxgg.gov.cn/es-articles/es-article/_search', callback=self.__page_parse, method='POST',headers=self.__post_headers, body=json.dumps(body), meta={'cookiejar': response.meta['cookiejar'], 'WebNode': WebNode, 'page':1})

    # 页面解析
    def __page_parse(self, response):
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
            pass
            # 提交Request跟进
            body = copy.deepcopy(self.__post_params)
            body["query"]["bool"]["must"][1]["wildcard"]["path"].update({"wildcard":self.__WebNodeParams[response.meta['WebNode']]})
            body.update({'from': (response.meta['page'] * 15) })
            yield Request('http://zfcg.czj.gxgg.gov.cn/es-articles/es-article/_search', callback=self.__page_parse, method='POST',headers=self.__post_headers, body=json.dumps(body), meta={'cookiejar': response.meta['cookiejar'], 'WebNode': response.meta['WebNode'], 'page': (response.meta['page'] + 1)})
