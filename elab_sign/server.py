import socket
# 建立socket，监听连接信息，如果是科中网段的允许链接，否则干下线
# 每天0：00所有人干下线
import threading
import datetime
import time

IP = '192.168.1.227'
PORT = 9090
BUFLEN = 1024


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((IP, PORT))
server_socket.listen(100)
print('启动连接')

ips=[]
clients = []
login_info={}
addr_user={}

def init():
    while True:
        client, addr = server_socket.accept()  # 阻塞线程
        if client in clients:
            print('老用户二次加入')
        elif addr[0] not in ips:
            print('新用户加入', addr)
            clients.append(client)
            ips.append(addr[0])
            current_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
            client.send(bytes(f'登录成功 {current_time}'.encode('utf-8')))
            r = threading.Thread(target=receive_msg, args=(client,addr,))
            r.start()
        #todo:同一台电脑不能登录2次
        else:
            print('同一台电脑两次登录，登录失败')
            client.send(bytes('登录失败'.encode('utf-8')))


def receive_msg(client,addr):
    while True:
        time.sleep(1)
        try:
            if client in clients:
                data = client.recv(BUFLEN).decode('utf-8')
                #如果是结束信息
                if data == "END":

                    exit_time = time.time()
                    user = addr_user[addr]
                    duration = exit_time - login_info[user]
                    exit_date = time.strftime("%Y-%m-%d", time.localtime(exit_time))
                    login_date = time.strftime("%Y-%m-%d", time.localtime(login_info[user]))
                    exit_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(exit_time))
                    last_login = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(login_info[user]))
                    print(f'用户{addr}退出了,退出时间为{exit_time},本次登录时长{duration}')

                    #todo：如果是同一天发生的，那么此次登录时间写入日志
                    if exit_date == login_date:
                        f = open('login.txt', 'a+')
                        f.write(f'{user} {last_login} {exit_time} {duration}\n')
                        f.close()
                        clients.remove(client)
                        ips.remove(addr[0])
                        hour = int(duration/3600)
                        min = int(duration%3600/60)
                        second = int(duration%60)
                        client.send(bytes(f'记录成功 {hour}:{min}:{second}'.encode('utf-8')))
                        return #释放线程

                    else:
                        print(f'{user} 挂机超过1天，不予记录')
                        client.send(bytes('挂机超过1天，不予记录'.encode('utf-8')))
                        clients.remove(client)
                        ips.remove(addr[0])
                        return  # 释放线程

                # 不是退出信息的话,就是登录信息
                else:
                    login_time = float(data.split()[0])
                    user = data.split()[1]
                    login_info[user]=login_time
                    addr_user[addr]=user
                    login_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(login_time))
                    print(f'{addr}{user} 登录时间为：{login_time}')


    #如果是强制退出了：
        except BaseException as error:

            print('用户强制中断了一个链接')
            if client in clients:
                exit_time = time.time()
                user = addr_user[addr]
                duration = exit_time - login_info[user]
                exit_date = time.strftime("%Y-%m-%d", time.localtime(exit_time))
                login_date = time.strftime("%Y-%m-%d", time.localtime(login_info[user]))
                exit_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(exit_time))
                last_login = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(login_info[user]))
                print(f'用户{addr}退出了,退出时间为{exit_time},本次登录时长{duration}')

                # todo：如果是同一天发生的，那么此次登录时间写入日志
                if exit_date == login_date:
                    #写日志
                    f = open('login.txt', 'a+')
                    f.write(f'{user} {last_login} {exit_time} {duration}\n')
                    f.close()
                    clients.remove(client)
                    ips.remove(addr[0])
                else:
                    print(f'{user} 挂机超过1天，不予记录')
                    clients.remove(client)
                    ips.remove(addr[0])


t1 = threading.Thread(target=init)
t1.start()

while True:
    print(f'当前在线人数为 {len(clients)}')
    time.sleep(5)
