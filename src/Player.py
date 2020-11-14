import socket


class Player:

    def __init__(self, character: str, connection: socket.socket):
        """Initialize new instance of class Player
        Args:
            character (str): The player's character
            connection (socket.socket): The connection with game server
        """
        self.character = character
        self.connection = connection
        self.space = None # room or hallway

        # Track whether player was moved by another player
        self.was_moved = False


    def __str__(self):
        return f"{self.character}:{self.space}"


    def __repr__(self):
        return self.__str__()