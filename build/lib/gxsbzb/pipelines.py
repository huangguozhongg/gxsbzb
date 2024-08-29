# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from .items import *
from .utile.DBUtile import *

class GxsbzbPipeline(object):
    def process_item(self, item, spider):
        return item

# 数据持久化
class gxykdx_Pipeline(object):

    # host:主机名, port:端口号, user:用户名, password:用户密码, db:数据库名
    def __init__(self, MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB):
        # 开启数据库连接
        self.mysql_host = MYSQL_HOST
        self.mysql_port = MYSQL_PORT
        self.mysql_user = MYSQL_USER
        self.mysql_password = MYSQL_PASSWORD
        self.mysql_db = MYSQL_DB

    @classmethod
    def  from_crawler(cls, crawler, *args, **kwargs):
        return cls(
            MYSQL_HOST = crawler.settings.get('MYSQL_HOST'),
            MYSQL_PORT =crawler.settings.get('MYSQL_PORT'),
            MYSQL_USER = crawler.settings.get('MYSQL_USER'),
            MYSQL_PASSWORD = crawler.settings.get('MYSQL_PASSWORD'),
            MYSQL_DB = crawler.settings.get('MYSQL_DB')
        )

    def open_spider(self,spider):
        # 开启数据库连接
        self.mysql_client = MysqlUtile(host=self.mysql_host, port=self.mysql_port, user=self.mysql_user, password=self.mysql_password, db=self.mysql_db)

    def close_spider(self,spider):
        # 关闭数据库连接
        self.mysql_client.close()

    def process_item(self, item, spider):
        # 标题表一级表
        if isinstance(item, gxykdx_Item):
            tmp_itme = self.__data_processing(item)
            # 输出数据库（编号，有效性，创建时间，标题，链接，日期，模块，网址地址，网址标题，网站节点，爬取次数）
            self.mysql_client.insert_one(tablename='gxykdx', values=(tmp_itme['Id'], tmp_itme['IsValid'], tmp_itme['CreateDate'], tmp_itme['Title'], tmp_itme['Url'], tmp_itme['Time'], tmp_itme['Website'], tmp_itme['WebUrl'], tmp_itme['WebTitle'], tmp_itme['WebNode'], tmp_itme['Count']))
            return item
        # 结果公告表二级表
        elif isinstance(item, resultannouncement_Item):
            tmp_itme = self.__data_processing(item)
            # 输出数据库（编号，有效性，创建时间，标题，链接，日期，模块，网址地址，网址标题，网站节点，爬取次数）
            self.mysql_client.insert_one(tablename='resultannouncement', values=(tmp_itme['Id'], tmp_itme['IsValid'], tmp_itme['CreateDate'], tmp_itme['WebName'], tmp_itme['Area'], tmp_itme['ProjectType'], tmp_itme['ProjectName'], tmp_itme['ProjectCode'], tmp_itme['CJ_CompanyName'], tmp_itme['CJ_Money'], tmp_itme['CG_CompanyName'], tmp_itme['ZBDL_CompanyName'], tmp_itme['Url'], tmp_itme['Content']))
            return item
        # 合同公告一级表
        elif isinstance(item, contractcon_onelevel_Item):
            tmp_itme = self.__data_processing(item)
            # 输出数据库（编号，有效性，创建时间，标题，链接，日期，模块，所属地区，爬取次数）
            self.mysql_client.insert_one(tablename='contractcon_onelevel', values=(tmp_itme['Id'], tmp_itme['IsValid'], tmp_itme['CreateDate'], tmp_itme['Title'], tmp_itme['Url'],tmp_itme['Time'], tmp_itme['Website'], tmp_itme['Area'], tmp_itme['Count']))
            return item
        #  合同公告二级表
        if isinstance(item, contract_twolevel_Item):
            tmp_itme = self.__data_processing(item)
            # 输出数据库（编号，有效性，创建时间，合同标题，合同链接，采购人名称，供应商名称，代理机构名称，采购项目名称, 采购项目编号, 合同编号, 合同金额, 预算金额, 合同发布时间）
            self.mysql_client.insert_one(tablename='contract_twolevel', values=(tmp_itme['Id'], tmp_itme['IsValid'], tmp_itme['CreateDate'], tmp_itme['ContractTitle'],tmp_itme['ContractUrl'], tmp_itme['Purchaser'], tmp_itme['Supplier'], tmp_itme['Agency_Name'],tmp_itme['ProjectName'], tmp_itme['ProjectCode'], tmp_itme['ContractCode'], tmp_itme['ContractPrice'], tmp_itme['BudgetPrice'], tmp_itme['ReleaseTime']))
            return item
        else:
             raise DropItem("Mising title in %s" % item)

    def __data_processing(self,item):
        tmp_dict = dict(item)
        for key,value in tmp_dict.items():
            if type(value) == str:
                tmp_dict.update({key:value.strip()})
        return tmp_dict



