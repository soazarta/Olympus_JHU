from PyQt5.QtWidgets import *
from src.Game import ROOMS

class ChoiceDialog(QDialog):

    def __init__(self, rooms, chars, parent=None):
        QDialog.__init__(self, parent)
        self.okButton = QPushButton("Ok")
        self.okButton.clicked.connect(self.close)
        self.roomCombo = QComboBox()
        for r in rooms:
            self.roomCombo.addItem(r)
        self.charCombo = QComboBox()
        for c in chars:
            self.charCombo.addItem(c)
        self.allRooms = QComboBox()
        for a in ROOMS:
            self.allRooms.addItem(a)
        layout = QVBoxLayout()
        layout.addWidget(self.roomCombo)
        layout.addWidget(self.charCombo)
        layout.addWidget(self.allRooms)
        layout.addWidget(self.okButton)
        self.setLayout(layout)
