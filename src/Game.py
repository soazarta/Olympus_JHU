from random import randint

from collections import deque
from .Player import Player


class Game:

    def __init__(self, game_data: object):
        """Initialize new instance of class Game

        Args:
            game_data (object): The game data
        """
        # Initialize game data
        self.characters = game_data["Characters"]
        self.weapons = game_data["Weapons"]
        self.rooms = game_data["Rooms"]

        # Configure special envelope
        a = randint(0, 5)
        b = randint(0, 8)
        self.special_envelope = [self.characters[a], self.weapons[a], self.rooms[b]]        

        self.players = list()
        self.turns = deque()


    def game_state(self) -> str:
        """Current game state

        Returns:
            str: description of current game state
        """
        state = "Game State\n"
        state += f"Players: {self.players}\n"
        state += f"Turn: {self.turns[0] if len(self.turns) > 0 else None}\n"

        return state


    def game_ready(self) -> bool:
        """Check if all players are ready to play.

        Returns:
            bool: If all players are ready
        """
        # TODO: Implement a logic to determine if players are ready
        return len(self.players) == 2


    def next_turn(self):
        """Handle next turn in gameplay
        """
        for player in self.players:
            game_continues = True
            print("1. Make A Suggestion")
            print("2. Travel")
            choice = -1
            print(f'Player {self.players.index(player) + 1} is located at {player.room}')
            while choice not in ['1','2']:
                choice = input(f" Player {self.players.index(player) + 1} - {player}: Please Select an Action")
            choice = int(choice)
            if choice == 1:
                game_continues = player.suggestion(self.special_envelope)
                if not game_continues:
                    print(f"{player} solved the mystery!")
                    print(f"{player} wins!")
                    return game_continues
            if choice == 2:
                player.travel()
                print(f"correct anwser is {self.special_envelope}")
                print("---NEXT TURN---")
        return game_continues
