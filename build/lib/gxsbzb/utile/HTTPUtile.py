import re, hashlib, os,json, random, uuid, time as t
from datetime import datetime, date ,time
from requests.sessions import Session
from scrapy import Request
from scrapy.http.cookies import CookieJar
from scrapy.dupefilters import  RFPDupeFilter
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from pybloom import  ScalableBloomFilter
from .DBUtile import MysqlUtile
from ..settings import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB

########## 通用请求头 ##########

class Headerler(object):
    # HTML
    __html ={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'
            }

    # FORM
    __from = {'Accept': 'text/html, */*; q=0.01',
              'Accept-Encoding': 'gzip, deflate',
              'Accept-Language': 'zh-CN,zh;q=0.9',
              'Cache-Control': 'max-age=0',
              'Connection': 'keep-alive',
              'Upgrade-Insecure-Requests': '1',
              'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
              'X-Requested-With': 'XMLHttpRequest'
              }

    # JSON
    __json = {'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
            }

    # 获取Headers  @type: 类型
    @ classmethod
    def get_headers(cls, type:str='html')->dict:
        if type.upper() == 'FORM':
            return  cls.__from
        elif type.upper() == 'JSON':
            return  cls.__json
        else:
            return cls.__html


########## Scrapy Cookie ##########

class  Cookieler(object):

    # 初始化函数 @response 响应对象，@url:请求url, @path:路径
    def __init__(self, response=None, url=None, path=None):
        # 实例化cookiejar对象
        self.__cookiejar = CookieJar()
        self.__real_cookie = {}
        if response:
            self.set_cookie_response(response)
        if url:
            self.set_cookie_selenium(url)
        if path:
            try:
                self.file = open('cookie.json', encoding='utf-8')
            except IOError as e:
                print(e)

    # 设置cookie(response) @response:响应对象
    def set_cookie_response(self, response):
        tmp_cookies = {}
        if isinstance(response,Session):
            tmp_cookies = response.cookies
        else:
            tmp_cookies = self.__cookiejar.extract_cookies(response, response.request)
        if tmp_cookies:
            for cookie in tmp_cookies:
                p = re.compile(r'<Cookie (.*?) for .*?>')
                cookies = re.findall(p, str(cookie))
                if '=' in cookies[0]:
                    cookies = (cookie.split('=', 1) for cookie in cookies)
                    tmp_dict = dict(cookies)
                    for item in tmp_dict:
                        self.__real_cookie[item] = tmp_dict[item]

    # 设置cookie(selenium) @url:请求url
    def set_cookie_selenium(self, url):
        options = webdriver.FirefoxOptions()
        options.add_argument('-headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Firefox(options=options, executable_path='C:\Program Files\Mozilla Firefox\geckodriver.exe')
        # driver.set_page_load_timeout(10)
        # driver.maximize_window()
        driver.get(url)
        for cookie in driver.get_cookies():
            self.__real_cookie.update({cookie['name']: cookie['value']})
        driver.quit()

    # 设置cookie（dict） @cookies:会话字典
    def set_cookie(self,cookies:dict):
        self.__real_cookie.update(cookies)

    # 获取cookie
    def get_cookie(self)->dict:
        return self.__real_cookie


########## URL过滤 ##########

class UrlFilter(RFPDupeFilter):

    # 初始化函数  @path:文件路径，@ismysql:是否数据库
    def __init__(self, path=None, ismysql=None):
        RFPDupeFilter.__init__(self,path)
        self.__urls_sbf = ScalableBloomFilter(mode=ScalableBloomFilter.SMALL_SET_GROWTH)
        if ismysql:
            # 开启数据库连接
            self.__mysql_client = MysqlUtile(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, password=MYSQL_PASSWORD, db=MYSQL_DB)
            # 查询数据库
            result = self.__mysql_client.fetch_all(tablename='title_node_information', columns='tn_url')
            if result:
                for row in result:
                    self.request_seen(Request(url=row[0]))
            # 关闭数据库
            self.__mysql_client.ColoseConnect()

    # 请求过滤查看 @reques: 请求对象
    def request_seen(self, request):
        fp = self.request_fingerprint(request)
        if fp in self.urls_sbf:
            return  True
        else:
            self.__urls_sbf.add(fp)
        if self.file:
            self.file.write(fp + os.linesep)


