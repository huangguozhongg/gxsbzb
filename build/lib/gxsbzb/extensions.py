from scrapy import signals
from scrapy.exceptions import NotConfigured
from .items import *
from .utile.DBUtile import *

# 关闭Spider(URL)
class SpiderUrlFilter(object):

    def __init__(self, MYSQL_HOST,MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD,MYSQL_DB):
        # 连接数据库
        self.__mysql_client = MysqlUtile(MYSQL_HOST,MYSQL_PORT,MYSQL_USER,MYSQL_PASSWORD,MYSQL_DB)
        # 最新记录
        self.__lastConfig = {}

    @classmethod
    def from_crawler(cls, crawler):
        # 首先检查一下是否存在响应的配置，如果不存在抛出NotConfigured异常
        if not crawler.settings.getbool('CLOSESPIDER_ITEMURL'):
            raise NotConfigured
        # 初始化扩展实例
        ext = cls(  MYSQL_HOST = crawler.settings.get('MYSQL_HOST'),
                    MYSQL_PORT = crawler.settings.get('MYSQL_PORT'),
                    MYSQL_USER = crawler.settings.get('MYSQL_USER'),
                    MYSQL_PASSWORD = crawler.settings.get('MYSQL_PASSWORD'),
                    MYSQL_DB = crawler.settings.get('MYSQL_DB'))
        # 将扩展中的spider_opened,spider_closed和 item_scraped连接到响应信号处，进行触发。
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)
        # 扩展实例返回
        return ext


    def spider_opened(self, spider):
        print('———————————— Spider正在打开(附加URL判断(config)) ————————————')
        # 设置属性
        result = self.__mysql_client.fetch_all(tablename='config', columns='Url')
        setattr(spider, 'mysql_config', list(map(lambda x: x[0],result)))

    def spider_closed(self, spider):
        print('———————————— Spider正在关闭(附加URL判断(config)) ————————————')
        for item in self.__lastConfig.values():
            # 删除表数据
            self.__mysql_client.delete(tablename='config',where='Website="%s" and WebNode="%s"' % (item['Website'],item['WebNode']))
            # 插入数据库
            self.__mysql_client.insert_one(tablename='config',values=(item['Id'], item['IsValid'], item['CreateDate'], item['Title'], item['Url'], item['Time'], item['Website'], item['WebUrl'], item['WebTitle'], item['WebNode']))
        # 关闭数据库
        self.__mysql_client.close()

    def item_scraped(self, item, spider):
        print('———————————— Item正在处理(附加URL判断(config)) ————————————')
        # 最新记录
        if isinstance(item, gxykdx_Item):
            key = item['WebTitle']+ item['WebNode']
            if key not in self.__lastConfig:
                self.__lastConfig.update({key: item})

