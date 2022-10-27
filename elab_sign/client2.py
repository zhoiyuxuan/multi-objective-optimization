import socket, threading
import time

IP = '192.168.1.186'
PORT = 9090
BUFLEN = 1024


def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP,PORT))
    data = s.recv(BUFLEN).decode('utf-8')
    print(data)
    if data == '登录失败':
        s.close()
    else:
        name = ' 陈昊伟'
        msg = f'{time.time()} {name}'
        s.send(bytes(msg.encode('utf-8')))
    return s


def close(s):
    s.send(bytes('END'.encode('utf-8')))
    data = s.recv(BUFLEN).decode('utf-8')
    print(data)
    s.close()

s = connect()
time.sleep(20)
close(s)

