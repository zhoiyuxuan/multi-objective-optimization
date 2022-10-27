from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader

import socket, threading
import time

IP = '127.0.0.1'
PORT = 9090
BUFLEN = 1024


class Stats:
    def __init__(self):
        self.ui = QUiLoader().load('ui/client.ui')
        self.ui.startbutton.clicked.connect(self.connect)
        self.ui.endbutton.clicked.connect(self.close)


    def connect(self):
        if self.ui.nameinfo.text() == '':
            self.ui.statuslabel.setText('请输入有效姓名')
        else:
            try:
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.connect((IP,PORT))
                self.ui.statuslabel.setText('登陆中...')
                data = self.s.recv(BUFLEN).decode('utf-8')
                time.sleep(2)#让服务器端开启线程
                self.ui.statuslabel.setText(data)
                if data == '登录失败':
                    self.s.close()
                    return 0
                else:

                        name = ' '+self.ui.nameinfo.text()
                        msg = f'{time.time()} {name}'
                        self.s.send(bytes(msg.encode('utf-8')))
                self.ui.startbutton.setEnabled(False)
                self.ui.endbutton.setEnabled(True)
            except ConnectionRefusedError:
                self.ui.statuslabel.setText('签到服务器端未开启，请联系周宁组长')



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
    stats = Stats()
    stats.ui.show()
    app.exec_()

