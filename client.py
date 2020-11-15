import os
import pickle
import socket
from typing import Dict, List

from src.messages import *
from src.options import *


HOST = "localhost"
PORT = 54321


def menu(title: str, choices: List[str]) -> str:
    """Displays a menu and gets the user's choice."""
    print(title)
    for i, choice in enumerate(choices):
        print(f"{i+1} {choice}")

    selection = -1
    while selection not in range(len(choices)):
        try:
            selection = int(input("Number: ")) - 1
        except ValueError:
            selection = -1
    # New line to separate things
    print()

    return choices[selection]


def handle(s: socket.socket):
    unpickled = pickle.loads(s.recv(4096))
    while unpickled:
        header = unpickled["type"]
        data = unpickled["data"]

        if header in [STATE, INFO]:
            print(data)

        if header == GAME_OVER:
            print(data)
            s.close()
            return

        if header == OPTIONS:
            if len(data) == 1:
                option = list(data.keys())[0]
            else:
                option = menu("Options", list(data.keys()))
            response = None

            if option == MOVE:
                destination = menu("Destination?", data[option])
                response = Move(destination)
            
            if option == SUGGESTION:
                character = menu("Character?", data[option]["characters"])
                weapon = menu("Weapon?", data[option]["weapons"])
                # Can only accuse in the room you're in, sending data anyways
                room = data[option]["rooms"]
                response = Suggestion(character, weapon, room)
            
            if option == ACCUSATION:
                character = menu("Character?", data[option]["characters"])
                weapon = menu("Weapon?", data[option]["weapons"])
                room = menu("Room?", data[option]["rooms"])
                response = Accusation(character, weapon, room)
            
            if option == SHOW_CARD:
                if not data[option]["cards"]:
                    print("No matching cards to show")
                    response = ShowCard(None)
                else:
                    card = menu(f"Card to show to {data[option]['player']}", data[option]["cards"])
                    response = ShowCard(card)
            
            if option == END:
                response = End()
            
            pickled = pickle.dumps(response)
            s.sendall(pickled)

        unpickled = pickle.loads(s.recv(4096))


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    # The server sends the list of available characters
    data = pickle.loads(s.recv(1024))
    character = menu("Who will you choose?", data)

    # TODO: Verify that the chosen character wasn't taken in waiting. Server
    # sends OK response maybe?

    # Send back our choice
    s.sendall(character.encode())

    # Enable colors in the terminal for Windows, no need for Linux/macOS
    if os.name == "nt":
        os.system("color")

    # Handle server communications
    handle(s)
