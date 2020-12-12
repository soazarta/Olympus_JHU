from PyQt5.QtWidgets import *
from src.Game import ROOMS

class ChoiceDialog(QDialog):

    def __init__(self, outputString: str, room=None, character=None, weapon=None, cards=None, parent=None):
        QDialog.__init__(self, parent)

        self.okButton = QPushButton("Ok")
        self.okButton.clicked.connect(self.close)

        self.text = QLabel(outputString)

        comboList = []

        if character is not None:
            self.charCombo = QComboBox()
            self.charCombo.setPlaceholderText("Choose a Character")
            self.charCombo.setCurrentIndex(-1)
            for c in character:
                self.charCombo.addItem(c)
            comboList.append(self.charCombo)

        if weapon is not None:
            self.weaponCombo = QComboBox()
            self.weaponCombo.setPlaceholderText("Choose a Weapon")
            self.weaponCombo.setCurrentIndex(-1)
            for w in weapon:
                self.weaponCombo.addItem(w)
            comboList.append(self.weaponCombo)

        if room is not None:
            self.roomCombo = QComboBox()
            self.roomCombo.setPlaceholderText("Choose a Room")
            self.roomCombo.setCurrentIndex(-1)
            for r in room:
                self.roomCombo.addItem(r)
            comboList.append(self.roomCombo)

        if cards is not None:
            self.cardsCombo = QComboBox()
            self.cardsCombo.setPlaceholderText("Choose a Card")
            self.cardsCombo.setCurrentIndex(-1)
            for c in cards:
                self.cardsCombo.addItem(c)
            comboList.append(self.cardsCombo)

        layout = QVBoxLayout()
        layout.addWidget(self.text)
        for c in comboList:
            layout.addWidget(c)
        layout.addWidget(self.okButton)
        self.setLayout(layout)
