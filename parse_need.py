#!/usr/bin/env python
# encoding: utf-8
'''
@author: kafkal
@contact: 1051748335@qq.com
@software: pycharm
@file: parse_need.py
@time: 2020/3/23 023 15:35
@desc:
'''
import re
import os

def parse_need(filename:str) -> bool:
    if os.path.exists(filename):
        try:
            with open('need.html','r',encoding='utf-8') as f:
                content = f.read()
                names = re.findall('<h6.*?>(.*?)<',content,re.M)
                needs = re.findall('<span class="badge badge-danger">(\d+)<',content,re.M)

            with open('need.db','w',encoding='utf-8') as f:
                for i in range(len(names)):
                    f.write(f"{names[i]} {needs[i]}\n")
            return True
        except:
            return False