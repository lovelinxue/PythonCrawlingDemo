#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Display document description information
编译环境: Python
网络源代码地址:

"""


__author__ = 'LoveLinXue.com'

import urllib.request
import json
import random
import os

size = 0
pageNum = 1
downloadNum = 0


def get(url):
    url = url
    request = urllib.request.Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0')
    request.add_header('X-Forwarded-For', str(random.randint(0, 255)) + '.' + str(random.randint(0, 255)) + '.' + str(
        random.randint(0, 255)) + '.' + str(random.randint(0, 255)))
    result = urllib.request.urlopen(request).read()
    return result


def save(url, fileName):
    with open(fileName, 'wb') as f:
        f.write(get(url))
        print(fileName + '  下载完成OK')
    global size
    size += os.path.getsize(fileName)
    global downloadNum
    downloadNum += 1


def download(result, filePath):
    for i in range(0, len(result)):
        if (result[i]['src']):
            save(result[i]['src'], filePath+'/'+result[i]['trackName']+'.m4a')
        else:
            print('%s 下载失败,可能因为是付费专辑' %(result[i]['trackName']))


def run():
    filePath = input('请输入存放数据的路径地址\n')
    if os.path.exists(filePath):
        if (os.listdir(filePath)):
            print('文件夹 %s 已经存在且不为空' % (filePath))
            run()
        else:
            print('文件夹 %s 不为空,可以使用' % (filePath))
    else:
        os.mkdir(filePath)
        print('文件夹 %s 将被创建' %(filePath))
    id=input('请输入ID\n')

    try:
        id = int(id)
    except Exception as e:
        print('错误: %s 错误原因:ID非纯数字' %e )
        run()

    print('开始下载'.center(30, '#'))
    pageid = 1
    hasMore = 1
    while hasMore:
        url = "https://www.ximalaya.com/revision/play/album?albumId=" + str(id) + "&pageSize=30&pageNum=" + str(pageid)
        result=get(url).decode('utf-8')
        hasMore = json.loads(result)['data']['hasMore']
        result = json.loads(result)['data']['tracksAudioPlay']
        download(result, filePath)
        pageid += 1
        print('下载结束'.center(30,'#'))
        print("文件存放路径%s,一共下载%s集,占用空间%.2fMb" % (os.getcwd() + "/" + filePath, downloadNum, size / 1024 / 1024))


if __name__ == '__main__':
    run()



