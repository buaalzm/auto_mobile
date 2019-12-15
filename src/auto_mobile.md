
# 背景介绍

这是一个从今年双十一时候产生的一个想法，好多平台上都有很多羊毛可以薅，每天签到啊什么的，然后每天去点就很烦，希望做一个自动化的小工具去让程序去自动完成各种签到，浏览什么的。

正好赶上崴脚下不了地，只能宅在宿舍，而且最难的最优化也考完了，就利用这段时间把这个想法实现了一下。

程序应包含如下几个功能

1. 有一个窗口专门用来显示手机的屏幕，在这个窗口上的点击和滑动应该能映射到手机的点击和滑动。并且由于手机屏幕的分辨率太高了，这里还有一个缩放映射的问题。
2. 各种手机的操作可以录成一个动作组，基本的动作包含：点击，滑动，延时，返回键，home键。录制的动作组应以一定格式存储在文件中，并方便编辑
3. 针对不同的任务，记录不同的动作文件，动作文件导入后应可以批量执行

程序上传到了：https://github.com/buaalzm/auto_mobile  
博客连接：https://blog.csdn.net/qq_33833073/article/details/103553273

# 项目概述

主要功能应有如下几个

1. 屏幕显示
2. 动作录制与存储
3. 动作加载与执行

其中，用电脑操作手机使用adb工具，GUI设计使用PyQt5，动作文件的存储使用json格式

---
# 使用说明

- 点击测试连接，在命令行中会输出devices信息，有设备号则表示连上了
- 点击获取屏幕，获得一张手机的截图并显示在窗口中
- 返回桌面和返回上一级按钮映射到手机对应的操作
- 在显示手机屏幕的地方上面点击或滑动，会映射到手机对应的操作，并获取一张新的截图
- 点击开始录制按钮之后，弹出对话框输入要保存的文件名（不需要加扩展名），在电脑端对手机的操作会被记录下来，点击停止录制，记录的动作保存到../mobile_action目录中，以json文件存储
- 添加和删除按钮是对动作文件进行操作，编辑要执行的动作组，待执行的动作会显示到下方的TreeWidget中
- 点击开始执行，即执行TreeWidget中显示的动作组

 
# 详细设计

## 提升一个类用于图像显示

设计一个ImageLabel类专门用于图像显示，以及鼠标事件的拦截

### 提升类的操作

新建一个ImageLabel.py文件，在里面编写ImageLabel类，继承QLabel  
初始化时传递一个图片的路径，通过showImage函数显示图片


```python
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel


class ImageLabel(QLabel):
    showImageSignal = pyqtSignal()

    def __init__(self, parent=None):
        super(ImageLabel, self).__init__(parent)

    def setImagePath(self, imagePath):
        self.imagePath = imagePath

    def showImage(self):
        sp = QPixmap(self.imagePath)
        self.setPixmap(sp)
```

编写好这个类之后，在QTdesigner中新建一个label，右键提升类。提升类的时候

- 类名写定义的类名
- 文件写定义的文件名，把.h删掉

这样就可以使用自己定义的提升类模块了

## 处理与数据存取

在ActionMaganage类中，完成了各种动作的管理。包括描述的5种动作的存储和读取，不同的动作，存储的参数不太一样。比如，点击就需要x，y两个参数，延时需要一个时间参数，拖拽需要两个坐标一个时间，一共五个参数

程序如下：

```
import json


class ActionManage():
    tempAction = {}
    def recordActionSetStart(self, actionSetName):
        self.tempAction = {'action set name': actionSetName, 'action set': []}

    def addClickAction(self, position):
        if len(position)<2:
            print('parameter error')
            return
        action = {'action name':'click'}
        action['param'] = position
        action['cmd'] = 'adb shell input tap {x} {y}'.format(x=position[0], y=position[1])
        self.tempAction['action set'].append(action)

    def addDelayAction(self, delayTime):
        action = {'action name': 'delay'}
        action['param'] = delayTime
        self.tempAction['action set'].append(action)

    def addDragAction(self, paramlist):
        if len(paramlist)<5:
            print('parameter error')
            return
        action = {'action name': 'swipe'}
        action['param'] = paramlist
        action['cmd'] = 'adb shell input swipe {} {} {} {} {}'.format(*paramlist)
        self.tempAction['action set'].append(action)

    def addPressHomeAction(self):
        action = {'action name': 'home'}
        action['cmd'] ='adb shell input keyevent 3'
        self.tempAction['action set'].append(action)

    def addPressReturnAction(self):
        action = {'action name': 'return'}
        action['cmd'] = 'adb shell input keyevent 4'
        self.tempAction['action set'].append(action)

    def recordActionSetFinish(self):
        try:
            with open("../mobile_action/{name}.json".format(name=self.tempAction['action set name']), "w") as f:
                json.dump(self.tempAction, f)
        except:
            print('save file failed')

    def loadActionSet(self, filename):
        with open(filename) as f:
            data = json.load(f)
            return data['action set']
```

具体使用需要先初始化一个存储的文件名，然后往里面添加动作就可以了，就像这样：

```
if __name__ == '__main__':
    am = ActionManage()
    am.recordActionSetStart('test')
    am.addDelayAction(500)
    am.addClickAction([100,200])
    am.addDragAction([100,100,200,200,500])
    am.recordActionSetFinish()
    actionList = am.loadActionSet('../mobile_action/test.json')
    print(actionList)
```

## 动作执行

传入一个文件名的列表，即可顺序执行每个文件中存的动作。文件名是通过QFileDialog选到一个TreeWidget中的，省去了手动输入的麻烦，并且可以避免录入错误造成的文件无法读取。动作执行单独开一个线程MobileActionExecThread，使用时需要先初始化，传入文件名列表（不含扩展名，从treeWidget中自动获取），执行self.mt.run()即开始

程序：

```
from PyQt5.QtCore import QThread
import json
import time
import os


class MobileActionExecThread(QThread):
    def setFileNames(self, name_list):
        self.name_list = name_list

    def run(self):
        for name in self.name_list:
            try:
                with open('../mobile_action/' + name + '.json') as f:
                    action_data = json.load(f)
                    print('action set name:{}'.format(action_data['action set name']))
                    for action in action_data['action set']:
                        if action['action name'] == 'delay':
                            print('delay:{}'.format(action['param']))
                            time.sleep(float(action['param']) / 1000)
                        else:
                            print(action['cmd'])
                            os.system(action['cmd'])
            except:
                print('打开文件{}失败'.format(name))

```

具体使用：

```
self.mt = MobileActionExecThread()
    self.mt.setFileNames(name_list)
    self.mt.run()
```

## 主程序

这里主要是处理一些按钮和显示的事件，并调用各个子模块，将各个部分穿起来

```
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
```

## 一个小批处理程序

在记录的时候，有时候每个动作的间隔比较长，想把每个动作之间的延迟批量改小一点。于是编了一个小程序

```
import json
import sys


if __name__ == '__main__':
    filenamelist = sys.argv[1:]
    print(sys.argv)
    t = 500
    for filename in filenamelist:
        with open(filename) as f:
            data = json.load(f)
            for i, action in enumerate(data["action set"]):
                if data["action set"][i]["action name"] == 'delay':
                    data["action set"][i]["param"] = t
        try:
            with open(filename, "w") as f:
                json.dump(data, f)
        except:
            print('save file failed')
```

然后编写一个bat文件

```
python convert_delay.py %1
pause
```

这样就可以把待处理的文件直接拖到bat文件上，直接修改好