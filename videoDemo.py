#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Display document description information
编译环境: Python


"""
__author__ = 'LoveLinXue.com'

import requests
from lxml import etree


class MiniMp4(object):

    def GetMovies(self, page):
        url = 'http://www.minimp4.com/movie/?page={}'.format(page)
        html = requests.get(url)
        htmll = etree.HTML(html.text)
        hrefs = htmll.xpath('//div[@class="meta"]/h1/a/@href')

        for url in hrefs:
            html = requests.get(url)
            dat = etree.HTML(html.text)
            moviename = dat.xpath('//div[@class="movie-meta"]/h1/text()')
            print(moviename)
            self.saveMovies(moviename)

    def saveMovies(self, data):
        with open('movies.txt', 'a', encoding='utf-8') as fp:
            fp.write(data[0] + '\n')


if __name__ == '__main__':
    miniClass = MiniMp4()
    for n in range(10):
        miniClass.GetMovies(n)
