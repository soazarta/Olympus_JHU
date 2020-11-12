from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt


class ClueBoard(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        painter = QPainter(self)
        pixmap = QPixmap("QTDesigner/ClueBoard.jpg")
        painter.drawPixmap(self.rect(), pixmap)
        pen = QPen(Qt.red, 3)
        painter.setPen(pen)
        painter.drawEllipse(10,10, 100,100)
