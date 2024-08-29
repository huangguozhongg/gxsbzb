from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from gxsbzb.utile.HTTPUtile import *
##########  国家及区级以上单位网站 ##########
# 1.广西政府采购网
from gxsbzb.spiders.gxzfcgw_Spider import *
# 2.广西公共资源交易中心
from gxsbzb.spiders.gxggzy_Spider import *
# 3.中国政府采购网
from gxsbzb.spiders.zgzfcgw_Spider import *
# 4 .中国建筑业联合会
from gxsbzb.spiders.gxjzylhh_Spider import  *
# 5 .中国国际招标网
from gxsbzb.spiders.zggjzbw_Spider import  *
# 6.中国机电设备招标中心
from gxsbzb.spiders.zgjdsbzbzx_Spider import *
# 7.广西自然资源厅网站
from gxsbzb.spiders.gxzrzytwz_Spider import  *
# 8.广西水利厅
from gxsbzb.spiders.gxslt_Spider import  *
# 9.中央投资项目招标代理资格管理平台
from gxsbzb.spiders.zytzxmzbdlzgglpt_Spider import *
# 10 广西国资委
from gxsbzb.spiders.gxgzw_Spider import  *
# 11. 广西建设网
from gxsbzb.spiders.gxjsw_Spider import  *
# 12.广西住房和城乡建设厅网站与广西造价信息网
from gxsbzb.spiders.gxzjt_Spider import  *
# 13.广西政府采购中心
from gxsbzb.spiders.gxzfcgzx_Spider import *
# 14.广西壮族自治区市场监督管理局
from gxsbzb.spiders.gxscjgglj_Spider import *
# 15.广西壮族自治区文化厅
from gxsbzb.spiders.gxwlt_Spider import *
# 16.中国招标投标协会
from gxsbzb.spiders.zgzbtbxh_Spider import *
# 17.广西招标投标监督网
from gxsbzb.spiders.gxzbtbggfwpt_Spider import *
# 18.广西政协网
from gxsbzb.spiders.gxzx_Spider import *
# 19.广西南宁市文化广电和旅游局
from gxsbzb.spiders.gxnwlj_Spider import *
# 20.中国水利工程协会
from gxsbzb.spiders.zgslgcxh_Spider import *
# 21.中国住房和城乡建设网
from gxsbzb.spiders.zgzcjsb_Spider import *
# 22.中国招标投标公共服务平台
from gxsbzb.spiders.zgzbtbggfwpt_Spider import *
# 23.广西高级人民法院
from gxsbzb.spiders.gxgjrmfy_Spider import *
# 24.广西壮族自治区残疾人联合会
from gxsbzb.spiders.gxcjrlhh_Spider import *
# 25.中国招标采购网
from gxsbzb.spiders.zgzbcgw_Spider import *
# 26.中国发改委会
from gxsbzb.spiders.zgfgwyh_Spider import  *

##########  各地市级网站 ##########
# 1.广西南宁公共资源交易中心
from gxsbzb.spiders.nnsggzyjyzx_Spider import *
# 2.广西南宁市政府采购
from gxsbzb.spiders.nnszfcg_Spider import *
# 4.广西柳州市公共资源交易中心
from gxsbzb.spiders.lzsggzyjyzx_Spider import *
# 5.广西柳州市政府采购网站
from gxsbzb.spiders.lzszfcgw_Spider import *
# 6.广西百色市公共资源交易中心网
from gxsbzb.spiders.bssggzyjyzx_Spider import *
# 7.广西百色市财政局网站
from gxsbzb.spiders.bssczjwz_Spider import *
# 8.广西百色市人民政府网
from gxsbzb.spiders.bssrmzfmhwz_Spider import *
# 9.广西百色市住房和城乡建设局
from gxsbzb.spiders.bsszcxj_Spider import *
# 10.广西崇左市公共资源交易中心
from gxsbzb.spiders.czsggzyjyzx_Spider import *
# 11.广西北海市公共资源交易中心
from gxsbzb.spiders.bhsggzyjyzx_Spider import *
# 12.广西防城港市工程招标造价信息网
from gxsbzb.spiders.fcgszbzj_Spider import *
# 13.广西防城港市公共资源交易中心
from gxsbzb.spiders.fcgsggzyjyzx_Spider import *
# 14.广西防城港市政府采购网
from gxsbzb.spiders.fcgszfcgw_Spider import *
# 15.广西贵港市公共资源
from gxsbzb.spiders.ggsggzy_Spider import *
# 16.广西贵港市政府采购网
from gxsbzb.spiders.ggszfcgw_Spider import *
# 17.广西桂林市公共资源交易中心
from gxsbzb.spiders.glsggzyjyzx_Spider import *
# 18.广西桂林市政府采购网
from gxsbzb.spiders.glszfcgw_Spider import *
# 19.广西河池市公共资源交易中心
from gxsbzb.spiders.hcsggzyjyzx_Spider import *
# 20.广西河池市人民政府门户网站
from gxsbzb.spiders.hcsrmzfmhwz_Spider import *
# 21.广西贺州市公共资源交易中心
from gxsbzb.spiders.hzsggzyjyzx_Spider import *
# 22.广西来宾市公共资源交易中心
from gxsbzb.spiders.lbsggzyjyzx_Spider import *
# 23.广西钦州市公共资源交易中心
from gxsbzb.spiders.qzsggzyjyzx_Spider import *
# 24.广西钦州市政府采购中心
from gxsbzb.spiders.qzszfcgzx_Spider import *
# 25.广西财经学院
from gxsbzb.spiders.gxcjxy_Spider import *
# 26.广西钦州市住房和城乡建设局
from gxsbzb.spiders.qzszcjsj_Spider import *
# 27.广西河池市天峨县人民政府门户网站
from gxsbzb.spiders.hcstxxrmzfmhwz_Spider import *
# 28.广西大学
from gxsbzb.spiders.gxdx_Spider import *
# 29.广西梧州市公共资源交易中心
from gxsbzb.spiders.wzsggzyjyzx_Spider import *
# 30.广西梧州市政府采购网
from gxsbzb.spiders.wzszfcgw_Spider import *
# 31.广西玉林市公共资源交易平台
from gxsbzb.spiders.ylsggzyjypt_Spider import *
# 32.广西玉林市人民政府门户网站
from gxsbzb.spiders.ylsrmzfmhwz_Spider import *

