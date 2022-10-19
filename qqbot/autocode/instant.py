import requests

#回复信息
def reply():
    while True:
        print("'科中2020群': 789859340,'七域-线下课快乐~': 607575078,'七域の打ち師たち': 608768045,'七域校迎新一': 807183553, '七域23群-百团10.3': 829151493, 'testo': 484067856")
        gid = input('gid >>')
        msg = input('msg >>')
        requests.get(url=f'http://127.0.0.1:5700/send_group_msg?group_id={gid}&message={msg}')
        print(f'已向群({gid}) 发送 {msg}')
        con = input('continue(y/n):')
        while con == 'y':
            msg = input('msg >>')
            requests.get(url=f'http://127.0.0.1:5700/send_group_msg?group_id={gid}&message={msg}')
            print(f'已向群({gid}) 发送 {msg}')
            con = input('continue(y/n):')

#获得群聊列表
def get_group_list():
    group_list={}
    resp = requests.get(url=f'http://127.0.0.1:5700/get_group_list')
    groups = resp.json()['data']
    for g in groups:
        group_list[g['group_name']]=g['group_id']
    print('获取完成')

#设置群专属头衔
def set_group_special_title():
    gid = input('gid >>')
    uid = input('uid >>')
    title = input('stitle >>')
    duration = input('duration >> -1')
    requests.get(url=f'http://127.0.0.1:5700/set_group_special_title?group_id={gid}&user_id={uid}&duration={duration}&special_title={title}')
    print(f'已给群{gid} 成员{uid} 颁发头衔{title}')

#禁言用户
def set_group_ban():
    gid = input('gid >>')
    uid = input('uid >>')
    duration = input('duration >>')
    requests.get(url=f'http://127.0.0.1:5700/set_group_ban?group_id={gid}&user_id={uid}&duration={duration}')
    print(f'已给群{gid} 成员{uid} 禁言{duration}')

#群打卡
def send_group_sign():
    gid = input('gid >>')
    requests.get(url=f'http://127.0.0.1:5700/send_group_sign?group_id={gid}')

#群成员列表
def get_group_member_list():
    gid = input('gid >>')
    resp = requests.get(url=f'http://127.0.0.1:5700/get_group_member_list?group_id={gid}')
    groups = resp.json()['data']
    group_list ={}
    for g in groups:
        group_list[g['nickname']] = g['user_id']
    print(group_list)

#发送群公告
def send_group_notice():
    gid = input('gid >>')
    content = input('content >>')
    requests.get(
        url=f'http://127.0.0.1:5700/_send_group_notice?group_id={gid}&content={content}')

#撤回消息
def retract_msg():
    mid = input('mid >>')
    requests.get(url=f'http://127.0.0.1:5700/delete_msg?message_id={mid}')

def get_male_female_ratio():
    gid = input('gid >>')
    resp = requests.get(url=f'http://127.0.0.1:5700/get_group_member_list?group_id={gid}')
    groups = resp.json()['data']
    group_list = {}
    for g in groups:
        group_list[g['nickname']] = g['sex']

    female = 0
    male = 0
    unknown = 0
    for item, value in group_list.items():
        if value == 'female':
            female += 1
        elif value == 'male':
            male += 1
        else:
            unknown += 1
    print('male:', male, 'female:', female, 'unknown:', unknown)


def main():
    while True:
        print('请选择功能:\n'
              '1 回复信息\n'
              '2 获取群聊列表\n'
              '3 禁言用户\n'
              '4 设置群专属头衔\n'
              '5 群打卡\n'
              '6 群成员信息列表\n'
              '7 发送群公告\n'
              '8 撤回消息\n'
              '9 获得群男女比\n')
        try:
            choice = int(input('>>'))
        except:
            print('输入错误,请重新输入:')
            choice = int(input('>>'))

        if choice == 1:
            reply()
        elif choice == 2:
            get_group_list()
        elif choice == 3:
            get_group_list()
        elif choice == 4:
            set_group_special_title()
        elif choice == 5:
            send_group_sign()
        elif choice == 6:
            get_group_member_list()
        elif choice == 7:
            send_group_notice()
        elif choice == 8:
            retract_msg()
        elif choice == 9:
            get_male_female_ratio()
        else:
            print('input error')


if __name__ == '__main__':
    main()