import socket,threading,time
from PySide2.QtWidgets import QApplication
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QIcon


IP = '192.168.1.186'
PORT = 9090
BUFLEN = 1024

heartbeat = False
login_time = 0
class Stats:
    def __init__(self):
        self.ui = QUiLoader().load('client.ui')
        self.ui.startbutton.clicked.connect(self.connect)
        self.ui.endbutton.clicked.connect(self.close)

    def connect(self):
        if self.ui.nameinfo.text() == '':
            self.ui.statuslabel.setText('请输入有效姓名')
        else:
            try:
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect((IP,PORT))
                data = self.client_socket.recv(BUFLEN).decode('utf-8')
                self.ui.statuslabel.setText(data)
                #被迫登录失败，关闭socket连接
                if data == '同一台电脑两次登录，登陆失败':
                    self.client_socket.close()
                #登录成功，发送登录信息
                else:
                    global login_time
                    login_time = time.time()
                    name = self.ui.nameinfo.text()
                    msg = f'{time.time()} {name}'
                    self.send_msg(msg)
                    #等1s避免粘包
                    time.sleep(1)
                    #启动监听线程
                    t1 = threading.Thread(target=self.receive_msg)
                    t1.start()
                    #启动心跳线程
                    t2 = threading.Thread(target=self.deal_heartbeat)
                    t2.start()
                    #设置按钮状态
                    self.ui.startbutton.setEnabled(False)
                    self.ui.endbutton.setEnabled(True)

            #主动登录失败，说明是服务器orip的问题
            except TimeoutError:
                self.ui.statuslabel.setText('连接超时，请确认IP是否正确')
                print('连接超时，请确认IP是否正确')
            except ConnectionRefusedError:
                self.ui.statuslabel.setText('服务器未启动，请联系周宁')
                print('服务器未启动，请联系周宁')

    def duration_count(self):
        duration = time.time()-login_time
        hour = int(duration / 3600)
        min = int(duration % 3600 / 60)
        second = int(duration % 60)
        return f' {hour} {min} {second}'

    def deal_heartbeat(self):
        while 1:
            time.sleep(5)
            try:
                self.send_msg('HEARTBEAT')
            #处理服务器断联
            except ConnectionResetError:
                self.ui.statuslabel.setText('服务器关闭连接,本次时间已记录',self.duration_count())
                self.ui.startbutton.setEnabled(True)
                self.ui.endbutton.setEnabled(False)
                return

    def receive_msg(self):
        while 1:
            time.sleep(1)
            try:
                data = self.client_socket.recv(BUFLEN).decode('utf-8')
                if data == '签到时长已记录':
                    self.ui.statuslabel.setText('本次时间已记录',self.duration_count())
                elif data =='pipebreak':
                    self.ui.statuslabel.setText('socket连接断开，时间已记录',self.duration_count())
                    self.ui.startbutton.setEnabled(True)
                    self.ui.endbutton.setEnabled(False)
                else:
                    self.ui.statuslabel.setText(data)
            #处理服务器突然断联
            except ConnectionResetError:
                self.ui.statuslabel.setText('服务器关闭连接,本次时间已记录',self.duration_count())
                self.ui.startbutton.setEnabled(True)
                self.ui.endbutton.setEnabled(False)
                return

    def send_msg(self,msg):
        self.client_socket.send(bytes(msg.encode('utf-8')))

    def close(self):
        msg = "END"
        self.send_msg(msg)
        time.sleep(2.5) #等关闭信息发过来
        self.client_socket.close()
        self.ui.startbutton.setEnabled(True)
        self.ui.endbutton.setEnabled(False)


if __name__ == '__main__':
    app = QApplication([])
    app.setWindowIcon(QIcon('elab.png'))
    stats = Stats()
    stats.ui.show()
    app.exec_()

