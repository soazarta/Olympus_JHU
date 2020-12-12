from typing import List

from .player import Player

class Tile:
    """Generic class to represent a game tile."""
    def __init__(self, name: str) -> None:
        self.name = name
        self.neighbors = [] # type: List["Tile"]
        self.players = [] # type: List["Player"]
    
    @property
    def full(self) -> bool:
        """If there are available spaces. Implemented by subclasses."""
        raise NotImplementedError
