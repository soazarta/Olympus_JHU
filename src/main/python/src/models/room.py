from .tile import Tile


class Room(Tile):
    """Represents a room tile."""

    def __init__(self, name: str) -> None:
        super().__init__(name)
    
    @property
    def full(self) -> bool:
        # Rooms can have as many people as needed
        return False
