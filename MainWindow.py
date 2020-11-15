import sys
from PyQt5 import uic
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *
from QTRecources import characters_rc
from QTRecources import Title_rc
from QTRecources import GameBoard_rc
from clickablelabel import *
from clueboard import *
import socket
import threading
import time
import src.Game as Game
import ChoiceDialog
import pickle

from src.messages import *
from src.options import *


HOST = "localhost"
PORT = 54321


class GameBoard(QWidget):
    waitingScreen = []
    movie = []
    waiting = True
    input = False
    chosenAction = None
    response = None
    currentOptions = []
    res = dict()
    currentData = []
    charAvatar = {
        "Mrs. White": "QTDesigner/MadameWhite.jpg",
        "Mr. Green": "QTDesigner/LordGreen.jpg",
        "Mrs. Peacock": "QTDesigner/DamePeacock.jpg",
        "Professor Plum": "QTDesigner/ProfPlum.jpg",
        "Miss Scarlet": "QTDesigner/MlleScarlet.jpg",
        "Colonel Mustard": "QTDesigner/ColMustard.jpg"
    }


    def __init__(self):
        super().__init__()
        uic.loadUi("QTDesigner/GameBoard.ui", self)
        self.setFixedSize(self.size())
        self.movie = QMovie("QTDesigner/ClueLoadingScreen.gif")
        self.waitingScreen = QLabel()
        self.waitingScreen.setMovie(self.movie)
        # creating a timer object
        self.timer = QTimer()
        # adding action to timer
        self.timer.timeout.connect(self.Waiting)
        # update the timer every tenth second
        self.timer.start(100)
        self.LockIn.clicked.connect(self.SetAction)

    def setAvatar(self, character):
        pixMap = QPixmap(self.charAvatar[character])
        self.CharAvatar.setPixmap(pixMap)

    def Waiting(self):
        if self.isVisible():
            if self.waiting:
                self.movie.start()
                self.waitingScreen.show()
                self.setEnabled(False)
            elif not self.waiting:
                self.movie.stop()
                self.waitingScreen.hide()
                self.setEnabled(True)

    def getMove(self, options) -> dict:
        # Set current options
        self.currentOptions = options
        while not self.input:
            pass
        self.input = False
        return self.res

    def SetAction(self):
        option = self.OptionCombo.currentText()

        if option == MOVE:
            b = ChoiceDialog.ChoiceDialog(self.currentData[option])
            b.exec()
            self.response = Move(b.roomCombo.currentText())
        '''
        if option == SUGGESTION:
            character = menu("Character?", data[option]["characters"])
            weapon = menu("Weapon?", data[option]["weapons"])
            # Can only accuse in the room you're in, sending data anyways
            room = data[option]["rooms"]
            self.response = Suggestion(character, weapon, room)

        if option == ACCUSATION:
            character = menu("Character?", data[option]["characters"])
            weapon = menu("Weapon?", data[option]["weapons"])
            room = menu("Room?", data[option]["rooms"])
            self.response = Accusation(character, weapon, room)

        if option == SHOW_CARD:
            if not data[option]["cards"]:
                print("No matching cards to show")
                self.response = ShowCard(None)
            else:
                card = menu(f"Card to show to {data[option]['player']}", data[option]["cards"])
                self.response = ShowCard(card)

        if option == END:
            self.response = End()
        '''

    def PopulateOptions(self, data):
        self.currentData = data
        options = list(data.keys())
        self.response = None
        self.OptionCombo.clear()
        for o in options:
            self.OptionCombo.addItem(o)

    def getResponse(self) -> str:
        while self.response is None:
            pass
        return self.response

        '''
        rooms = self.currentOptions[Option.Move_Room_Make_Suggestion]["Rooms"]
        suggestions = self.currentOptions[Option.Move_Room_Make_Suggestion]["Suggestions"]
        b = ChoiceDialog.ChoiceDialog(rooms, suggestions)
        b.exec()
        print("!!!!!!!")
        print(b.charCombo.currentText())
        print(b.roomCombo.currentText())
        print(b.allRooms.currentText())
        print("!!!!!!!")
        self.res["Room"] = b.roomCombo.currentText()
        self.res["Suggestion"] = {"Suspect": b.charCombo.currentText(), "Room": b.allRooms.currentText()}
        self.input = True
        '''