########## 测试 ##########
from gxsbzb.spiders.TestSpider import *

if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    # # 1.广西政府采购网
    # process.crawl(gxzfcgw_xxgg_Spider)
    # process.crawl(gxzfcgw_zcfg_Spider)
    # process.crawl(gxzfcgw_jdjc_Spider)
    # process.crawl(gxzfcgw_xxgg_jggg_zbjggg_second_Spider)
    # process.crawl(gxzfcgw_xxgg_htgg_first_Spider)
    # process.crawl(gxzfcgw_xxgg_htgg_second_Spider)
    # 2.广西壮族自治区公共资源交易中心
    # process.crawl(gxggzy_zbjydt_Spider)
    # 3.中国政府采购网
    # process.crawl(zgzfcgw_zcfg_Spider)
    # process.crawl(zgzfcgw_cggg_Spider)
    # # 4. 广西建筑业联合会
    # process.crawl(gxjzylhh_tsz_Spider)
    # # 5 .中国国际招标网
    # process.crawl(zggjzbw_zh_Spider)
    # process.crawl(zggjzbw_ywxx_Spider)
    # # 6.中国机电设备招标中心
    # process.crawl(zgjdsbzbzx_tzgg_Spider)
    # # 7. 广西自然资源厅网站
    # process.crawl(gxzrzytwz_ggbg_Spider)
    # # 8. 广西壮族自治区水利厅网站
    # process.crawl(gxslt_tzgg_Spider)
    # # 9.中央投资项目招标代理资格管理平台
    # process.crawl(zytzxmzbdlzgglpt_zc_Spider)
    # # 10 广西壮族自治区人民政府国有资产监督管理委员会网站
    # process.crawl(gxgzw_cb_Spider)
    # # 11.广西建设网
    # process.crawl(gxjsw_zbxx_Spider)
    # process.crawl(gxjsw_rdxx_Spider)
    # 12.广西住房和城乡建设厅网站
    # process.crawl(gxzjt_wgzz_Spider)
    # 13.广西壮族自治区政府采购中心
    # process.crawl(gxzfcgzx_cbz_Spider)
    # 14.广西壮族自治区市场监督管理局
    # process.crawl(gxscjgglj_dtw_Spider)
    # 15.广西壮族自治区文化和旅游厅门户网站
    # process.crawl(gxwlt_tzgg_Spider)
    # process.crawl(gxwlt_gwyyw_Spider)
    # process.crawl(gxwlt_gxyw_Spider)
    # 16.中国招标投标协会
    # process.crawl(zgzbtbxh_tzzg_Spider)
    # 17.广西壮族自治区招标投标公共服务平台
    # process.crawl(gxzbtbggfwpt_zbgg_Spider)
    # process.crawl(gxzbtbggfwpt_tzgg_Spider)
    # 18.广西政协网
    # process.crawl(gxzx_tht_Spider)
    # 19.广西南宁市文化广电和旅游局
    # process.crawl(gxnwlj_gtz_Spider)
    # 20.中国水利工程协会
    # process.crawl(zgslgcxh_tx_Spider)
    # 21.中华人民共和国住房和城乡建设部
    # process.crawl(zgzcjsb_zx_Spider)
    # 22.中国招标投标公共服务平台
    # process.crawl(zgzbtbggfwpt_zzzzg_Spider)
    # 23.广西壮族自治区高级人民法院
    # process.crawl(gxgjrmfy_tzgg_Spider)
    # 24.广西壮族自治区残疾人联合会
    # process.crawl(gxcjrlhh_tzgg_Spider)
    # 25.中国招标采购网
    # process.crawl(zgzbcgw_zzc_Spider)
    # 26.中华人民共和国国家发展和改革委员会
    # process.crawl(zgfgwyh_fgwg_Spider)


