class Card:
    """Represents the playing card used in suggestions."""
    def __init__(self, value: str) -> None:
        self.value = value
    
    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return self.value
