from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from PyQt5 import QtGui
import time


class ImageLabel(QLabel):
    mousePressSignal = pyqtSignal(int, int)
    mouseDragSignal = pyqtSignal(int, int, int, int, int)

    def __init__(self, parent=None):
        super(ImageLabel, self).__init__(parent)

    def setImagePath(self, imagePath):
        self.imagePath = imagePath

    def showImage(self):
        sp = QPixmap(self.imagePath)
        self.setPixmap(sp)

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.pressX = ev.x()
        self.pressY = ev.y()
        self.currentTime = time.perf_counter()

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
        if self.pressX == ev.x() and self.pressY == ev.y():
            # 按下和松开是一个地方，点击事件
            self.mousePressSignal.emit(ev.x(), ev.y())
        else:
            # 按下和松开不是一个地方，拖拽事件
            clock = time.perf_counter()
            time_diff = int((clock - self.currentTime)*1000)  # 毫秒计时
            self.mouseDragSignal.emit(self.pressX, self.pressY, ev.x(), ev.y(), time_diff)
