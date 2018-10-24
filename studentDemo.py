# -*-coding:utf-8-*-

import urllib2
import sys

from bs4 import BeautifulSoup

# 写入Excel表需要使用的库
from openpyxl import Workbook

reload(sys)
sys.setdefaultencoding('utf-8')  # 设置系统默认编码

print sys.version  # 打印当前版本信息
sys.setdefaultencoding('utf-8')

# 为了方便翻页将网址代码分成两部分
urlstart = 'http://my.yingjiesheng.com/index.php/personal/xjhinfo.htm/?page='
urlend = '&cid=&city=21&word=&province=0&schoolid=&sdate=&hyid=0'

setSQLData = []

# 爬取数据 总页数64,为了练习,就取20页
for i in range(1, 11):
    url = urlstart + str(i) + urlend

    print '正在打印:' + url;

    request = urllib2.urlopen(url)
    html = request.read()
    bs = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    alllist1 = bs.find_all('tr', class_='bg0')
    alllist2 = bs.find_all('tr', class_='bg1')
    alllist = alllist1 + alllist2

    # 对数据进行处理筛选
    for contenttd in alllist:

        month = contenttd.find('td', width='120').text
        companyweb = contenttd.find('td', width='250').find('a').get('href')

        if 'http' not in companyweb:
            companyweb = 'http://my.yingjiesheng.com/' + str(companyweb)

        companyName = contenttd.find('td', width='250').find('a').text
        school = contenttd.find('td', width='250').next_sibling.next_sibling.text
        classRoom = contenttd.find('td', width='250').next_sibling.next_sibling.next_sibling.next_sibling.text

        row = [month, companyweb, companyName, school, classRoom]

        setSQLData.append(row)

# 将数据写入Excel
wb = Workbook()
# 设置Excel文件名
dest_filename = 'UserInfoFile.xlsx'
# 新建一个表
ws1 = wb.active

# 设置表头
titleList = ['时间', '网址', '招聘企业', '学校', '地址']
for row in range(len(titleList)):
    c = row + 1
    ws1.cell(row=1, column=c, value=titleList[row])

# 填写表内容
for listIndex in range(len(setSQLData)):
    ws1.append(setSQLData[listIndex])

wb.save(filename=dest_filename)
