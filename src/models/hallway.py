from .tile import Tile


class Hallway(Tile):
    """Represents a hallway tile."""

    def __init__(self, name: str) -> None:
        super().__init__(name)
        
    @property
    def full(self) -> bool:
        # A hallways can only have 1 player at a time
        return len(self.players) != 0
