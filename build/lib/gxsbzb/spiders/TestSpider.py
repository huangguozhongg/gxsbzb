# -*- coding: utf-8 -*-
import  json
from scrapy import *
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup
from lxml import etree
from ..items import *
from ..utile.HTTPUtile import *

class TestSpider(Spider):
    # 爬虫名称
    name = 'Test'
    # 查询条件
    select = {'tablename': 'gxykdx', 'columns':'Id,Url', 'where': 'WebNode="信息公告结果公告"'}
    # 结果信息

    # 第一个请求
    def start_requests(self):
        return [Request(url='http://www.baidu.com', callback=self.parse)]

    # 第一个响应
    def parse(self, response):
        # 获取数据库URL
        self.__QueueUrl = getattr(self, 'QUEUE_URL', [])
        print(self.__QueueUrl[0])