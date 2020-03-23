#!/usr/bin/env python
# encoding: utf-8
'''
@author: kafkal
@contact: 1051748335@qq.com
@software: pycharm
@file: calculate.py
@time: 2020/3/23 023 15:35
@desc:
'''
import config

def get_map(filename:str) -> dict:
    '''

    获取地图掉落信息

    :param filename:
    :return:
    '''
    with open(filename,'r',encoding='utf-8') as f:
        lines = f.readlines()
    map_armory = {}
    for line in lines:
        line = line.split()
        map = line[0]
        armorys = [int(line[1])]
        for armory in line[2:]:
            armory = armory.split("#")
            armorys.append((armory[0],int(armory[1]),int(armory[2])))
        map_armory[map] = armorys
    return map_armory


def get_need(filename:str) -> dict:
    '''

    获取所需设计图信息

    :param filename:
    :return:
    '''
    with open(filename,'r',encoding='utf-8') as f:
        lines = f.readlines()
    needs = {}
    for line in lines:
        line = line.split()
        needs[line[0]] = int(line[1])
    return needs


def cal_efficiency(map_armory:dict) -> dict:
    '''

    计算刷图效率

    :param map_armory:
    :return:
    '''
    map_efficiency = {}
    for map,armory in map_armory.items():
        efficiency = 0
        for i in armory[1:]:
            if i[2] > 0:
                efficiency += i[1]
        map_efficiency[map] = (efficiency,armory[0])
    return map_efficiency

def sort_map_armory_by_efficiency(map_armory) -> list:
    map_efficiency = cal_efficiency(map_armory)
    return sorted(map_efficiency.items(),key=lambda x:(x[1][0],x[1][1]),reverse=True)


def _map_compare(map1,map2:str) -> bool:
    map1 = [int(x) for x in map1.split('-')]
    map2 = [int(x) for x in map2.split('-')]
    if map1[0] > map2[0] or (map1[0] == map2[0] and map1[1] > map2[1]):
        return True
    return False

def map_limit(map_armory:dict,limit:str):
    pop_k = []
    for k in map_armory:
        if _map_compare(k,limit):
            pop_k.append(k)
    for k in pop_k:
        map_armory.pop(k)


def _armory_in_map(armory:str,armorys:list) -> bool:
    for i in range(1,len(armorys)):
        if armory == armorys[i][0]:
            return True
    return False

def _find_min_armory(armorys:list) -> str:
    '''

    找出最少次数能刷到的装备

    :param armorys:
    :return:
    '''
    min_armory = armorys[1]
    for i in range(2,len(armorys)):
        if min_armory[2] == 0:
            min_armory = armorys[i]
            continue
        if armorys[i][2] > 0 and armorys[i][2] / armorys[i][1] < min_armory[2] / min_armory[1]:
            min_armory = armorys[i]
    return min_armory

def _update_needs(armorys:list,needs:dict,times:int):
    '''

    更新所需设计图

    :param armorys:
    :param needs:
    :param times:
    :return:
    '''
    for i in range(1,len(armorys)):
        if armorys[i][0] in needs:
            needs[armorys[i][0]] -= int(times * armorys[i][1] / 100 * config.Multiple + 1)
            if needs[armorys[i][0]] < 0 :
                needs[armorys[i][0]] = 0

def _update_map_armory(needs,map_armory:dict):
    '''

    更新地图掉落

    :param needs:
    :param map_armory:
    :return:
    '''
    pop_k = []
    for map,armorys in map_armory.items():
        sum = 0
        for i in range(1,len(armorys)):
            if armorys[i][0] in needs:
                armorys[i] = (armorys[i][0],armorys[i][1],needs[armorys[i][0]])
                sum += needs[armorys[i][0]]
        armorys[0] = sum
        if armorys[0] == 0:
            pop_k.append(map)
    for k in pop_k:
        map_armory.pop(k)

def cal_times(algorithm:str,map_armory,needs:dict,armory=''):
    '''

    计算所需刷图次数 可选择算法
    目前以地图效率作为衡量指标

    :param algorithm:
    :param map_armory:
    :param needs:
    :return:
    '''
    mapTimes = {}
    totalTimes = 0
    if algorithm == "needs_weight" or algorithm == "装备优先":
        pop_k = []
        for map,armorys in map_armory.items():
            flag = False
            for i in range(1,len(armorys)):
                if armorys[i][0] == armory:
                    flag = True
                    break
            if not flag:
                pop_k.append(map)
        for k in pop_k:
            map_armory.pop(k)
        map_efficiency = sort_map_armory_by_efficiency(map_armory)
        return map_efficiency,'NaN'

    elif algorithm == "map_efficiency" or algorithm == "地图效率":
        while map_armory:
            map_efficiency = sort_map_armory_by_efficiency(map_armory)
            now_map = map_efficiency[0][0]
            armorys = map_armory[now_map]
            min_armory = _find_min_armory(armorys)
            times = int(min_armory[2] / (config.Multiple * min_armory[1]/100))
            _update_needs(armorys,needs,times)
            _update_map_armory(needs,map_armory)
            mapTimes[now_map] = mapTimes.get(now_map, 0) + times
            totalTimes += times
        return mapTimes,totalTimes

if __name__ == '__main__':
    map_armory = get_map("map.db")
    # map_limit(map_armory,'29-14')
    needs = get_need("need.db")
    print(cal_times(config.Algorithm, map_armory, needs))