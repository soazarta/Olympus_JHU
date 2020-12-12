class Option:
    """Generic option to be overriden."""
    def __init__(self) -> None:
        pass

class Move(Option):
    """Move a tile."""
    def __init__(self, destination: str) -> None:
        super().__init__()
        self.destination = destination

class Suggestion(Option):
    """Make a suggestion."""
    def __init__(self, character: str, weapon: str, room: str) -> None:
        super().__init__()
        self.character = character
        self.weapon = weapon
        self.room = room

class Accusation(Option):
    """Make an accusation."""
    def __init__(self, character: str, weapon: str, room: str) -> None:
        super().__init__()
        self.character = character
        self.weapon = weapon
        self.room = room

class ShowCard(Option):
    """Show one of your cards to the player making the suggestion."""
    def __init__(self, card: str) -> None:
        super().__init__()
        self.card = card

class End(Option):
    """Choose to end your turn."""
    def __init__(self) -> None:
        super().__init__()
