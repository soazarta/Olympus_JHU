from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt


class ClueBoard(QWidget):
    chars = []
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
        "Study_Hall": (320, 40),
        "Study_Library": (95, 185),
        "Hall_Lounge": (770, 40),
        "Hall_Billiard": (545, 185),
        "Lounge_Dinning": (995, 185),
        "Library_Billiard": (320, 320),
        "Library_Conservatory": (95, 465),
        "Billiard_Ballroom": (545, 465),
        "Billiard_Dinning": (770, 320),
        "Dinning_Kitchen": (995, 465),
        "Conservatory_Ballroom": (320, 600),
        "Ballroom_Kitchen": (770, 600)
    }

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

    def updateChars(self, state: str):
        allChars = state.splitlines()
        for s in allChars:
            self.chars.append(s.split(':'))
        print(self.chars)

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        painter = QPainter(self)
        pixmap = QPixmap("QTDesigner/ClueBoard.jpg")
        painter.drawPixmap(self.rect(), pixmap)
        for c in self.chars:
            brush = QBrush(self.CharacterColors[c[0]])
            painter.setBrush(brush)
            painter.drawEllipse(self.RoomPositions[c[1]][0], self.RoomPositions[c[1]][1], 65, 65)
