#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/21 10:56
# @Author  : zhoujl
# @Site    : 
# @File    : templates_gen.py
# @Software: PyCharm
from crack import CrackWeiboSlide

if __name__ == '__main__':
    crack = CrackWeiboSlide()
    count = 1
    while True:
        crack.open()
        captcha = crack.get_image(name='templates_retina/{}.png'.format(count))
        count += 1