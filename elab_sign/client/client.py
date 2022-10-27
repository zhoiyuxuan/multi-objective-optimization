from PySide2.QtWidgets import QApplication
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QIcon

import socket,threading
import time

IP = '192.168.1.186'
PORT = 9090
BUFLEN = 1024


class Stats:
    def __init__(self):
        self.ui = QUiLoader().load('client.ui')
        self.ui.startbutton.clicked.connect(self.connect)
        self.ui.endbutton.clicked.connect(self.close)

    #发送心跳
    def send_heartbeat(self):
        while True:
            self.s.send(bytes('heartbeat'.encode('utf-8')))
            time.sleep(10)

    def connect(self):
        if self.ui.nameinfo.text() == '':
            self.ui.statuslabel.setText('请输入有效姓名')
        else:
            try:
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.connect((IP,PORT))

                #心跳线程启动
                t = threading.Thread(target=self.send_heartbeat)
                t.start()

                data = self.s.recv(BUFLEN).decode('utf-8')
                time.sleep(1)#让服务器端开启线程
                self.ui.statuslabel.setText(data)
                if data == '登录失败':
                    self.s.close()
                    return 0
                else:
                    name = self.ui.nameinfo.text()
                    msg = f'{time.time()} {name}'
                    self.s.send(bytes(msg.encode('utf-8')))
                self.ui.startbutton.setEnabled(False)
                self.ui.endbutton.setEnabled(True)
            except ConnectionRefusedError:
                self.ui.statuslabel.setText('不在科中范围or签到服务器端未开启')

    def close(self):
        self.s.send(bytes('END'.encode('utf-8')))
        data = self.s.recv(BUFLEN).decode('utf-8')
        print(data)
        self.ui.statuslabel.setText(data)
        self.s.close()
        self.ui.startbutton.setEnabled(True)
        self.ui.endbutton.setEnabled(False)


if __name__ == '__main__':
    app = QApplication([])
    app.setWindowIcon(QIcon('elab.png'))
    stats = Stats()
    stats.ui.show()
    app.exec_()

