import requests
import socket
import json

ListenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ListenSocket.bind(('localhost', 5701))
ListenSocket.listen(100)

HttpResponseHeader = '''HTTP/1.1 200 OK
Content-Type: text/html
'''

def request_to_json(msg):
    for i in range(len(msg)):
        if msg[i]=="{" and msg[-1]=="}":
            return json.loads(msg[i:])
    return None


def rev_msg():
    Client, Address = ListenSocket.accept()
    Request = Client.recv(1024).decode(encoding='utf-8')
    # print(Request)
    rev_json=request_to_json(Request)
    Client.sendall((HttpResponseHeader).encode(encoding='utf-8'))
    Client.close()
    return rev_json


data = {
    'user_id': 123456,# QQ号
    'message': '你好',# 消息内容
    'auto_escape': False
}
cq_url = "http://127.0.0.1:5700/send_private_msg"
rev = requests.post(cq_url, data=data)
print(rev.url)

if __name__ == '__main__':
    print('============start==================')
    while True:
        rev_msg = rev_msg()
        user_id = rev_msg.setdefault('user_id')
        raw_message = rev_msg.setdefault('raw_message')
        print(f'您收到了来自{user_id}的{raw_message}')