class CharacterSelect(QWidget):
    selected = ""
    charLocked = False

    def __init__(self):
        super().__init__()
        uic.loadUi("QTDesigner/CharacterSelect.ui", self)

        # Find all clickable labels and load in Character names
        self.availableChars = Game.CHARACTERS
        cnt = 0
        for items in self.charSelectWidget_2.children():
            if isinstance(items, ClickableLabel):
                items.LabelName = self.availableChars[cnt]
                items.getRef(self)
                cnt += 1

        # Connect push button to the Game Board
        self.pushButton.clicked.connect(self.lockInCharacter)

    def lockInCharacter(self):
        self.selectedWidget.setEnabled(False)
        self.charSelectWidget_2.setEnabled(False)
        self.charLocked = True
        self.WaitingAlert.setStyleSheet("font: 75 15pt MS Sans Serif;background-color: rgb(255, 255, 255)")

    def updateChars(self, chars):
        for items in self.charSelectWidget_2.children():
            if isinstance(items, ClickableLabel):
                if items.LabelName in chars:
                    print(items.LabelName)
                    items.setEnabled(True)
                else:
                    items.setEnabled(False)


class MainWindow(QMainWindow):
    start = False
    activeWindow = []
    characterWindow = []
    boardWindow = []
    displayBoard = False

    def __init__(self):
        super().__init__()
        uic.loadUi("QTDesigner/Clue-Less.ui", self)
        self.boardWindow = GameBoard()
        self.characterWindow = CharacterSelect()
        self.pushButton.clicked.connect(self.buttonPressed)
        # creating a timer object
        self.timer = QTimer()
        # adding action to timer
        self.timer.timeout.connect(self.showBoard)
        # update the timer every tenth second
        self.timer.start(100)

    def showBoard(self):
        if self.displayBoard:
            self.boardWindow.show()
            self.timer.stop()

    def buttonPressed(self):
        self.hide()
        self.start = True
        self.characterWindow.show()

    def packetHandler(self, socket: socket.socket):
        # Wait for player to start game
        while self.start is not True:
            pass
        # Select Character
        data = pickle.loads(socket.recv(1024))
        # Display available characters
        characters = data
        self.characterWindow.updateChars(characters)
        # Wait for user to select character
        while not self.characterWindow.charLocked:
            pass
        # Update packet with character choice
        # TODO: Verify that the chosen character wasn't taken in waiting. Server
        # sends OK response maybe?

        # Send back our choice
        socket.sendall(self.characterWindow.selected.encode())
        self.boardWindow.setAvatar(self.characterWindow.selected)
        unpickled = pickle.loads(socket.recv(4096))
        while unpickled:
            header = unpickled["type"]
            data = unpickled["data"]
            # The game has started
            if header in [STATE, INFO]:
                if header == INFO:
                    if data == "Starting Game!":
                        # Begin Receiving Moves
                        self.displayBoard = True
                        time.sleep(.5)
                        self.characterWindow.close()
                    else:
                        print(data)
                else:
                    # Re-paint the board with new state
                    self.boardWindow.Board.updateChars(data)
            if header == GAME_OVER:
                print(data)
                socket.close()
                return
            if header == OPTIONS:
                self.boardWindow.waiting = False
                self.boardWindow.PopulateOptions(data)
                # Wait for GUI response to chosen option
                response = self.boardWindow.getResponse()
                self.boardWindow.waiting = True
                pickled = pickle.dumps(response)
                socket.sendall(pickled)

            unpickled = pickle.loads(socket.recv(4096))

def main():
    # Create MainWindow
    app = QApplication(sys.argv)
    # Create Socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    mainwindow = MainWindow()
    # Start Client Thread
    x = threading.Thread(target=mainwindow.packetHandler, args=(s,))
    x.start()
    # Run the client GUI
    mainwindow.show()
    app.exec()


if __name__ == "__main__":
    main()