##########  各地市级网站 ##########
    # 1.广西南宁市公共资源交易中心
    # process.crawl(nnggzyjyzx_gtzz_Spider)
    # 2.广西南宁市政府集中采购中心网站
    # process.crawl(nnzfcg_zc_Spider)
    # 4.广西柳州市公共资源交易中心
    # process.crawl(lzsggzyjyzx_zjg_Spider)
    # 5.广西柳州市政府采购网站
    # process.crawl(lzszfcgw_zzc_Spider)
    # 6.广西百色市公共资源交易中心
    # process.crawl(bssggzyjyzx_ztzj_Spider)
    # 7.广西百色市财政局网站
    # process.crawl(bssczjwz_tzgg_Spider)
    # 8.广西百色市人民政府网??
    # process.crawl(bssrmzfmhwz_tzw_Spider)
    # 9.广西百色市住房和城乡建设局
    # process.crawl(bsszcxj_gt_Spider)
    # process.crawl(bsszcxj_q_Spider)
    # 10.广西崇左市公共资源交易中心
    # process.crawl(czsggzyjyzx_tzj_Spider)
    # 11.广西北海市公共资源交易中心
    # process.crawl(bhsggzyjyzx_tgzz_Spider)
    # 12.广西防城港市工程招标造价信息网
    # process.crawl(fcgszbzj_tzz_Spider)
    # 13.广西防城港市公共资源交易中心
    # process.crawl(fcgsggzyjyzx_tgzj_Spider)
    # 14.广西防城港市政府采购网
    # process.crawl(fcgszfcgw_zc_Spider)
    # 15.广西贵港市公共资源
    # process.crawl(ggsggzy_tzj_Spider)
    # 16.广西贵港市政府采购网
    # process.crawl(ggszfcgw_zcz_Spider)
    # 17.广西桂林市公共资源交易中心
    # process.crawl(glsggzyjyzx_ztzj_Spider)
    # 18.广西桂林市政府采购网
    # process.crawl(glszfcgw_cg_Spider)
    # 19.广西河池市公共资源交易中心
    # process.crawl(hcsggzyjyzx_tgzz_Spider)
    # 20.广西河池市人民政府门户网站
    # process.crawl(hcsrmzfmhwz_tzx_Spider)
    # 21.广西贺州市公共资源交易中心
    # process.crawl(hzsggzyjyzx_gzz_Spider)
    # 22.广西来宾市公共资源交易中心
    # process.crawl(lbsggzyjyzx_gtzz_Spider)
    # 23.广西钦州市公共资源交易中心
    # process.crawl(qzsggzyjyzx_gtzz_Spider)
    # 24.广西钦州市政府采购中心
    # process.crawl(qzszfcgzx_cgtz_Spider)
    # 25.广西财经学院
    # process.crawl(gxcjxy_c_Spider)
    # 26.广西钦州市住房和城乡建设局
    # process.crawl(qzszcjsj_zh_Spider)
    # 27.广西河池市天峨县人民政府门户网站
    # process.crawl(hcstxxrmzfmhwz_tz_Spider)
    # 28.广西大学
    # process.crawl(gxdx_t_Spider)
    # 29.广西梧州市公共资源交易中心
    # process.crawl(wzsggzyjyzx_ztzj_Spider)
    # 30.广西梧州市政府采购网
    # process.crawl(wzszfcgw_sx_Spider)
    # process.crawl(wzszfcgw_zt_Spider)
    # 31.广西玉林市公共资源交易平台
    # process.crawl(ylsggzyjypt_tf_Spider)
    # process.crawl(ylsggzyjypt_j_Spider)
    # 32.广西玉林市人民政府门户网站
    # process.crawl(ylsrmzfmhwz_t_Spider)
    # 测试
    # process.crawl(TestSpider)
    process.start()

