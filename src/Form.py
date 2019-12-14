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
        Form.resize(898, 655)
        self.centralwidget = QtWidgets.QWidget(Form)
        self.centralwidget.setObjectName("centralwidget")
        self.screenLabel = ImageLabel(self.centralwidget)
        self.screenLabel.setGeometry(QtCore.QRect(460, 40, 191, 371))
        self.screenLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.screenLabel.setObjectName("screenLabel")
        self.getScreenShotPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.getScreenShotPushButton.setGeometry(QtCore.QRect(60, 70, 91, 23))
        self.getScreenShotPushButton.setObjectName("getScreenShotPushButton")
        self.returnHomePushButton = QtWidgets.QPushButton(self.centralwidget)
        self.returnHomePushButton.setGeometry(QtCore.QRect(170, 70, 75, 23))
        self.returnHomePushButton.setObjectName("returnHomePushButton")
        self.returnPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.returnPushButton.setGeometry(QtCore.QRect(260, 70, 75, 23))
        self.returnPushButton.setObjectName("returnPushButton")
        self.recordActionPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.recordActionPushButton.setGeometry(QtCore.QRect(60, 120, 101, 23))
        self.recordActionPushButton.setCheckable(True)
        self.recordActionPushButton.setChecked(True)
        self.recordActionPushButton.setObjectName("recordActionPushButton")
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
        self.getScreenShotPushButton.setText(_translate("Form", "获取屏幕"))
        self.returnHomePushButton.setText(_translate("Form", "返回桌面"))
        self.returnPushButton.setText(_translate("Form", "返回上一级"))
        self.recordActionPushButton.setText(_translate("Form", "开始录制动作"))
from ImageLabel import ImageLabel
