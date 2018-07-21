#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/21 10:45
# @Author  : zhoujl
# @Site    : 
# @File    : error.py
# @Software: PyCharm
class NoMatchedTemplateError(Exception):
    def __init__(self):
        super.__init__(self)

    def __str__(self):
        return repr('No Match Template!')