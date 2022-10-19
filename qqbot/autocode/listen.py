import time

from flask import Flask, request

'''注意，这里的import api是另一个py文件，下文会提及'''
import api
import threading
import banword_list

app = Flask(__name__)

'''监听端口，获取QQ信息'''

@app.route('/', methods=["POST"])
def post_data():
    msg = request.get_json()
    uid = msg.get('user_id') #发送信息者qq号码
    mid = msg.get('message_id') #信息号码
    gid = msg.get('group_id') #群聊号码
    raw_message = msg.get('raw_message') #信息内容
    # time_current = time.time()
    # global time0
    # global lasttime
    # if time_current - time0 >86400:
    #     lasttime = time0
    #     time0 = time_current

    '下面的request.get_json().get......是用来获取关键字的值用的，关键字参考上面代码段的数据格式'
    if msg.get('message_type') == 'private':  # 如果是私聊信息
        api.keyword(raw_message, uid)  # 将 Q号和原始信息传到我们的后台

    if msg.get('message_type') == 'group':  # 如果是群聊信息
        api.keyword(raw_message, uid, gid, mid)  # 将Q号和原始信息传到我们的后台

    return 'OK'

if __name__ == '__main__':
    t1 = threading.Timer(1,function = api.run)
    t1.start()
    app.run(debug=True, host='127.0.0.1', port=5701)  # 此处的 host和 port对应上面 yml文件的设置

