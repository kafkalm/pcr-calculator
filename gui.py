#!/usr/bin/env python
# encoding: utf-8
'''
@author: kafkal
@contact: 1051748335@qq.com
@software: pycharm
@file: gui.py
@time: 2020/3/23 023 17:24
@desc:
'''
from tkinter import *
from tkinter import ttk,filedialog,messagebox
from calculate import *
from parse_need import *
from parse_map import *

needs = None
map_armory = None
armorys = {}

def algorithmSwitch(choose):
    if choose == "地图效率":
        armoryBox.configure(state="disabled")
        armoryBox.current(0)
    elif choose == "装备优先":
        armoryBox.configure(state = "readonly")
        needpath = need_path.get()
        if needpath in armorys:
            armoryBox['values'] = armorys[needpath]
        else:
            if not parse_need(needpath):
                messagebox.showerror('错误', '解析设计图模式错误,请检查文件/文件路径是否正确')
                algorithmMode.set("地图效率")
                armoryBox.configure(state="disabled")
                raise SystemError("解析设计图模式错误")
            needs = get_need('need.db')
            new_value = ['']
            for need in needs:
                new_value.append(need)
            armorys[needpath] = new_value
            armoryBox['values'] = new_value
        armoryBox.current(0)


def choose_need():
    need.delete('0','end')
    need.insert('0',filedialog.askopenfilename())


def choose_map():
    map.delete('0', 'end')
    map.insert('0', filedialog.askopenfilename())


def get_level():
    if map_level.get() != '':
        level = map_level.get().split("-")
        if 0 < int(level[0]) < 32 and 0 < int(level[1]) < 15:
            return map_level.get()
        messagebox.showerror('错误','关卡格式不正确!')
        level.delete('0','end')
    return ''


def calculate():
    global needs,map_armory
    needpath = need_path.get()
    mappath = map_path.get()
    if not parse_need(needpath):
        messagebox.showerror('错误','解析设计图模式错误,请检查文件/文件路径是否正确')
        raise SystemError("解析设计图模式错误")
    if not parse_map(mappath):
        messagebox.showerror('错误','解析地图掉落错误,请检查文件/文件路径是否正确')
        raise SystemError("解析地图掉落错误")
    needs = get_need('need.db')
    map_armory = get_map('map.db')
    algorithm = algorithmMode.get()

    level = get_level()
    if level:
        map_limit(map_armory,level)
    armory = armoryChoose.get()
    res = cal_times(algorithm,map_armory,needs,armory)

    if algorithm == '地图效率':
        res_str = f'所需次数 : {res[1]}次\n'
        for map,times in res[0].items():
            res_str += f'{map} : {times}次\n'
    elif algorithm == '装备优先':
        res_str = f'所需次数 : {res[1]}次\n'
        for i in res[0]:
            res_str += f'{i[0]} : 效率 {i[1][0]}%\n'
    result.delete('1.0',END)
    result.insert(INSERT,res_str)



root = Tk()
root.title("Princess Connect Re:dive 刷图计算器")
root.iconbitmap(r"D:\python_file\PCR\pcr.ico")
root.geometry("500x620")
root.resizable(width = False,height = False)

Label(root,text='算法选择',width=12,height=2).place(x=0,y=445)
Label(root,text = '关卡限制',width=12,height = 2).place(x = 0,y=480)
Label(root,text = '设计图文件',width=12,height = 2).place(x= 0,y=510)
Label(root,text = '地图掉落文件',width=12,height = 2).place(x=0,y=540)
Label(root,text = '默认选择日服最新进度,填写格式为XX-XX,如29-14',width=45,height = 2).place(x=160,y=480)
Label(root,text = '优先装备选择',width = 12,height = 2).place(x=200,y=445)
Label(root,text = 'Made By kafkal\nqq:1051748335',width = 20,height = 2).place(x=330,y=580)

algorithmMode = StringVar()
algorithmMode.set("地图效率")
armoryChoose = StringVar()
map_level = StringVar()
need_path = StringVar()
map_path = StringVar()

level = Entry(root,textvariable = map_level,width=10)
level.place(x=90,y=488)
need = Entry(root,textvariable = need_path,width = 40)
need.place(x=90,y=518)
map = Entry(root,textvariable = map_path,width = 40)
map.place(x=90,y=549)

Button(root,text="选择",width = 12,command = choose_need).place(x=380,y=515)
Button(root,text="选择",width = 12,command = choose_map).place(x=380,y=545)
Button(root,text="计算",width = 20,command = calculate).place(x=20,y=580)
Button(root,text="导出",width = 20,command = calculate).place(x=180,y=580)


armoryBox = ttk.Combobox(root,textvariable=armoryChoose)
armoryBox.place(x=290,y=450)
armoryBox.configure(state = "disabled")

algorithmOption = OptionMenu(root,algorithmMode,"地图效率","装备优先",command=algorithmSwitch)
algorithmOption.place(x=88,y=445)

result = Text(root,width=67,height=32)
result.place(x=10,y=10)

root.mainloop()