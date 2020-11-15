from PyQt5.QtWidgets import *
from src.Game import ROOMS

class ChoiceDialog(QDialog):

    def __init__(self, room=None, character=None, weapon=None, parent=None):
        QDialog.__init__(self, parent)

        self.okButton = QPushButton("Ok")
        self.okButton.clicked.connect(self.close)
        comboList = []

        if character is not None:
            self.charCombo = QComboBox()
            for c in character:
                self.charCombo.addItem(c)
            comboList.append(self.charCombo)

        if weapon is not None:
            self.weaponCombo = QComboBox()
            for w in weapon:
                self.weaponCombo.addItem(w)
            comboList.append(self.weaponCombo)

        if room is not None:
            self.roomCombo = QComboBox()
            for r in room:
                self.roomCombo.addItem(r)
            comboList.append(self.roomCombo)

        layout = QVBoxLayout()
        for c in comboList:
            layout.addWidget(c)
        layout.addWidget(self.okButton)
        self.setLayout(layout)
