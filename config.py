#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/20 19:37
# @Author  : zhoujl
# @Site    : 
# @File    : config.py
# @Software: PyCharm

# 微博登陆信息
LOGIN_URL = 'https://passport.weibo.cn/signin/login?entry=mweibo&r=https://m.weibo.cn/'
USERNAME = '13471352284'
PASSWORD = 'Wfeii7827'

# 是否为Retina屏，并依此选择模板路径
RETINA = True
TEMPLATES_DIR = 'templates_retina/' if RETINA else 'templates/'


