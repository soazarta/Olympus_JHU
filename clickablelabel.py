from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class ClickableLabel(QLabel):
    clicked = pyqtSignal()
    container = []
    LabelName = []

    def __init__(self, parent=None):
        QLabel.__init__(self, parent)
        self.setEnabled(False)

    def getRef(self, cont):
        self.container = cont

    def mousePressEvent(self, ev):
        self.container.selectedChar.setPixmap(self.pixmap())
        self.container.charInfo.setText(self.LabelName)
        self.container.selected = self.LabelName
        self.clicked.emit()
