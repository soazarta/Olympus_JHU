import json
import os
import pickle 
import socket

from enum import Enum
from pathlib import Path
from types import SimpleNamespace


# Helper class to define actions between server and client
class Action(Enum):
    Choose_Character = 1
    Ready = 2
    Waiting = 3
    Game_Ready = 4
    Play = 5
    Wait = 6


# Packet class for communication between server and client
class Packet:
    def __init__(self, action: Action, state: str, data: object):
        self.action = action
        self.state = state
        self.data = data


def process_packet(packet: Packet, connection: socket.socket) -> Packet:
    """Process a socket connection packet

    Args:
        packet (Packet): The packet to be processed
        connection (socket.socket): The socket connection

    Returns:
        packet (Packet): The processed packet
    """
    connection.send(pickle.dumps(packet))    
    response = connection.recv(1024)

    return pickle.loads(response)


def load_game_data() -> object:
    """Load game data from database file

    Returns: 
        object: Game's data object
    """
    path = Path(__file__).parent

    # TODO: handle FileNotFoundError exception
    with open(os.path.join(path, "GameData.json")) as data_file:
        game_data = vars(json.load(data_file, object_hook=lambda d: SimpleNamespace(**d)))

    # Verify GameData object has all necessary data
    if "Characters" not in game_data:
        raise KeyError("GameData missing key: Characters.")

    if "Weapons" not in game_data:
        raise KeyError("GameData missing key: Weapons.")

    if "Rooms" not in game_data:
        raise KeyError("GameData missing key: Rooms.")

    return game_data