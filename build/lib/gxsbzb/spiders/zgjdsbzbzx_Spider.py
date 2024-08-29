# -*- coding: utf-8 -*-
from scrapy import *
from ..items import *
from ..utile.HTTPUtile import *

## 6.中国机电设备招标中心##

# 通知公告
class zgjdsbzbzx_tzgg_Spider(Spider):

    # 爬虫名
    name = 'zgjdsbzbzx_tzgg'
    # 网站标题
    __WebTitle = '中国机电设备招标中心'
    # 网站地址
    __WebUrl = 'https://www.miitcntc.org.cn/nav/zhong-xin-shou-ye-1.html'
    # 网站节点
    __WebNodes = ['通知公告']
    # 网站定位
    __Websites = __WebNodes
    # 网站节点地址
    __WebNodeUrls = [ 'https://www.miitcntc.org.cn/news/gong-gao-tong-zhi-42']

    # 第一个Rqeust请求
    def start_requests(self):
        return [Request(self.__WebNodeUrls[0], callback=self.parse)]

    # 第一个Request响应
    def parse(self, response):
        try:
            # 首先抽取所有的文章
            papers = response.xpath('//div[@class="e_box e_box-000 p_news"]//div[@class="e_box e_ListBox-001 p_articles"]')
            # 从每篇文章中抽取数据
            for paper in papers:
                # 标题
                Title = paper.xpath('./div[@class="js_coverUrlTitle item_hide"]/text()').extract()[0]
                # url
                Url = response.urljoin(paper.xpath('./a[@class="e_link e_link-000 p_LinkA"]/@href').extract()[0])
                # 日期
                Time = paper.xpath('.//div[@class="e_box e_box-000 p_assist"]//div[@class="font"]/text()').extract()[0]
                # 保持到Item（编号，有效性，创建时间，标题，链接，日期，模块，网址地址，网址标题，网站节点，爬取次数）
                item = gxykdx_Item(Id=str(uuid.uuid1()), IsValid=1, CreateDate='DEFAULT', Title=Title, Url=Url, Time=Time, Website=self.__Websites[0], WebUrl=self.__WebUrl, WebTitle=self.__WebTitle, WebNode=self.__WebNodes[0], Count=0)
                # 提交Item，判断URL是否重复
                if hasattr(self, 'mysql_config'):
                    if Url in getattr(self, 'mysql_config'):
                        raise Exception('URL重复，抛出异常！')
                yield item
        except Exception as e:
            print(e)