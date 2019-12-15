# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Form.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(898, 830)
        self.centralwidget = QtWidgets.QWidget(Form)
        self.centralwidget.setObjectName("centralwidget")
        self.screenLabel = ImageLabel(self.centralwidget)
        self.screenLabel.setGeometry(QtCore.QRect(420, 10, 191, 371))
        self.screenLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.screenLabel.setObjectName("screenLabel")
        self.actionLoadWidget = QtWidgets.QWidget(self.centralwidget)
        self.actionLoadWidget.setGeometry(QtCore.QRect(50, 180, 291, 251))
        self.actionLoadWidget.setObjectName("actionLoadWidget")
        self.widget = QtWidgets.QWidget(self.actionLoadWidget)
        self.widget.setGeometry(QtCore.QRect(10, 10, 271, 225))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.fileAddPushButton = QtWidgets.QPushButton(self.widget)
        self.fileAddPushButton.setObjectName("fileAddPushButton")
        self.horizontalLayout.addWidget(self.fileAddPushButton)
        self.fileRemovePushButton = QtWidgets.QPushButton(self.widget)
        self.fileRemovePushButton.setObjectName("fileRemovePushButton")
        self.horizontalLayout.addWidget(self.fileRemovePushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.taskTreeWidget = QtWidgets.QTreeWidget(self.widget)
        self.taskTreeWidget.setObjectName("taskTreeWidget")
        self.verticalLayout.addWidget(self.taskTreeWidget)
        self.widget1 = QtWidgets.QWidget(self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(60, 70, 271, 112))
        self.widget1.setObjectName("widget1")
        self.gridLayout = QtWidgets.QGridLayout(self.widget1)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.adbTestPushButton = QtWidgets.QPushButton(self.widget1)
        self.adbTestPushButton.setObjectName("adbTestPushButton")
        self.gridLayout.addWidget(self.adbTestPushButton, 0, 0, 1, 1)
        self.getScreenShotPushButton = QtWidgets.QPushButton(self.widget1)
        self.getScreenShotPushButton.setObjectName("getScreenShotPushButton")
        self.gridLayout.addWidget(self.getScreenShotPushButton, 0, 1, 1, 1)
        self.returnHomePushButton = QtWidgets.QPushButton(self.widget1)
        self.returnHomePushButton.setObjectName("returnHomePushButton")
        self.gridLayout.addWidget(self.returnHomePushButton, 1, 0, 1, 1)
        self.returnPushButton = QtWidgets.QPushButton(self.widget1)
        self.returnPushButton.setObjectName("returnPushButton")
        self.gridLayout.addWidget(self.returnPushButton, 1, 1, 1, 1)
        self.recordActionPushButton = QtWidgets.QPushButton(self.widget1)
        self.recordActionPushButton.setCheckable(True)
        self.recordActionPushButton.setChecked(True)
        self.recordActionPushButton.setObjectName("recordActionPushButton")
        self.gridLayout.addWidget(self.recordActionPushButton, 2, 0, 1, 1)
        self.actionStartPushButton = QtWidgets.QPushButton(self.widget1)
        self.actionStartPushButton.setObjectName("actionStartPushButton")
        self.gridLayout.addWidget(self.actionStartPushButton, 3, 0, 1, 1)
        self.taskStopPushButton = QtWidgets.QPushButton(self.widget1)
        self.taskStopPushButton.setObjectName("taskStopPushButton")
        self.gridLayout.addWidget(self.taskStopPushButton, 3, 1, 1, 1)
        Form.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Form)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 898, 23))
        self.menubar.setObjectName("menubar")
        Form.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Form)
        self.statusbar.setObjectName("statusbar")
        Form.setStatusBar(self.statusbar)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "auto_mobile"))
        self.screenLabel.setText(_translate("Form", "图片显示区域"))
        self.fileAddPushButton.setText(_translate("Form", "添加"))
        self.fileRemovePushButton.setText(_translate("Form", "移除"))
        self.taskTreeWidget.headerItem().setText(0, _translate("Form", "任务列表"))
        self.adbTestPushButton.setText(_translate("Form", "测试连接"))
        self.getScreenShotPushButton.setText(_translate("Form", "获取屏幕"))
        self.returnHomePushButton.setText(_translate("Form", "返回桌面"))
        self.returnPushButton.setText(_translate("Form", "返回上一级"))
        self.recordActionPushButton.setText(_translate("Form", "开始录制动作"))
        self.actionStartPushButton.setText(_translate("Form", "开始执行"))
        self.taskStopPushButton.setText(_translate("Form", "任务终止"))
from ImageLabel import ImageLabel
