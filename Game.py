from random import randint

from Player import Player


class Game:

    def __init__(self):
        a = randint(0, 5)
        b = randint(0, 8)
        self.characters = ["Mrs. White", "Mr. Green", "Mrs. Peacock", "Professor Plum", "Miss Scarlet", "Colonel Mustard"]
        self.players = []
        self.weapons = ["Candlestick", "Dagger", "Lead Pipe", "Revolver", "Rope", "Wrench"]
        self.rooms = ["Kitchen", "Ballroom", "Conservatory", "Dining Room", "Cellar", "Billiard Room", "Library",
                      "Lounge", "Study"]
        self.special_envelope = [self.characters[a], self.weapons[a], self.rooms[b]]


    def load_players(self):
        print("Welcome to the game clue - mock up version")
        num_of_players = 0
        while num_of_players not in ['3','4','5','6']:
            num_of_players = input("how many players are their today? Choose 3 to 6 players")
        num_of_players = int(num_of_players)
        print(f"you chose {num_of_players} players")
        for player_num in range(1, num_of_players + 1):
            choose_character = -1
            print("----------------con--------")
            print(f"Choose a number between one and {len(self.characters)}")
            print("available characters:")
            for names in enumerate(self.characters, 1):
                print(names)
            while choose_character not in range(0, len(self.characters)):
                choose_character = input(f"Player #{player_num}, choose a number:")
                if not choose_character.isdigit():
                    continue
                choose_character = int(choose_character) - 1
            print("------------------------")
            print(f"player {player_num} has chosen {self.characters[choose_character]}")
            name = self.characters.pop(choose_character)
            new_player = Player(name)
            self.players.append(new_player)
        for player in range(len(self.players)):
            print(f" Player {player+1} {self.players[player]}")

    def next_turn(self):
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





