import socket,threading,time
from abc import ABCMeta, abstractmethod

#对于每个子socket，都有一个监听信息的线程，一个心跳线程

IP = '192.168.1.186'
PORT = 9090
BUFLEN = 1024

#抽象产品
class Socket(metaclass=ABCMeta):
    @ abstractmethod
    def socket_start(self): #监听连接
        pass

    @ abstractmethod
    def listen_msg(self, client): #监听发来的消息
        pass

    @ abstractmethod
    def send_msg(self, client,msg): #向哪个子socket传送什么msg
        pass

    @ abstractmethod
    def socket_close(self, client): #关闭哪个子socket
        pass

# 抽象工厂
class SocketFactory(metaclass=ABCMeta):
    @ abstractmethod
    def CreateFactory(self):
        pass

# 产品角色：
class ServerSocket(Socket):
    def __init__(self,IP,PORT):
        #socket参数
        self.ip = IP
        self.port = PORT
        #连接相关信息保存
        self.clients = [] #在线用户信息[clients]
        self.ips = [] #在线ip信息[ip]
        self.client2ip={} #clientsocket和ip的映射关系{client:ip}
        self.login_time = {} #记录在线人员登录时间{ip：logintime}
        self.ip2user ={} #建立用户和ip的映射{ip：user}

    #启动socket，可以同时进行多个连接
    def socket_start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.ip,self.port))
        server_socket.listen(100)
        print('server socket start')
        #启动等待连接进程
        t = threading.Thread(target=self.wait_connection,args=(server_socket,))
        t.start()

    def wait_connection(self,server_socket):
        while True: #true必须跟上阻塞函数
            socket.setdefaulttimeout(20)
            client, addr = server_socket.accept() #阻塞等待连接,建立一个新的套接字处理这个client

            if client in self.clients:
                print('老用户再次登录')
            elif addr[0] not in self.ips:
                print('新用户登录')
                #记录新用户信息到在线表
                self.client2ip[client]=addr[0]
                self.clients.append(client)
                self.ips.append(addr[0])
                #调用发送方法发送登录成功信息给client
                login_time = time.time()
                self.login_time[addr[0]] = login_time
                login_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(login_time))
                msg = f'登录成功:{login_time}'
                self.send_msg(client, msg)
                #开启监听线程，监听来自该client socket的所有信息
                self.listen_msg(client)

            else:
                msg = '同一台电脑两次登录，登陆失败'
                #发送登录失败信息给client
                print(msg)
                self.send_msg(client,msg)


    def send_msg(self,client,msg):
        client.send(bytes(msg.encode('utf-8')))
        if msg !='ack':
            print(f'send {msg} to {self.client2ip[client]}')

    '''
    监听信息：
    listen_msg:abstract 用于开启监听线程
    receiev_msg：监听线程，监听所有信息，传到deal_msg进一步处理
    deal_msg：处理receive_msg传来的信息
    '''

    def listen_msg(self, client):
        t = threading.Thread(target=self.receive_msg, args=(client,))
        t.start()
        print(f'listen message from {self.client2ip[client]} start')

    def receive_msg(self,client):
        while True:#必须有阻塞
            time.sleep(1)
            try:
                if client in self.clients:
                    data = client.recv(BUFLEN).decode('utf-8') #阻塞在这儿了
                    if data !='HEARTBEAT':
                        print(data,f'from {self.client2ip[client]}')
                    # 连接中止
                    if data == 'END':
                        # todo:记录用户时长
                        user = self.ip2user[self.client2ip[client]]
                        logout_time = time.time()
                        duration = logout_time - self.login_time[self.client2ip[client]]
                        login_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                                   time.localtime(self.login_time[self.client2ip[client]]))
                        logout_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(logout_time))

                        f = open('login.txt', 'a+')
                        f.write(f'{user} {login_time} {logout_time} {duration}\n')
                        f.close()

                        msg = '签到时长已记录'
                        self.send_msg(client, msg)
                        self.log_out(client)
                    # 心跳信息
                    elif data == 'HEARTBEAT':
                        msg = 'ack'
                        self.send_msg(client,msg)
                    # 连接开始
                    else:
                        try:#粘包情况，重新发送
                            name = data.split()[2]
                            self.send_msg(client,'服务器繁忙，请重试')
                        except:
                            name = data.split()[1]
                            self.ip2user[self.client2ip[client]] = name

            except BaseException as error:
                # todo:记录用户时长
                user = self.ip2user[self.client2ip[client]]
                logout_time = time.time()
                duration = logout_time- self.login_time[self.client2ip[client]]
                login_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(self.login_time[self.client2ip[client]]))
                logout_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(logout_time))

                f = open('login.txt', 'a+')
                f.write(f'{user} {login_time} {logout_time} {duration}\n')
                f.close()


                print('用户强制中断了一个连接')
                self.log_out(client)
                return

            except socket.timeout:
                print('用户超过20s没有发送心跳')
                #todo:记录用户时长
                user = self.ip2user[self.client2ip[client]]
                logout_time = time.time()
                duration = logout_time - self.login_time[self.client2ip[client]]
                login_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.login_time[self.client2ip[client]]))
                logout_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(logout_time))

                f = open('login.txt', 'a+')
                f.write(f'{user} {login_time} {logout_time} {duration}\n')
                f.close()

                self.send_msg(client,'pipebreak')
                self.log_out(client)
                return

            except:
                print('用户登录出错')
                # todo:记录用户时长
                user = self.ip2user[self.client2ip[client]]
                logout_time = time.time()
                duration = logout_time - self.login_time[self.client2ip[client]]
                login_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.login_time[self.client2ip[client]]))
                logout_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(logout_time))

                f = open('login.txt', 'a+')
                f.write(f'{user} {login_time} {logout_time} {duration}\n')
                f.close()

                self.send_msg(client, 'pipebreak')
                self.log_out(client)
                return


    #清除client在线信息并断开连接
    def log_out(self,client):
        if client in self.clients:
            #关闭连接
            self.socket_close(client)
            #清除用户在线信息
            ip = self.client2ip[client]
            self.clients.remove(client)
            self.ips.remove(ip)
            del self.client2ip[client]
            del self.login_time[ip]
            del self.ip2user[ip]


    def socket_close(self, client):
        client.close()
        print(f'client socket {self.client2ip[client]} closed')




#产品工厂
class ServerSocketFactory(SocketFactory):
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port

    @property
    def CreateFactory(self):
        return ServerSocket(self.ip,self.port)

def online_members(server_socket):
    while 1:
        print(f'当前在线人数{len(server_socekt.clients)}')
        time.sleep(5)

#实例化
if __name__ == '__main__':
    server_socekt = ServerSocketFactory(IP,PORT).CreateFactory
    server_socekt.socket_start()
    t1 = threading.Thread(target=online_members(server_socekt))
    t1.start()

    # while 1:
    #     choice = input('查看当前在线人员：(1,2)')
    #     if choice == '1':
    #         print(server_socekt.ip2user)
    #     elif choice == '2':
    #         print(server_socekt)
    #     else:
    #         pass
