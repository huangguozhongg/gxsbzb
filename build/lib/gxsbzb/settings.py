# -*- coding: utf-8 -*-

# Scrapy settings for gxsbzb project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'gxsbzb'

SPIDER_MODULES = ['gxsbzb.spiders']
NEWSPIDER_MODULE = 'gxsbzb.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'
USER_AGENTS = [ 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6',
                'Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5',
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
                'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
                'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)',
                'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20',
                'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6',
                'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
                'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)',
                'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
                'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)',
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
                'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.3 Mobile/14E277 Safari/603.1.30',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36']

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True
# COOKIES_DEBUG默认值为False,如果启用，Scrapy将记录所有在request(Cookie 请求头)发送的cookies及response接收到的cookies(Set-Cookie 接收头)
COOKIES_DEBUG = True

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = True

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   # 'gxsbzb.middlewares.GxsbzbSpiderMiddleware': 543,
    'gxsbzb.middlewares.itemCloseSpider': 544,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'gxsbzb.middlewares.GxsbzbDownloaderMiddleware': 543,
    'gxsbzb.middlewares.randomUserAent': 401
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
   # 'scrapy.extensions.telnet.TelnetConsole': None,
    'gxsbzb.extensions.SpiderUrlFilter': 501,
    'gxsbzb.extensions.SCHEDULER_DUPEFILTER_URL': 502,
    'gxsbzb.extensions.SCHEDULER_QUEUE_URL': 503
}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
#    'gxsbzb.pipelines.GxsbzbPipeline': 300,
#     'scrapy_redis.pipelines.RedisPipeline': 300,
    'gxsbzb.pipelines.gxykdx_Pipeline': 301,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

######### Connection Mysql Mesages ########
# 主机地址
MYSQL_HOST  =   '192.168.99.7'
# 端口号
MYSQL_PORT  =   3306
# 用户名
MYSQL_USER  =   'gxbid'
# 密码
MYSQL_PASSWORD  =   '123456'
# 数据库
MYSQL_DB   =   'test'

######## Scrapy Redis_Bloomfilter_Message ########
# # Redis的IP和端口及连接参数：
# REDIS_HOST = '127.0.0.1'
# REDIS_PORT = 6379
# # REDIS_URL = 'redis://user:pass@hostname:6379'
# REDIS_PARAMS = {'socket_timeout': 30,'socket_connect_timeout': 30,'retry_on_timeout': True,'encoding': "utf-8",}
#
# # 使用scrapy_redis的调度器：
# SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# # SCHEDULER = 'scrapy_redis_bloomfilter.scheduler.Scheduler'
# # 对保存到redis中的数据进行序列化，默认使用pickle
# SCHEDULER_SERIALIZER = "scrapy_redis.picklecompat"
#
# # Request任务序列化后存放在redis中的key
# SCHEDULER_QUEUE_KEY = '%(spider)s:requests'
# # Request默认使用优先级队列（默认），其他：PriorityQueue（有序集合），FifoQueue（列表）、LifoQueue（列表）
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"
# # SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
# # SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"
#
# # URL去重规则，在redis中保存时对应的key
# SCHEDULER_DUPEFILTER_KEY = '%(spider)s:dupefilter'
# # 去重规则对应处理的类，将任务request_fingerprint(request)得到的字符串放入去重队列
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# SCHEDULER_DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'
# # DUPEFILTER_CLASS = "scrapy_redis_bloomfilter.dupefilter.RFPDupeFilter"
#
# # Item对象持久化，爬虫yield 时执行RedisPipeline
# REDIS_ITEMS_KEY = '%(spider)s:items'
# # REDIS_ITEMS_SERIALIZER = "scrapy.utils.serialize.ScrapyJSONEncoder"
#
# # 获取起始URL时（可避免URL重复，需Sadd添加），去集合中获取还是去列表中获取？True，集合；False，列表
# REDIS_START_URLS_AS_SET = False
# # 编写爬虫时，起始URL从redis的Key中获取
# REDIS_START_URLS_KEY = '%(name)s:start_urls'
#
# # 是否在关闭时候保留原来的调度器和去重记录，True=保留，False=清空
# SCHEDULER_PERSIST = False
# # 是否在开始之前清空调度器和去重记录，True=清空，False=不清空
# SCHEDULER_FLUSH_ON_START = True
# # 去调度器中获取数据时，如果为空，最多等待时间
# SCHEDULER_IDLE_BEFORE_CLOSE = 10

# # 哈希函数的个数，默认为6
# BLOOMFILTER_HASH_NUMBER = 6
# # Bloom Filter的bit参数，默认30
# BLOOMFILTER_BIT = 30

########## Scrapy-crawlera ##########
# DOWNLOADER_MIDDLEWARES= {'scrapy_crawlera.CrawleraMiddleware': 300}
# CRAWLERA_ENABLED = True
# CRAWLERA_APIKEY = ''

########## ClossSpider  Condition ##########
# Day is Int type (0 by default)
# e.g. range(0, 365)
# CLOSESPIDER_ITEMURL = True
# CLOSESPIDER_ITEMDAY = 30
# CLOSESPIDER_TIMEOUT = 0
# CLOSESPIDER_PAGECOUNT = 5
# CLOSESPIDER_ITEMCOUNT = 0
# CLOSESPIDER_ERRORCOUNT = 0

########## 特殊配置 ##########
# SCHEDULER_DUPEFILTER_URL = True
# SCHEDULER_QUEUE_URL = True