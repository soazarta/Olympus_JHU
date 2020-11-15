import socket
from typing import List

from .card import Card


class Player:
    """Represents a client in game."""

    def __init__(self, name: str, location: str, connection: socket.socket) -> None:
        self.name = name
        self.location = location
        self.connection = connection
        self.cards = [] # type: List[Card]
        # If the player has move on their turn
        self.has_moved = False
        # If the player has made a suggestion
        self.has_suggested = False
        # If the player was moved via a suggestion
        self.was_moved = False
        # # If the player must make a suggestion
        # self.is_suggesting = False

    # Used for select
    def fileno(self):
        return self.connection.fileno()

    def __str__(self) -> str:
        return f"{self.name}:{self.location}"
