from random import randint

from collections import deque
from configurations.helpers import Option
from .Player import Player


## CONSTANTS
# Rooms
STUDY = "Study"
HALL = "Hall"
LOUNGE = "Lounge"
LIBRARY = "Library"
BILLIARD = "Billiard Room"
DINNING = "Dinning Room"
CONSERVATORY = "Conservatory"
BALLROOM = "Ballroom"
KITCHEN = "Kitchen"

ROOMS = [STUDY, HALL, LOUNGE, LIBRARY, BILLIARD,
         DINNING, CONSERVATORY, BALLROOM, KITCHEN]

# Hallways
STUDY_HALL = "Study_Hall"
STUDY_LIBRARY = "Study_Library"
HALL_LOUNGE = "Hall_Lounge"
HALL_BILLIARD = "Hall_Billiard"
LOUNGE_DINNING = "Lounge_Dinning"
LIBRARY_BILLIARD = "Library_Billiard"
LIBRARY_CONSERVATORY = "Library_Conservatory"
BILLIARD_BALLROOM = "Billiard_Ballroom"
BILLIARD_DINNING = "Billiard_Dinning"
DINNING_KITCHEN = "Dinning_Kitchen"
CONSERVATORY_BALLROOM = "Conservatory_Ballroom"
BALLROOM_KITCHEN = "Ballroom_Kitchen"

# Characters
CHARACTERS = ["Mrs. White", "Mr. Green", "Mrs. Peacock",
              "Professor Plum", "Miss Scarlet", "Colonel Mustard"]

# Weapons
WEAPONS = ["Candlestick", "Dagger", "Lead Pipe", "Revolver", "Rope", "Wrench"]

# Characters in hallways
STARTING_POSITION = {"Mrs. White": BALLROOM_KITCHEN, "Mr. Green": CONSERVATORY_BALLROOM,
                     "Mrs. Peacock": LIBRARY_CONSERVATORY, "Professor Plum": STUDY_LIBRARY,
                     "Miss Scarlet": HALL_LOUNGE, "Colonel Mustard": LOUNGE_DINNING}


# Room class
class Room:

    def __init__(self, name: str, neighbours: list, secret_passage: str = None):
        """Initialize new instance of class Room

        Args:
            name (str): The room name
            neighbours (list): Adjacent rooms and hallways
            secret_passage (str): The secret passage
        """
        self.name = name
        self.neighbours = neighbours
        self.secret_passage = secret_passage
        self.players = list()


    def __str__(self):
        return f"{self.name} has {self.players}"


    def __repr__(self):
        return self.__str__()


# Hallway class
class Hallway:

    def __init__(self, name: str, neighbours: list):
        """Initialize new instance of class Hallway

        Args:
            name (str): The room name
            neighbours (list): Adjacent rooms and hallways
        """
        self.name = name
        self.neighbours = neighbours
        self.player = None


    def __str__(self):
        return f"{self.name} has {self.player}"


    def __repr__(self):
        return self.__str__()


