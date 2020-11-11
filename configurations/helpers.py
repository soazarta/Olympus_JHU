import pickle
import socket

from enum import Enum


# Helper class to define actions between server and client
class Action(Enum):
    Choose_Character = 1
    Ready = 2
    Waiting = 3
    Game_Ready = 4
    Play = 5
    Wait = 6


# Helper class to define possible options during player turn
class Option(Enum):
    Move_Hallway = "Move to Hallway"
    Secret_Passage_Make_Suggestion = "Move to Secret Passage & Make Suggestion"
    Stay_Make_Suggestion = "Stay in Room & Make Suggestion"
    Move_Room_Make_Suggestion = "Move to Room & Make Suggestion"
    Make_Accusation = "Make Accusation"
    Lose_Turn = "Lose Turn"


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
    response = connection.recv(4096)

    return pickle.loads(response)
