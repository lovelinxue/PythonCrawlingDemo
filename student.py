# -*-coding:utf-8-*-

import urllib2

from bs4 import BeautifulSoup



urlstart = 'http://my.yingjiesheng.com/index.php/personal/xjhinfo.htm/?page='#为了方便翻页将网址代码分成两部分
urlend = '&cid=&city=21&word=&province=0&schoolid=&sdate=&hyid=0'

for i in range(1,20):#从网站上直接获取页面个数
    print '正在打印第'+str(i)
    url=urlstart+str(i)+urlend#整理网站地址
    print url

    request=urllib2.urlopen(url)#用urllib2打开网站

    html=request.read()#读取网站代码

    bs=BeautifulSoup(html,'html.parser',from_encoding='utf-8')#BeautifulSoup整理网站代码

    alllist1=bs.find_all('tr',class_='bg0')#每一页的信息分为两个部分

    alllist2=bs.find_all('tr',class_='bg1')

    alllist=alllist1+alllist2#整理信息

    # print alllist

    for contenttd in alllist:

        # print contenttd

        row=[]
        mouth = contenttd.find('td',width="100").text # 定位到宣讲时间字符位置
        companyweb=contenttd.find('td',width='250').find('a').get('href')#定位到宣讲企业网站

        if "http" not in companyweb:
            companyweb="http://my.yingjiesheng.com/"+str(companyweb)#有些企业网站存在省略现象，鼠标放在网站上可以看到完整网站包含http://头部，对有省略的网址加上这一部分

        companyname=contenttd.find('td',width='250').find('a').text#定位宣讲企业名字
        xuexiao=contenttd.find('td',width='250').next_sibling.next_sibling.text#定位宣讲学校名字，这里第一个兄弟节点通常是空，所以再定位一次兄弟节点。具体可以看BeautifulSoup官方文档有解释
        jiaoshi=contenttd.find('td',width='250').next_sibling.next_sibling.next_sibling.next_sibling.text#定位宣讲学校教室信息

        row.append(mouth)
        row.append(companyweb)
        row.append(companyname)
        row.append(xuexiao)
        row.append(jiaoshi)
        for j in range(0,len(row)):
            print row[j]
        #print row         #打印以上信息，如果直接打印row,中文不会出现
