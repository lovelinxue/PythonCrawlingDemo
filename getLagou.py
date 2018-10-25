#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
爬取拉钩网招聘信息的一个小demo,在网上看的源代码,于是自己学着去敲一下
源代码地址:https://www.52pojie.cn/thread-800108-2-1.html
"""
__author__ = 'LoveLinXue'

import re, requests, json, sys

print sys.version

city = raw_input("请输入要查询的工作城市: ")

name = raw_input('请输入要查询的工作名称: ')

reload(sys)
sys.setdefaultencoding('utf-8')

url = 'https://www.lagou.com/jobs/positionAjax.json?px=default&city=%s&needAddtionalResult=false' % city

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': 'WEBTJ-ID=20180918181741-165ec2f83d743-0ee41db9c69e0e-6e1f147a-2073600-165ec2f83d95d1; _ga=GA1.2.1559975793.1537265862; '
              'user_trace_token=20180918181742-13d9fe9b-bb2c-11e8-baf2-5254005c3644; LGUID=20180918181742-13da0831-bb2c-11e8-baf2-5254005c3644; '
              'JSESSIONID=ABAAABAAAFCAAEG0FCA6542C1D06F1F470B0A7189B8AD06; index_location_city=%E6%88%90%E9%83%BD; '
              'TG-TRACK-CODE=index_search; _gid=GA1.2.1437892044.1537705170; LGSID=20180923201929-eb4f9cfb-bf2a-11e8-bb56-5254005c3644;'
              ' PRE_UTM=; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DXpamso_IxFbfBezXbGYWv8-vI3sYyGf67_89jrtjXQK%26wd%3D%26eqid%3Da27f010200061c48000000025ba784cc;'
              ' PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1537265862,1537265872,1537354446,1537705170; '
              'LGRID=20180923201940-f1eea38b-bf2a-11e8-bb56-5254005c3644; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1537705181; SEARCH_ID=baf28c394763403c8afc3fc36dce76a4',
    'Host': 'www.lagou.com',
    'Origin': 'https://www.lagou.com',
    'Referer': 'https://www.lagou.com/jobs/list_python?isSchoolJob=1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
    'X-Anit-Forge-Code': '0', 'X-Anit-Forge-Token': 'None', 'X-Requested-With': 'XMLHttpRequest',
}

num = 0
bar = 0

while num < 100:
    num += 1
    date = {'first': 'true', 'kd': name, 'pn': num}
    returned = requests.post(url, data=date, headers=headers)
    html = json.loads(returned.text.strip('()[]'))
    html = html['content']
    html = html['positionResult']
    n = int(html['resultSize'])
    if n > 0:
        html = html["result"]
        for i in html:
            dianhua = i['lastLogin']
            xueli = i['education']
            gongzi = i['salary']
            gongsimingcheng = i['companyFullName']
            fuli = i['positionAdvantage']
            gongzuo = i['positionName']
            chengshi = i['city']
            bar += 1
            print '城市: %s -- 公司名称: %s -- 学历要求: %s -- 工作: %s -- 工资: %s -- 福利: %s -- 联系电话: %s' % (chengshi, gongsimingcheng, xueli, gongzuo, gongzi, fuli, dianhua)
    else:
        print '成功爬取 %s 条招聘信息' %bar
        break
