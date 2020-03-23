#!/usr/bin/env python
# encoding: utf-8
'''
@author: kafkal
@contact: 1051748335@qq.com
@software: pycharm
@file: parse_map.py
@time: 2020/3/23 023 15:35
@desc:
'''
import re
import os

def parse_map(filename:str) -> bool:
    if os.path.exists(filename):
        try:
            with open(filename,'r',encoding='utf-8') as f:
                content = f.read()
                maps = re.findall('<tr><td>(.*?)<',content,re.M)
                map_armory = {}
                for i in maps:
                    map_div = re.findall(f'>{i}<.*?</tr>',content,re.M)
                    total_need = re.findall('td> (\d+).*?<',map_div[0])
                    armory_list = re.findall(f'<img.*?title="(.*?)".*?<h6.*?>(\d+)<.*?<span class="text-center py-1 d-block"> (\d+)',map_div[0],re.M)
                    armory_list.insert(0,total_need[0])
                    map_armory[i] = armory_list

            with open('map.db','w',encoding='utf-8') as f:
                for map,armorys in map_armory.items():
                    str = map + ' ' + armorys[0]
                    for armory in armorys[1:]:
                        str = str + ' ' + '#'.join(armory)
                    f.write(str + '\n')
            return True
        except:
            return False

