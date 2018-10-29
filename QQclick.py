#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Display document description information
编译环境: Python3.7
QQ空间批量点赞
源代码地址:https://www.52pojie.cn/forum.php?mod=viewthread&tid=809228&extra=page%3D1%26filter%3Dauthor%26orderby%3Ddateline
"""
__author__ = 'LoveLinXue.com'

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time


options = webdriver.ChromeOptions()

options.add_argument('user-agent=Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Mobile Safari/537.36')

browser = webdriver.Chrome('/usr/local/bin/chromedriver', options=options)
browser.get('https://qzone.qq.com/')
browser.implicitly_wait(2)

# 输入QQ号
browser.find_element_by_id('u').send_keys('这里填写你的QQ账号')
# 输入QQ密码
browser.find_element_by_id('p').send_keys('这里填写你的QQ密码')
browser.find_element_by_id('go').click()
# 等待10秒手动解决验证码
time.sleep(10)

while True:
    try:
        like = browser.find_element_by_xpath('//button[text()="赞"]')
        top = int(like.location['y'])
        browser.execute_script('document.documentElement.scrollTop={}'.format(top))
        ActionChains(browser).move_to_element(like).click().perform()


    except Exception as e:
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        load_most = browser.find_element_by_xpath('//button[text()="加载更多"]')
        print(load_most)
        ActionChains(browser).move_to_element(load_most).click().perform()