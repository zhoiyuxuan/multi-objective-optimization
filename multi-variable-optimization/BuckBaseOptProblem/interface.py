from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
from PySide2 import QtCore
import sys,os

class MainWindow:

    def __init__(self):
        # 从文件中加载UI定义
        # 从 UI 定义中动态 创建一个相应的窗口对象
        self.ui = QUiLoader().load('ui/interface.ui')

        # 显示参数两个按钮
        self.ui.ParaDescribe.clicked.connect(self.ShowInputInfo)
        self.ui.ParaDescribe2.clicked.connect(self.ShowFormulaInfo)

        #运行 ： 1 传递字典参数 2 运行程序
        self.ui.RunButton.clicked.connect(self.runOptimization)

    def ShowInputInfo(self):
        QMessageBox.about(self.ui,
                    '输入参数说明',
        f'''\n
            OD：磁芯外径\n
            ID：磁芯内径\n
            HT：磁芯高度\n
            a,b,c,x：磁场强度——磁感应强度拟合数据\n
            g,h,j：磁损与磁感应强度、频率的拟合数据\n
            LE：有效磁路长度(mm)\n
            AL：一圈电感量\n'''
                    )

    def ShowFormulaInfo(self):
        QMessageBox.about(self.ui,
                          '输入参数说明',
                          f'''\n
                    Rin：输入端导通阻抗\n
                    Rout：输出端导通阻抗\n
                    Rhds：高侧场效应管电阻\n
                    RLds：低侧场效应管导通电阻\n
                    Vin：输入电压\n
                    Vout：输出电压\n
                    tdead：死区时间\n
                    ttr：上升下降时间\n
                    Qg：栅极电荷\n
                    rc：电容esr\n
                    d：漆包线直径\n
                    VDD：驱动供电\n'''
                          )

    def runOptimization(self):
        print('run exe')
        #获得所有参数字典
        dict = {}
        try:
            # 输入参数
            if self.ui.ODEdit.text() != '':
                dict['OD'] = float(self.ui.ODEdit.text())
            if self.ui.IDEdit.text() != '':
                dict['ID'] = float(self.ui.IDEdit.text())
            if self.ui.HTEdit.text() != '':
                dict['HT'] = float(self.ui.HTEdit.text())
            if self.ui.aEdit.text() != '':
                dict['a'] = float(self.ui.aEdit.text())
            if self.ui.bEdit.text() != '':
                dict['b'] = float(self.ui.bEdit.text())
            if self.ui.cEdit.text() != '':
                dict['c'] = float(self.ui.cEdit.text())
            if self.ui.eEdit.text() != '':
                dict['e'] = float(self.ui.eEdit.text())
            if self.ui.xEdit.text() != '':
                dict['qa'] = float(self.ui.xEdit.text())
            if self.ui.gEdit.text() != '':
                dict['g'] = float(self.ui.gEdit.text())
            if self.ui.hEdit.text() != '':
                dict['h'] = float(self.ui.hEdit.text())
            if self.ui.jEdit.text() != '':
                dict['j'] = float(self.ui.jEdit.text())
            if self.ui.ALEdit.text() != '':
                dict['AL'] = float(self.ui.ALEdit.text())
            if self.ui.LEEdit.text() != '':
                dict['LE'] = float(self.ui.LEEdit.text())
            if self.ui.VEEdit.text() != '':
                dict['VE'] = float(self.ui.VEEdit.text())

            # 公式参数
            if self.ui.RinEdit.text() != '':
                dict['Rin'] = float(self.ui.RinEdit.text())
            if self.ui.RoutEdit.text() != '':
                dict['Rout'] = float(self.ui.RoutEdit.text())
            if self.ui.RhdsEdit.text() != '':
                dict['Rhds'] = float(self.ui.RhdsEdit.text())
            if self.ui.RLdsEdit.text() != '':
                dict['RLds'] = float(self.ui.RLdsEdit.text())
            if self.ui.VinEdit.text() != '':
                dict['Vin'] = float(self.ui.VinEdit.text())
            if self.ui.VoutEdit.text() != '':
                dict['Vout'] = float(self.ui.VoutEdit.text())
            if self.ui.tdeadEdit.text() != '':
                dict['tdead'] = float(self.ui.tdeadEdit.text())
            if self.ui.ttrEdit.text() != '':
                dict['ttr'] = float(self.ui.ttrEdit.text())
            if self.ui.QgEdit.text() != '':
                dict['Qg'] = float(self.ui.QgEdit.text())
            if self.ui.rcEdit.text() != '':
                dict['rc'] = float(self.ui.rcEdit.text())
            if self.ui.dEdit.text() != '':
                dict['d'] = float(self.ui.dEdit.text())
            if self.ui.VDDEdit.text() != '':
                dict['VDD'] = float(self.ui.VDDEdit.text())

            # 算法参数
            if self.ui.popsizeEdit.text() != '':
                dict['pop_size'] = float(self.ui.popsizeEdit.text())
            if self.ui.iterEdit.text() != '':
                dict['iter'] = float(self.ui.iterEdit.text())

            # 电流参数
            if self.ui.IEdit.text() != '':
                dict['I'] = float(self.ui.IEdit.text())

        except ValueError as result:
            wrong_info = 'ValueError: ' + str(result)
            QMessageBox.about(self.ui,
                              '错误信息：', wrong_info)
        finally:
            print(dict)



if __name__ == '__main__':
    os.environ["QT_MAC_WANTS_LAYER"] = '1'
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QApplication([])
    mainWindow = MainWindow()
    mainWindow.ui.show()
    app.exec_()