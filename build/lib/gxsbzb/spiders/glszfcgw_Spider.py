from scrapy import *
from ..items import *
from ..utile.HTTPUtile import *

## 广西桂林政府采购网 ##

# 采购公告，工作动态，通知公告，政策法规
class glszfcgw_cgtz_Spider(Spider):

    # 爬虫的名称
    name = 'glszfcgw_cgtz'
    # 网站标题
    __WebTitle = '广西桂林市政府采购网'
    # 网站地址
    __WebUrl = "http://zfcg.glcz.cn:880/IndexViewController.do?method=index"
    # 网站节点
    __WebNodes =[
                   '市级采购单一来源公告',
                   '市级采购中标公告',
                   '市级采购成交公告',
                   '市级采购更正公告',
                   '市级采购采购公告',
                   '市级采购其他公告',
                   '县区级采购采购公告',
                   '县区级采购成交公告',
                   '县区级采购更正公告',
                   '县区级采购单一来源公告',
                   '县区级采购中标公告',
                   '县区级采购其他公告',

                   '工作动态市级',
                   '通知公告市级',
                   '通知公告县区级',

                   '政策法规市级',
                   '策法规自治区级',
                   '政策法规国家级'
                   ]
    __Websites = __WebNodes
    # 网站节点URL
    __WebNodeUrls = [ 'http://zfcg.glcz.cn:880/CmsNewsController/getCmsNewsList/channelCode-shengji_dylygg/param_bulletin/20/page_%d.html',
                      'http://zfcg.glcz.cn:880/CmsNewsController/getCmsNewsList/channelCode-shengji_zbgg/param_bulletin/20/page_%d.html',
                      'http://zfcg.glcz.cn:880/CmsNewsController/getCmsNewsList/channelCode-shengji_cjgg/param_bulletin/20/page_%d.html',
                      'http://zfcg.glcz.cn:880/CmsNewsController/getCmsNewsList/channelCode-shengji_gzgg/param_bulletin/20/page_%d.html',
                      'http://zfcg.glcz.cn:880/CmsNewsController/getCmsNewsList/channelCode-shengji_cggg/param_bulletin/20/page_%d.html',
                      'http://zfcg.glcz.cn:880/CmsNewsController/getCmsNewsList/channelCode-shengji_qtgg/param_bulletin/20/page_%d.html',
                      'http://zfcg.glcz.cn:880/CmsNewsController/getCmsNewsList/channelCode-sxjcg_cggg/param_bulletin/20/page_%d.html',
                      'http://zfcg.glcz.cn:880/CmsNewsController/getCmsNewsList/channelCode-sxjcg_cjgg/param_bulletin/20/page_%d.html',
                      'http://zfcg.glcz.cn:880/CmsNewsController/getCmsNewsList/channelCode-sxjcg_gzgg/param_bulletin/20/page_%d.html',
                      'http://zfcg.glcz.cn:880/CmsNewsController/getCmsNewsList/channelCode-sxjcg_dylygg/param_bulletin/20/page_%d.html',
                      'http://zfcg.glcz.cn:880/CmsNewsController/getCmsNewsList/channelCode-sxjcg_zbgg/param_bulletin/20/page_%d.html',
                      'http://zfcg.glcz.cn:880/CmsNewsController/getCmsNewsList/channelCode-sxjcg_qtgg/param_bulletin/20/page_%d.html',

                      'http://zfcg.glcz.cn:880/GzdtControllerExt/getCmsNewsListGZDT/channelCode-sj/param_bulletin/20/page_%d.html',
                      'http://zfcg.glcz.cn:880/CmsNewsControllerExt/getCmsNewsListTZ/channelCode-sjgg/param_bulletin/20/page_%d.html',
                      'http://zfcg.glcz.cn:880/CmsNewsControllerExt/getCmsNewsListTZ/channelCode-qxgg/param_bulletin/20/page_%d.html',

                      'http://zfcg.glcz.cn:880/ZcfgControllerExt/getCmsNewsList/channelCode-sxjfgzd/param_bulletin/20/page_%d.html',
                      'http://zfcg.glcz.cn:880/ZcfgControllerExt/getCmsNewsList/channelCode-sjfgzd/param_bulletin/20/page_%d.html',
                      'http://zfcg.glcz.cn:880/ZcfgControllerExt/getCmsNewsList/channelCode-gjzcfg/param_bulletin/20/page_%d.html'
                    ]
    start_urls = [__WebUrl]  # 第一个URl


    ## 第一个response响应
    def parse(self, response):
        # 请求队列
        for WebNode,WebNodeUrl in zip(range(len(self.__WebNodes)),self.__WebNodeUrls):
            yield Request(WebNodeUrl % 1, callback=self.__page_parse, method='GET', meta={'WebNode': WebNode, 'page':1})


    ## 页面解析
    def __page_parse(self, response):
        try:
            # 首先抽取所有的文章
            papers = response.xpath('//div[@class="column infoLink noBox unitWidth_x6"]//ul//li')
            # 从每篇文章中抽取数据
            for paper in papers:
                # 标题
                Title = paper.xpath('./a/@title').extract()[0].strip()
                # url
                Url = response.urljoin(paper.xpath('./a/@href').extract()[0].strip())
                # 日期
                Time = paper.xpath('./span[@class="date"]/text()').extract()[0].strip()
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
            # 跟进request
            yield Request(url= self.__WebNodeUrls[response.meta['WebNode']] % (response.meta['page'] + 1), callback=self.__page_parse, method='GET', meta={'WebNode': response.meta['WebNode'], 'page': (response.meta['page'] + 1)})