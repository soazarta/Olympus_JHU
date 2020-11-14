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
from configurations.helpers import *
import socket
import threading
import time
import src.Game as Game
from src.GamePlay import *


HOST = "localhost"
PORT = 54321


class GameBoard(QWidget):
    waitingScreen = []
    movie = []
    waiting = False

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

    def Waiting(self):
        if self.waiting:
            self.movie.start()
            self.waitingScreen.show()
        elif not self.waiting:
            self.movie.stop()
            self.waitingScreen.hide()




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

    def packetHandler(self, socket):
        response = socket.recv(16384)
        packet = pickle.loads(response)
        while self.start is not True:
            pass
        while True:
            # The game has started
            if self.displayBoard:
                # Re-paint the board every turn
                self.boardWindow.Board.updateChars(packet.state)

            if packet.action == Action.Choose_Character:
                # Display available characters
                characters = packet.data
                self.characterWindow.updateChars(characters)
                # Wait for user to select character
                while not self.characterWindow.charLocked:
                    pass
                # Update packet with character choice
                characters.remove(self.characterWindow.selected)
                packet.action = Action.Ready
                packet.data = {"character": self.characterWindow.selected, "characters": characters}
                packet = process_packet(packet, socket)
                print("Waiting for other players to join ...")

            elif packet.action == Action.Waiting:
                # Wait for other players' turn
                packet = process_packet(packet, socket)

            elif packet.action == Action.Game_Ready:
                print("Ready to play game!")
                # Clean up character select
                self.displayBoard = True
                time.sleep(.2)
                self.characterWindow.close()
                packet = process_packet(packet, socket)

            elif packet.action == Action.Play:
                if self.boardWindow.waiting:
                    self.boardWindow.waiting = False
                #print(packet.state)
                player_move = parse_options(packet.data)

                packet.action = Action.Game_Ready
                packet.data = player_move
                packet = process_packet(packet, socket)

            elif packet.action == Action.Wait:
                print("Waiting for other players to finish their turns...")
                if self.displayBoard:
                    self.boardWindow.waiting = True
                packet.action = Action.Game_Ready
                packet = process_packet(packet, socket)
            else:
                print("Invalid Action")
                print(packet.action)


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
