from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from src.models import Player


class ClueBoard(QWidget):
    chars = dict()
    CharacterColors = {
        "Mrs. White": Qt.gray,
        "Mr. Green": Qt.green,
        "Mrs. Peacock": Qt.blue,
        "Professor Plum": QColor(220, 42, 255),
        "Miss Scarlet": Qt.red,
        "Colonel Mustard": Qt.yellow
    }
    RoomPositions = {
        "Study": (95, 40),
        "Hall": (545, 40),
        "Lounge": (995, 40),
        "Library": (95, 320),
        "Billiard Room": (545, 320),
        "Dinning Room": (995, 320),
        "Conservatory": (95, 600),
        "Ballroom": (545, 600),
        "Kitchen": (995, 600),
        "Study-Hall": (320, 40),
        "Study-Library": (95, 185),
        "Hall-Lounge": (770, 40),
        "Hall-Billiard": (545, 185),
        "Lounge-Dinning": (995, 185),
        "Library-Billiard": (320, 320),
        "Library-Conservatory": (95, 465),
        "Billiard-Ballroom": (545, 465),
        "Billiard-Dinning": (770, 320),
        "Dinning-Kitchen": (995, 465),
        "Conservatory-Ballroom": (320, 600),
        "Ballroom-Kitchen": (770, 600)
    }

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

    def updateChars(self, state: str):
        for s in state.splitlines():
            self.chars[s.split(':')[0]] = s.split(':')[1]

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        painter = QPainter(self)
        pixmap = QPixmap("QTDesigner/ClueBoard.jpg")
        painter.drawPixmap(self.rect(), pixmap)
        for c in self.chars.items():
            brush = QBrush(self.CharacterColors[c[0]])
            painter.setBrush(brush)
            painter.drawEllipse(self.RoomPositions[c[1]][0], self.RoomPositions[c[1]][1], 65, 65)
