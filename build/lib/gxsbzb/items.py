# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from scrapy import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst, Identity
from w3lib.url import canonicalize_url
import  re

class GxsbzbItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


# 自定义处理方法
class customFilter(object):

    # 是否是中文
    def is_Chinese(word):
        for ch in word:
            if '\u4e00' <= ch <= '\u9fff':
                return True
        return False

    # 是否含数字
    @classmethod
    def isHasNumber(cls, x):
        if re.findall('[0-9]+', x) and  (not re.findall('[①-⑨]', x)):
            return re.findall('\d{2,}\.\d{2,}|\d{1,}', x)[0]
        elif x == 'NULL':
            return 'NULL'
        return ''

    # 是否含中文
    @classmethod
    def isHasChinese(cls, x):
        if cls.is_Chinese(x):
            return x
        elif x == 'NULL':
            return 'NULL'
        return ''

    # 是否是全中文
    @classmethod
    def isAllChinese(cls, x):
        tmp1 = re.findall('[0-9a-zA-Z①-⑨]+', x)
        tmp2 = re.search('[:：]', x)
        if (not tmp1) and tmp2:
            if len(x) == tmp2.end():
                return ''
            else:
                return x[tmp2.end():]
        elif (not tmp1) and  (not tmp2):
            return  x
        elif x == 'NULL':
            return 'NULL'
        return ''

    # 是否属编号
    @classmethod
    def isIdCode(cls, x):
        tmp = re.findall('^[0-9a-zA-Z-]+', x)
        if tmp:
            return  tmp[0]
        elif x == 'NULL':
            return 'NULL'
        return ''

    # 是否属日期
    @classmethod
    def isDatetime(cls, x):
        if x !='NULL':
            p = re.compile(r'\d{2,4}([-\./\\:\s])?\d{2}([-\.:/\\\s])?\d{2}')
            x = p.search(x).group() if p.search(x) else False
            if x:
                return re.sub(r'\.|-|:|/|\\|\s', '-', x)
            else:
                return ''
        elif x == 'NULL':
            return  'NULL'


# 标题节点信息表
class gxykdx_Item(Item):
    # 编号
    Id = Field(input_processor=Identity(), output_processor=TakeFirst())
    # 是否有效
    IsValid = Field(input_processor=Identity(), output_processor=TakeFirst())
    # 创建时间
    CreateDate = Field(input_processor=Identity(), output_processor=TakeFirst())
    # 标题
    Title = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    # 链接
    Url = Field(input_processor=MapCompose(canonicalize_url), output_processor=TakeFirst())
    # 日期
    Time = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    # 模块
    Website = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    # 网站地址
    WebUrl = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    # 网站标题
    WebTitle = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    # 网站节点
    WebNode = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    # 爬取次数
    Count = Field(input_processor=Identity(), output_processor=TakeFirst())


# 广西政府采购网结果公告中标二级
class resultannouncement_Item(Item):
    # 编号
    Id = Field(input_processor=Identity(), output_processor=TakeFirst())
    # 是否有效
    IsValid = Field(input_processor=Identity(), output_processor=TakeFirst())
    # 创建时间
    CreateDate = Field(input_processor=Identity(), output_processor=TakeFirst())
    # 网站名称
    WebName = Field(input_processor=Identity(), output_processor=TakeFirst())
    # 区域
    Area = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    # 项目类型
    ProjectType = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    # 项目名称
    ProjectName = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    # 项目编号
    ProjectCode = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    # 成交人名称
    CJ_CompanyName = Field(input_processor=MapCompose(str.strip, customFilter.isAllChinese), output_processor=TakeFirst())
    # 成交金额
    CJ_Money = Field(input_processor=MapCompose(str.strip, customFilter.isHasNumber), output_processor=TakeFirst())
    # 采购单位
    CG_CompanyName = Field(input_processor=MapCompose(str.strip, customFilter.isAllChinese), output_processor=TakeFirst())
    # 采购代理机构
    ZBDL_CompanyName = Field(input_processor=MapCompose(str.strip, customFilter.isAllChinese), output_processor=TakeFirst())
    # 附件链接
    Url = Field(input_processor=MapCompose(canonicalize_url), output_processor=TakeFirst())
    # 文本
    Content = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())


# 广西政府采购网合同公告一级
class contractcon_onelevel_Item(Item):
    # 编号
    Id = Field(input_processor=Identity(), output_processor=TakeFirst())
    # 是否有效
    IsValid = Field(input_processor=Identity(), output_processor=TakeFirst())
    # 创建时间
    CreateDate = Field(input_processor=Identity(), output_processor=TakeFirst())
    # 标题
    Title = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    # 链接
    Url = Field(input_processor=MapCompose(canonicalize_url), output_processor=TakeFirst())
    # 日期
    Time = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    # 模块
    Website = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    # 所属区域
    Area = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    # 爬取次数
    Count = Field(input_processor=Identity(), output_processor=TakeFirst())


# 广西政府采购网合同公告二级
class contract_twolevel_Item(Item):
    # 编号
    Id = Field(input_processor=Identity(), output_processor=TakeFirst())
    # 是否有效
    IsValid = Field(input_processor=Identity(), output_processor=TakeFirst())
    # 创建时间
    CreateDate = Field(input_processor=Identity(), output_processor=TakeFirst())
    # 合同标题
    ContractTitle = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    # 合同链接
    ContractUrl = Field(input_processor=MapCompose(canonicalize_url), output_processor=TakeFirst())
    # 采购人名称
    Purchaser = Field(input_processor=MapCompose(str.strip, customFilter.isAllChinese), output_processor=TakeFirst())
    # 供应商名称
    Supplier = Field(input_processor=MapCompose(str.strip, customFilter.isAllChinese), output_processor=TakeFirst())
    # 代理机构名称
    Agency_Name = Field(input_processor=MapCompose(str.strip, customFilter.isAllChinese), output_processor=TakeFirst())
    # 采购项目名称
    ProjectName = Field(input_processor=MapCompose(str.strip, customFilter.isHasChinese), output_processor=TakeFirst())
    # 采购项目编号
    ProjectCode = Field(input_processor=MapCompose(str.strip, customFilter.isIdCode), output_processor=TakeFirst())
    # 合同编号
    ContractCode = Field(input_processor=MapCompose(str.strip, customFilter.isIdCode), output_processor=TakeFirst())
    # 合同金额
    ContractPrice = Field(input_processor=MapCompose(str.strip, customFilter.isHasNumber), output_processor=TakeFirst())
    # 预算金额
    BudgetPrice = Field(input_processor=MapCompose(str.strip, customFilter.isHasNumber), output_processor=TakeFirst())
    # 合同发布时间
    ReleaseTime = Field(input_processor=MapCompose(str.strip, customFilter.isDatetime), output_processor=TakeFirst())


