import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QFileDialog, QTreeWidgetItem
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
from Form import Ui_Form
from ActionManage import ActionManage
from MobileActionExecThread import MobileActionExecThread
import time
import json


class MainWindow(QMainWindow):
    screenSize = (1080, 2340)  # 截屏大小
    resizeRatio = 3  # 缩放比例
    am = ActionManage()
    t_temp = time.perf_counter()
    delay_time = 500
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # QtCore.QMetaObject.connectSlotsByName(self)

        self.screenShowSize = QSize(self.screenSize[0]/self.resizeRatio, self.screenSize[1]/self.resizeRatio)

        # 对imageLabel读图片的路径进行初始化
        self.ui.screenLabel.setImagePath('./image/resized_screen.png')

        self.ui.screenLabel.resize(self.screenShowSize)
        self.ui.screenLabel.setPixmap(QPixmap("./image/1.jpg"))

        self.ui.screenLabel.mousePressSignal.connect(self.imageLabelPressSlot)
        self.ui.screenLabel.mouseDragSignal.connect(self.imageLabelDragSlot)

    # 获取截屏并显示
    @QtCore.pyqtSlot()
    def on_getScreenShotPushButton_clicked(self):
        os.system("adb shell /system/bin/screencap -p /sdcard/screen.png")
        time.sleep(0.5)
        os.system("adb pull /sdcard/screen.png ./image/screen.png")
        sp = QPixmap("./image/screen.png")
        sp = sp.scaled(self.screenShowSize)
        sp.save('./image/resized_screen.png')
        self.ui.screenLabel.showImage()

    # 处理屏幕点击事件
    def imageLabelPressSlot(self, x, y):
        x = self.resizeRatio * x
        y = self.resizeRatio * y
        print('按下{x},{y}'.format(x=x, y=y))
        os.system('adb shell input tap {x} {y}'.format(x=x, y=y))
        if self.ui.recordActionPushButton.isChecked() == False:
            self.am.addClickAction([x,y])
            self.addDelayRecord()
        self.on_getScreenShotPushButton_clicked()

    # 处理屏幕滑动事件
    def imageLabelDragSlot(self, x1, y1, x2, y2, t):
        x1 = self.resizeRatio * x1
        y1 = self.resizeRatio * y1
        x2 = self.resizeRatio * x2
        y2 = self.resizeRatio * y2
        print('从({x1},{y1}) 拖到({x2},{y2}) ，时间({t})'.format(x1=x1, y1=y1,x2=x2, y2=y2,t=t))
        os.system('adb shell input swipe {x1} {y1} {x2} {y2} {t}'.format(x1=x1, y1=y1,x2=x2, y2=y2,t=t))
        if self.ui.recordActionPushButton.isChecked() == False:
            self.am.addDragAction([x1,y1,x2,y2,t])
            self.addDelayRecord()
        self.on_getScreenShotPushButton_clicked()

    # 发送返回键
    @QtCore.pyqtSlot()
    def on_returnPushButton_clicked(self):
        os.system('adb shell input keyevent 4')
        if self.ui.recordActionPushButton.isChecked() == False:
            self.am.addPressReturnAction()
            self.addDelayRecord()

    # 发送回到home
    @QtCore.pyqtSlot()
    def on_returnHomePushButton_clicked(self):
        os.system('adb shell input keyevent 3')
        if self.ui.recordActionPushButton.isChecked() == False:
            self.am.addPressHomeAction()
            self.addDelayRecord()

    # 录制动作
    @QtCore.pyqtSlot()
    def on_recordActionPushButton_clicked(self):
        if self.ui.recordActionPushButton.isChecked():
            self.ui.recordActionPushButton.setText('开始录制')
            print("checked")
            self.am.recordActionSetFinish()
        else:
            print('unchecked')
            filename, ok = QInputDialog.getText(self,'', '输入文件名')
            if ok:
                self.ui.recordActionPushButton.setText('停止录制')
                print(filename)
                # 开始录制动作
                self.am.recordActionSetStart(filename)
                self.t_temp = time.perf_counter()
            else:
                self.ui.recordActionPushButton.setChecked(True)

    # 点击添加文件
    @QtCore.pyqtSlot()
    def on_fileAddPushButton_clicked(self):
        path, _ = QFileDialog.getOpenFileName(self,'打开文件','../mobile_action','(*.json)')
        filename = path.split('/')[-1].split('.')[0]
        print(filename)
        item = QTreeWidgetItem(self.ui.taskTreeWidget)
        item.setText(0, filename)

    # 点击移除
    @QtCore.pyqtSlot()
    def on_fileRemovePushButton_clicked(self):
        root = self.ui.taskTreeWidget.invisibleRootItem()
        for item in self.ui.taskTreeWidget.selectedItems():
            (item.parent() or root).removeChild(item)

    # 点击开始
    @QtCore.pyqtSlot()
    def on_actionStartPushButton_clicked(self):
        name_list = []
        for item in self.ui.taskTreeWidget.findItems("", Qt.MatchStartsWith):
            name_list.append(item.text(0))

        self.mt = MobileActionExecThread()
        self.mt.setFileNames(name_list)
        self.mt.run()

    # 点击测试连接
    @QtCore.pyqtSlot()
    def on_adbTestPushButton_clicked(self):
        os.system('adb devices')

    # 点击任务终止
    @QtCore.pyqtSlot()
    def on_taskStopPushButton_clicked(self):
        self.mt.terminate()

    # 记录两次动作时，把动作间的时间也记录进去
    def addDelayRecord(self):
        t = int((time.perf_counter() - self.t_temp) * 1000)
        self.t_temp = time.perf_counter()
        self.am.addDelayAction(t)

    # 执行动作组，输入是文件名的list，不包含扩展名
    def mobile_action_exec(self, name):
        try:
            with open('../mobile_action/'+name+'.json') as f:
                action_data = json.load(f)
                print('action set name:{}'.format(action_data['action set name']))
                for action in action_data['action set']:
                    if action['action name'] == 'delay':
                        time.sleep(float(action['param'])/1000)
                    else:
                        os.system(action['cmd'])
        except:
            print('打开文件{}失败'.format(name))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
