#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Display document description information
编译环境: Python3.7
批量下载优美网站图片
源代码地址:https://www.52pojie.cn/thread-807935-1-1.html

"""
__author__ = 'LoveLinXue.com'


import os
import requests
import re
from lxml import etree
import threading


class Umeispider():

    def __init__(self):
        # 需要爬取的地址,自己替换
        # self.base_url = "http://www.umei.cc/bizhitupian/fengjingbizhi/23547.htm"
        self.base_url = 'http://www.umei.cc/bizhitupian/fengjingbizhi/23530.htm'

    def get_url(self):
        urls = []
        if self.base_url[-7] == '_':
            url = self.base_url[:-7] + ".htm"
            print(url, 7)

        elif self.base_url[-6] == '_':
            url = self.base_url[:-6] + ".htm"
            print(url, 6)

        else:
            url = self.base_url
            print(url, 0)
        urls.append(url)
        url2 = url[:-4] + '_{}' + ".htm"
        for Num in range(2, 50):
            urls.append(url2.format(Num))

        print(urls)

        return urls

    def run(self):
        urls = self.get_url()
        for url in urls:
            # print(url)
            # print('请求地址: ', url)
            html_str = requests.get(url).content.decode('utf-8')
            if re.findall(r'404 Not Found', html_str):
                break
            self.get_image_url_name(html_str)

    def create_folder(self, file_name):
        if not os.path.exists(file_name):
            os.mkdir(file_name)
            print('文件夹%s创建成功' % file_name)

    def get_image_url_name(self, html):
        eroot = etree.HTML(html)
        image_url = eroot.xpath('//div/p//img/@src')[0]
        file_name = eroot.xpath('//strong/text()')[0]
        threading.Thread(target=self.save_image, args=(image_url, file_name)).start()

    def save_image(self, image_url, name):
        print('开始下载:', name)
        content = requests.get(image_url).content
        # 这里输入文件夹名
        folder_name = 'downloads'
        self.create_folder(folder_name)

        path = '%s/%s.jpg' % (folder_name, name)
        with open(path, 'wb') as f:
            f.write(content)

        print('下载完成', name)


if __name__ == '__main__':
    spider = Umeispider()
    # spider.get_url()
    spider.run()