# 关闭Spider(URL)
class SCHEDULER_DUPEFILTER_URL(object):

    def __init__(self, MYSQL_HOST,MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD,MYSQL_DB):
        # 连接数据库
        self.__mysql_client = MysqlUtile(MYSQL_HOST,MYSQL_PORT,MYSQL_USER,MYSQL_PASSWORD,MYSQL_DB)
        # 最新记录
        self.__lastConfig = {}
        # 去重条件
        self.__dupefilter = {}

    @classmethod
    def from_crawler(cls, crawler):
        # 首先检查一下是否存在响应的配置，如果不存在抛出NotConfigured异常
        if not crawler.settings.getbool('SCHEDULER_DUPEFILTER_URL'):
            raise NotConfigured
        # 初始化扩展实例
        ext = cls(  MYSQL_HOST = crawler.settings.get('MYSQL_HOST'),
                    MYSQL_PORT = crawler.settings.get('MYSQL_PORT'),
                    MYSQL_USER = crawler.settings.get('MYSQL_USER'),
                    MYSQL_PASSWORD = crawler.settings.get('MYSQL_PASSWORD'),
                    MYSQL_DB = crawler.settings.get('MYSQL_DB'))
        # 将扩展中的spider_opened,spider_closed和 item_scraped连接到响应信号处，进行触发。
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)
        # 扩展实例返回
        return ext

    def spider_opened(self, spider):
        print('———————————— Spider正在打开(关闭Spider(URL)) ————————————')
        if hasattr(spider,'dupefilter'):
            # 获取DUPEFILTER
            self.__dupefilter = spider.dupefilter
            # 设置DUPEFILTER_URL
            results = self.__mysql_client.fetch_all(tablename=self.__dupefilter.get('tablename','config'), columns='Url')
            setattr(spider, 'DUPEFILTER_URL', list(map(lambda x: x[0],results)))

    def spider_closed(self, spider):
        print('———————————— Spider正在关闭(关闭Spider(URL)) ————————————')
        for item in self.__lastConfig.values():
            # SQL
            colsL = ''
            colsR = []
            for column in self.__dupefilter.get('columns', 'WebTitle,WebNode').split(','):
                if colsL == '':
                    colsL = column + '="%s"'
                else:
                    colsL = colsL + ' and ' + column + '="%s"'
                colsR.append(item[column])
            else:
                colsL = colsL
                colsR = tuple(colsR)
                # 删除表数据
                self.__mysql_client.delete(tablename=self.__dupefilter.get('tablename', 'config'), where=colsL % colsR)
                # 插入数据库
                self.__mysql_client.insert_one(tablename=self.__dupefilter.get('tablename', 'config'), values=tuple(dict(item).values()))
        # 关闭数据库
        self.__mysql_client.close()

    def item_scraped(self, item, spider):
        print('———————————— Item正在处理(关闭Spider(URL)) ————————————')
        if self.__dupefilter and (isinstance(item, gxykdx_Item) or isinstance(item, contractcon_onelevel_Item)):
            # 键
            key = ''
            for column in self.__dupefilter.get('columns', 'WebTitle,WebNode').split(','):
                key = key + item[column]
            if key not in self.__lastConfig:
                self.__lastConfig.update({key: item})

#  更新查询数据库
class SCHEDULER_QUEUE_URL(object):

    def __init__(self, MYSQL_HOST,MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD,MYSQL_DB):
        # 连接数据库
        self.__mysql_client = MysqlUtile(MYSQL_HOST,MYSQL_PORT,MYSQL_USER,MYSQL_PASSWORD,MYSQL_DB)
        # 查询条件
        self.__queue = {}

    @classmethod
    def from_crawler(cls, crawler):
        # 首先检查一下是否存在响应的配置，如果不存在抛出NotConfigured异常
        if not crawler.settings.getbool('SCHEDULER_QUEUE_URL'):
            raise NotConfigured
        # 初始化扩展实例
        ext = cls(  MYSQL_HOST = crawler.settings.get('MYSQL_HOST'),
                    MYSQL_PORT = crawler.settings.get('MYSQL_PORT'),
                    MYSQL_USER = crawler.settings.get('MYSQL_USER'),
                    MYSQL_PASSWORD = crawler.settings.get('MYSQL_PASSWORD'),
                    MYSQL_DB = crawler.settings.get('MYSQL_DB'))
        # 将扩展中的spider_opened,spider_closed和 item_scraped连接到响应信号处，进行触发。
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)
        # 扩展实例返回
        return ext

    def spider_opened(self, spider):
        print('———————————— Spider正在打开(更新查询数据库) ————————————')
        if hasattr(spider,'queue'):
            # 获取select
            self.__queue = spider.queue
            results = self.__mysql_client.fetch_all(tablename= self.__queue.get('tablename', 'gxykdx'), columns=self.__queue.get('columns', 'Id,Url'), where=self.__queue.get('where', 'TRUE'), orderby=self.__queue.get('orderby', 'Time ASC'))
            # 设置SQUEUE_URL
            if results != []:
                setattr(spider, 'QUEUE_URL', list(results))

    def spider_closed(self, spider):
        print('———————————— Spider正在关闭(更新查询数据库) ————————————')
        # 关闭数据库
        self.__mysql_client.close()

    def item_scraped(self, item, spider):
        print('———————————— Item正在处理(更新查询数据库) ————————————')
        # 更新数据库
        if self.__queue and (isinstance(item, resultannouncement_Item) or isinstance(item, contract_twolevel_Item)):
            self.__mysql_client.update(tablename=self.__queue.get('tablename', 'gxykdx'), set='IsValid=2', where='Id="%s"' % item['Id'])