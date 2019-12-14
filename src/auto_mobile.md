

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