# Game class
class Game:

    def __init__(self):
        """Initialize new instance of class Game
        """
        self.characters = CHARACTERS
        self.weapons = WEAPONS
        self.rooms = ROOMS
        self.case_file = self.__init_case_file()
        self.board = self.__init_board()

        self.players = list()
        self.turns = deque()


    def __init_case_file(self) -> dict:
        """Initialize the case file

        Returns:
            dict: The case file
        """
        a = randint(0, 5)
        b = randint(0, 8)

        return {"Suspect": self.characters[a], "Room": self.rooms[b], "Weapon": self.weapons[a]}


    def __init_board(self) -> dict:
        """Initialize game board

        Returns:
            dict: The game board
        """
        return {STUDY: Room(STUDY, [STUDY_HALL, STUDY_LIBRARY], KITCHEN),
                HALL: Room(HALL, [STUDY_HALL, HALL_LOUNGE, HALL_BILLIARD]),
                LOUNGE: Room(LOUNGE, [HALL_LOUNGE, LOUNGE_DINNING], CONSERVATORY),
                LIBRARY: Room(LIBRARY, [STUDY_LIBRARY, LIBRARY_CONSERVATORY, LIBRARY_CONSERVATORY]),
                BILLIARD: Room(BILLIARD, [HALL_BILLIARD, LIBRARY_BILLIARD, BILLIARD_DINNING, BILLIARD_BALLROOM]),
                DINNING: Room(DINNING, [LOUNGE_DINNING, BILLIARD_DINNING, DINNING_KITCHEN]),
                CONSERVATORY: Room(CONSERVATORY, [LIBRARY_CONSERVATORY, CONSERVATORY_BALLROOM], LOUNGE),
                BALLROOM: Room(BALLROOM, [BILLIARD_BALLROOM, CONSERVATORY_BALLROOM, BALLROOM_KITCHEN]),
                KITCHEN: Room(KITCHEN, [DINNING_KITCHEN, BALLROOM_KITCHEN], STUDY),
                STUDY_HALL: Hallway(STUDY_HALL, [STUDY, HALL]),
                STUDY_LIBRARY: Hallway(STUDY, LIBRARY),
                HALL_LOUNGE: Hallway(HALL_LOUNGE, [HALL, LOUNGE]),
                HALL_BILLIARD: Hallway(HALL_BILLIARD, [HALL, BILLIARD]),
                LOUNGE_DINNING: Hallway(LOUNGE_DINNING, [LOUNGE, DINNING]),
                LIBRARY_BILLIARD: Hallway(LIBRARY_BILLIARD, [LIBRARY, BILLIARD]),
                LIBRARY_CONSERVATORY: Hallway(LIBRARY_CONSERVATORY, [LIBRARY, CONSERVATORY]),
                BILLIARD_BALLROOM: Hallway(BILLIARD_BALLROOM, [BILLIARD, BALLROOM]),
                BILLIARD_DINNING: Hallway(BILLIARD_DINNING, [BILLIARD, DINNING]),
                DINNING_KITCHEN: Hallway(DINNING_KITCHEN, [DINNING, KITCHEN]),
                CONSERVATORY_BALLROOM: Hallway(CONSERVATORY_BALLROOM, [CONSERVATORY, BALLROOM]),
                BALLROOM_KITCHEN: Hallway(BALLROOM_KITCHEN, [BALLROOM, KITCHEN])
                }


    def game_state(self) -> str:
        """Current game state

        Returns:
            str: description of current game state
        """
        state = "Game State\n"
        state += f"Players: {self.players}\n"
        state += f"Turn: {self.turns[0] if len(self.turns) > 0 else None}\n"
        #state += f"Board: {self.board}\n"

        return state


    def game_ready(self) -> bool:
        """Check if all players are ready to play.

        Returns:
            bool: If all players are ready
        """
        # TODO: Implement a logic to determine if players are ready
        return len(self.players) == 2


    def add_player(self, player: Player) -> bool:
        """Add new player to game

        Args:
            player (Player): The player to be added

        Returns:
            bool: Successfull addition or not
        """
        for plr in self.players:
            if player.character == plr.character:
                return False

        # Add player
        self.players.append(player)
        self.turns.append(player)

        # Update board with position
        player_position = STARTING_POSITION[player.character]
        self.board[player_position].player = player
        player.space = player_position

        return True


    def possible_options(self, player: Player) -> dict:
        """Determine possible options for player's turn

        Args:
            player (Player): The player

        Returns:
            dict: Map of options to values
        """
        options = dict()
        space = player.space

        # Suggestion are all other players
        temp = [x.character for x in self.players]
        suggestions = set(temp).difference(set(player.character))

        # Player in a room options
        if space in ROOMS:
            room = self.board[space]

            # Check if room has secret passage
            secret_passage = room.secret_passage
            if secret_passage != None:
                options[Option.Secret_Passage_Make_Suggestion] = {"Passage": secret_passage, "Suggestions": suggestions}

            # Check if hallways are blocked
            possible_hallways = list()

            for neighbour in room.neighbours:
                hallway = self.board[neighbour]
                if hallway.player == None:
                    possible_hallways.append(hallway.name)

            if len(possible_hallways) > 0:
                options[Option.Move_Hallway] = possible_hallways

            # Check if player was moved
            if player.was_moved:
                options[Option.Stay_Make_Suggestion] = suggestions

        # Player in a hallway options
        else:
            possible_rooms = self.board[space].neighbours
            options[Option.Move_Room_Make_Suggestion] = {"Rooms": possible_rooms, "Suggestions": suggestions}

        # Check if no options were available
        if len(options) == 0:
            options[Option.Lose_Turn] = None

        # Always add making an accusation as an option
        options[Option.Make_Accusation] = None

        return options


    def update_position(self, player) -> bool:
        """Update player position in board

        Args:
            player (Player): The player

        Returns:
            bool: Successful update or not
        """
        # TODO: logic to be implemented
        return None
