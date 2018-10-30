#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Display document description information
编译环境: Python


"""
__author__ = 'LoveLinXue.com'

from bs4 import BeautifulSoup
import requests
import lxml
import re
import pandas as pd
from tqdm import tqdm
import math


class lianjia():
    def __init__(self):

        self.pattern = re.compile(
            '<div class="info clear">.*?target="_blank">(.*?)</a>.*?class="houseInfo"><span class="houseIcon">.*?target="_blank">(.*?)</a>(.*?)</div>.*?class="positionIcon"></span>(.*?)<a href=.*?target="_blank">(.*?)</a>.*?class="totalPrice"><span>(.*?)</span>万')
        self.house_num_pattern = re.compile(u'共找到<span> (.*?) </span>套深圳二手房')
        self.area_dic = {'罗湖区': 'luohuqu',
                         '福田区': 'futianqu',
                         '南山区': 'nanshanqu',
                         '盐田区': 'yantianqu',
                         '宝安区': 'baoanqu',
                         '龙岗区': 'longgangqu',
                         '龙华区': 'longhuaqu',
                         '坪山区': 'pingshanqu'}

    def get_info(self, url):
        html = requests.get(url).text
        html = html.encode('utf-8')
        soup = BeautifulSoup(html, 'lxml')
        infos = soup.find_all(class_="info clear")
        return infos

    def get_content(self, info, area):
        info_dic = {}
        info = re.findall(self.pattern, str(info))
        info = list(info[0])
        info_dic['title'] = info[0].strip()
        info_dic['community'] = info[1].strip()
        house_list = info[2].split('|')
        if len(house_list) == 6:
            info_dic['hourseType'] = house_list[1].strip()
            info_dic['area'] = house_list[2].strip()
            info_dic['direction'] = house_list[3].strip()
            info_dic['fitment'] = house_list[4].strip()
            info_dic['elevator'] = house_list[5].strip()
        else:
            info_dic['hourseType'] = house_list[1].strip()
            info_dic['area'] = house_list[2].strip()
            info_dic['direction'] = house_list[3].strip()
            info_dic['fitment'] = '其他'
            info_dic['elevator'] = house_list[4].strip()
        info_dic['floorInfo'] = info[3].strip(' -  ')
        info_dic['position'] = info[4].strip()
        info_dic['price'] = info[5].strip()
        info_dic['area_positon'] = area
        return info_dic

    def run(self):
        data = pd.DataFrame()
        for area in self.area_dic.keys():
            print
            '>>>> 正在保存%s的二手房信息>>>\n' % area
            url = 'https://sz.lianjia.com/ershoufang/%s/' % self.area_dic[area]
            r = requests.get(url).text
            house_num = re.findall(self.house_num_pattern, r)[0].strip()
            total_page = int(math.ceil(int(house_num) / 30.0))
            if total_page >= 100:
                total_page = 100
            else:
                pass
            for page in tqdm(range(total_page)):
                url = 'https://sz.lianjia.com/ershoufang/%s/pg%s/' % (self.area_dic[area], str(page + 1))
                infos = self.get_info(url)
                for info in infos:
                    info_dic = self.get_content(info, area)
                    if data.empty:
                        data = pd.DataFrame(info_dic, index=[0])
                    else:
                        data = data.append(info_dic, ignore_index=True)
        data.to_csv('lianjia.csv', encoding='utf-8-sig')
        print
        '>>>> 链家二手房数据已保存❗️❗️❗️'


if __name__ == '__main__':
    x = lianjia()
    x.run()
