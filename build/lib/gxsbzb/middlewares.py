# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals, Item
from scrapy.exceptions import CloseSpider,NotConfigured
import  random, datetime, re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from gxsbzb.items import *
from gxsbzb.utile.DBUtile import *



class GxsbzbSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class GxsbzbDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


# 产生随机User-Agent
class randomUserAent(object):

    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        # 从Settings中加载USER_AGENTS的值
        return  cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self,request,spider):
        # 在process_request中设置User-Agent的值
        request.headers.setdefault('User-Agent', random.choice(self.agents))


# 产生随机Proxy
class randomProxy(object):

    def __init__(self, iplist):
        self.iplist = iplist

    @classmethod
    def from_craler(cls, crawler):
        # 从Setings中加载IPLIST的值
        return cls(crawler.settings.getlist('IPLIST'))

    def process_reqest(self, reqeust, spider):
        proxy = random.choice(self.iplist)
        reqeust.meta['proxy'] = proxy


# 页面渲染Seleninum
class seleniumJS(object):

    def process_request(self, request, spider):
        # 使用无头谷歌浏览器模式
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        # 指定谷歌浏览器路径
        self.driver = webdriver.Chrome(options=chrome_options, executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver')
        self.driver.get(request.url)
        time.sleep(1)
        html = self.driver.page_source
        self.driver.quit()
        return scrapy.http.HtmlResponse(url=request.url, body=html.encode('utf-8'), encoding='utf-8',request=request)

# 关闭spider(时间间隔)
class itemCloseSpider(object):

    def __init__(self, INTERVAL_DAY):
        self.INTERVAL_DAY = INTERVAL_DAY

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        INTERVAL_DAY = crawler.settings.getbool('CLOSESPIDER_ITEMDAY')
        # 首先检查一下是否存在响应的配置，如果不存在抛出NotConfigured异常
        if not INTERVAL_DAY:
            raise NotConfigured
        return cls(INTERVAL_DAY)

    def process_spider_output(self, response, result, spider):
            for r in result:
                if self.INTERVAL_DAY not in [None, 0]:
                    if isinstance(r, Item):
                        print(r['tn_date'])
                        if self.__isNotInterval( r['tn_date'], self.INTERVAL_DAY):
                            raise  CloseSpider('爬取Item超过指定时间限定！')
                yield r

    def __isNotInterval(self, date_str, interval) -> bool:
        nowtime = datetime.datetime.today()
        p = re.compile(r'\d{2,}[-\./\\:\s]?\d{2}[-\.:/\\\s]?\d{2}')
        date_str = p.search(date_str).group(0)
        date_str = re.sub(r'\.|-|:|/|\\|\s', '', date_str)
        try:
            tn_date = datetime.datetime.strptime(date_str, '%Y%m%d')
            if (nowtime - tn_date).days > interval:
                return True
        except Exception as e:
            print(e)
            return  False
        return False
