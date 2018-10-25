#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Display document description information

根据网上找的demo自己去学习一下保存文件相关的内容
源代码地址:https://www.52pojie.cn/thread-807386-1-2.html

"""
__author__ = 'LoveLinXue.com'


import urllib.request, lxml.html, time, os, re


def serchIndex(name):
    url = 'https://www.nvshens.com/girl/search.aspx?name=' + name
    print(url)
    html = urllib.request.urlopen(url).read().decode('utf-8')
    return html


def selectOne(html):
    tree = lxml.html.fromstring(html)
    one = tree.cssselect('#DataList1 > tr > td:nth-child(1) > li > div > a')[0]
    href = one.get('href')
    url = 'https://www.nvshens.com' + href + 'album/'
    print(url)
    html = urllib.request.urlopen(url).read().decode('utf-8')
    print(html)
    return html


def findPageTotal(html):
    tree = lxml.html.fromstring(html)
    lis = tree.cssselect('#photo_list > ul > li')
    list = []
    for li in lis:
        url = li.cssselect('div.igalleryli_div > a')
        href = url[0].get('href')
        list.append(href)

    findimage_urls = set(list)
    print(findimage_urls)
    return findimage_urls


def downloadImage(image_url, filename):
    for i in range(len(image_url)):
        try:
            req = urllib.request.Request(image_url)
            req.add_header('User-Agent', 'chrome 4{}'.format(i))
            image_data = urllib.request.urlopen(req).read()
        except (urllib.request.HTTPError, urllib.request.URLError) as e:
            time.sleep(0.1)
            continue
        open(filename, 'wb').writable(image_data)
        break


def mkdirByGallery(path):
    # 去除首位空格
    path = path.strip()
    path = 'E:\\py\\photo\\'+path
    #这两个函数之间最大的区别是当父目录不存在的时候os.mkdir(path)
    #不会创建，os.makedirs(path)
    #则会创建父目录。
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
    return path

