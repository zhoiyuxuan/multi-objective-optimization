import json
import os

import requests
import re
import random
import time
import banword_list
import pandas as pd
import datetime
import threading
import listen
import random

'下面这个函数用来判断信息开头的几个字是否为关键词'
'如果是关键词则触发对应功能，群号默认为空'

def keyword(message, uid, gid = None, mid = None):
    if message == '你好':
        return welcome(uid, gid)

    #针对某个待管理群聊
    if gid == 0000000: #gid是int32形式
        #敏感词检测
        result = retract(message,mid,uid)
        #封禁检测
        if result ==0:
            ban_user(gid,uid)


    if gid == 607575078 and '小小埋来点儿st' in message:
        pic_sender(gid)






# todo:自动群聊管理

#欢迎(回复) 传入gid,message
def welcome(uid, gid):
    if gid != None:  # 如果是群聊信息
        requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={}&message=hello'.format(gid))
    else:  # 如果是私聊信息
        requests.get(url='http://127.0.0.1:5700/send_private_msg?user_id={}&message=hello'.format(uid))

#撤回信息 传入message_id
def retract(message,mid,uid):
    t = time.gmtime()
    t_format = time.strftime("%Y-%m-%d",t)
    f = open(f'./{t_format}retract.txt','a+')
    b = banword_list.Banword()

    #拓展检测在这里进行添加api
    # todo 添加图像识别api 正则表达式筛选

    a = re.findall('[\u4e00-\u9fa5a-zA-Z0-9]+', message, re.S)  # 只要字符串中的中文，字母，数字
    a = "".join(a)
    print(a)

    #关键词触发
    for i in b.gnlist:
        if i in a and uid not in white_list:
            requests.get(url=f'http://127.0.0.1:5700/delete_msg?message_id={mid}')
            t_format = time.strftime('%H:%M:%S',t)
            f.write('{} {} {} 关键词触发\n'.format(t_format,uid,message))
            f.close()
            return 0

    #涩图检测

    print('check ok')
    return 1

white_list=[2505455107]

#每日更新白名单
def run():
    print('whitelist initialize')
    global white_list
    white_list = [2505455107]
    print(white_list)
    timer = threading.Timer(86400,function = run)
    timer.start()

#禁言用户,传入 group_id&user_id&duration
def ban_user(gid,uid):
    t = time.gmtime()
    t_format = time.strftime("%Y-%m-%d", t)
    f = open(f'./{t_format}retract.txt', 'r')
    content = f.readlines()
    guilty_dict = {}
    #词典初始化
    for i in content:
        i = i.replace('\n','')
        i = i.split(' ')
        guilty_dict[i[1]] = 0

    #累加
    for i in content:
        i = i.replace('\n', '')
        i = i.split(' ')
        guilty_dict[i[1]] += 1

    #检查当日问题儿童并禁言:
    global white_list

    for guid,value in guilty_dict.items():
        guid = int(guid)
        if value > random.randint(3,5) and guid not in white_list:
            print(f'{guid} is guilty,die!')
            white_list.append(guid)
            df = pd.read_csv('ban_history.csv', index_col=['id'])
            try:
                df.loc[guid, '次数'] += 1
                df.loc[guid, '时长累积'] += 43200
                df.to_csv('ban_history.csv', index_label='id')
            except KeyError:
                new = pd.DataFrame({'次数': 1, '时长累积': 43200}, index=[guid])
                df = df.append(new)
                df.to_csv('ban_history.csv', index_label='id')
            duration = df.loc[guid, '时长累积']
            requests.get(url=f'http://127.0.0.1:5700/set_group_ban?group_id={gid}&user_id={guid}&duration={duration}')


# todo:动漫图片发送
def pic_sender(gid):
    path = f'./data/images/2022-10-08'
    pics = os.listdir(path)
    pic = random.sample(pics, 1)[0]
    requests.get(url = 'http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}'.format(gid, r'[CQ:image,' r'file=' + f'./2022-10-08/{pic}' + r']'))

# todo:gamemaster
def gamemaster_chat(gid):
    pass


# todo:重点信息汇总
