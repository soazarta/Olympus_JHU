from itertools import cycle
import pickle
from random import randrange
import socket
from time import sleep
from typing import Dict, List, Set

from .constants import *
from .helpers import bold
from .messages import *
from .models import Player, Card, Hallway, Room, Tile
from .options import *


class Game:
    """Represents the internal game state."""

    def __init__(self, connections: Dict[str, socket.socket]) -> None:
        self._create_board()
        # Create player objects for everyone
        self.players = [] # type: List[Player]
        for character, connection in connections.items():
            if connection:
                # Get the player's starting tile
                location = START[character]
                player = Player(character, location, connection)
                self.players.append(player)
                self.board[location].players.append(player)
        self._setup_cards()
        # If the game is over or not
        self.over = False
        # Pseudo-turn when players must show cards
        self.suggestor = None # type: Player
        self.suggestion_turn = False
        self.suggestion = None # type: Suggestion

    def _create_board(self) -> None:
        """Mapping of names to board tiles also creating the adjacency list."""
        self.board = {
            STUDY: Room(STUDY),
            HALL: Room(HALL),
            LOUNGE: Room(LOUNGE),
            LIBRARY: Room(LIBRARY),
            BILLIARD: Room(BILLIARD),
            DINING: Room(DINING),
            CONSERVATORY: Room(CONSERVATORY),
            BALLROOM: Room(BALLROOM),
            KITCHEN: Room(KITCHEN),
            STUDY_HALL: Hallway(STUDY_HALL),
            STUDY_LIBRARY: Hallway(STUDY_LIBRARY),
            HALL_LOUNGE: Hallway(HALL_LOUNGE),
            HALL_BILLIARD: Hallway(HALL_BILLIARD),
            LOUNGE_DINING: Hallway(LOUNGE_DINING),
            LIBRARY_BILLIARD: Hallway(LIBRARY_BILLIARD),
            LIBRARY_CONSERVATORY: Hallway(LIBRARY_CONSERVATORY),
            BILLIARD_BALLROOM: Hallway(BILLIARD_BALLROOM),
            BILLIARD_DINING: Hallway(BILLIARD_DINING),
            DINING_KITCHEN: Hallway(DINING_KITCHEN),
            CONSERVATORY_BALLROOM: Hallway(CONSERVATORY_BALLROOM),
            BALLROOM_KITCHEN: Hallway(BALLROOM_KITCHEN),
        } # type: Dict[str, Tile]

        # Set up the adjacency list for with neighbors
        self.board[STUDY].neighbors = [self.board[_] for _ in [STUDY_HALL, STUDY_LIBRARY, KITCHEN]]
        self.board[HALL].neighbors = [self.board[_] for _ in [STUDY_HALL, HALL_LOUNGE, HALL_BILLIARD]]
        self.board[LOUNGE].neighbors = [self.board[_] for _ in [HALL_LOUNGE, LOUNGE_DINING, CONSERVATORY]]
        self.board[LIBRARY].neighbors = [self.board[_] for _ in [STUDY_LIBRARY, LIBRARY_CONSERVATORY, LIBRARY_CONSERVATORY]]
        self.board[BILLIARD].neighbors = [self.board[_] for _ in [HALL_BILLIARD, LIBRARY_BILLIARD, BILLIARD_DINING, BILLIARD_BALLROOM]]
        self.board[DINING].neighbors = [self.board[_] for _ in [LOUNGE_DINING, BILLIARD_DINING, DINING_KITCHEN]]
        self.board[CONSERVATORY].neighbors = [self.board[_] for _ in [LIBRARY_CONSERVATORY, CONSERVATORY_BALLROOM, LOUNGE]]
        self.board[BALLROOM].neighbors = [self.board[_] for _ in [BILLIARD_BALLROOM, CONSERVATORY_BALLROOM, BALLROOM_KITCHEN]]
        self.board[KITCHEN].neighbors = [self.board[_] for _ in [DINING_KITCHEN, BALLROOM_KITCHEN, STUDY]]
        self.board[STUDY_HALL].neighbors = [self.board[_] for _ in [STUDY, HALL]]
        self.board[STUDY_LIBRARY].neighbors = [self.board[_] for _ in [STUDY, LIBRARY]]
        self.board[HALL_LOUNGE].neighbors = [self.board[_] for _ in [HALL, LOUNGE]]
        self.board[HALL_BILLIARD].neighbors = [self.board[_] for _ in [HALL, BILLIARD]]
        self.board[LOUNGE_DINING].neighbors = [self.board[_] for _ in [LOUNGE, DINING]]
        self.board[LIBRARY_BILLIARD].neighbors = [self.board[_] for _ in [LIBRARY, BILLIARD]]
        self.board[LIBRARY_CONSERVATORY].neighbors = [self.board[_] for _ in [LIBRARY, CONSERVATORY]]
        self.board[BILLIARD_BALLROOM].neighbors = [self.board[_] for _ in [BILLIARD, BALLROOM]]
        self.board[BILLIARD_DINING].neighbors = [self.board[_] for _ in [BILLIARD, DINING]]
        self.board[DINING_KITCHEN].neighbors = [self.board[_] for _ in [DINING, KITCHEN]]
        self.board[CONSERVATORY_BALLROOM].neighbors = [self.board[_] for _ in [CONSERVATORY, BALLROOM]]
        self.board[BALLROOM_KITCHEN].neighbors = [self.board[_] for _ in [BALLROOM, KITCHEN]]

    def _setup_cards(self) -> None:
        # Add a rotating list of players for convenience
        self.rotation = cycle(self.players)

        character_cards = [Card(character) for character in CHARACTERS]
        weapon_cards = [Card(weapon) for weapon in WEAPONS]
        room_cards = [Card(room) for room in ROOMS]

        # Create a case with one of each card
        self.case = set() # type: Set[Card]
        self.case.add(character_cards.pop(randrange(len(character_cards))))
        self.case.add(weapon_cards.pop(randrange(len(weapon_cards))))
        self.case.add(room_cards.pop(randrange(len(room_cards))))

        cards = character_cards + weapon_cards + room_cards

        # Distribute all cards to players equally
        while cards:
            self._next().cards.append(cards.pop(randrange(len(cards))))
        
        self.broadcast(INFO, "Starting Game!")
        self.broadcast(STATE, str(self))

        for player in self.players:
            message = {"type": INFO, "data": f"Your cards are: {player.cards}"}
            data = pickle.dumps(message)
            player.connection.sendall(data)

    def _next(self) -> Player:
        self._front = next(self.rotation)
        return self._front

    def __str__(self) -> str:
        state = ""
        for p in self.players:
            state += p.__str__()
            state += "\n"
        return state
    
    @property
    def current(self) -> Player:
        return self._front

    def broadcast(self, header: str, body: str) -> None:
        """Broadcast a message to all players in a game.

        Args:
            header (str): The message header
            body (str): The message body
        """
        message = {"type": header, "data": body}
        data = pickle.dumps(message)

        for player in self.players:
            player.connection.sendall(data)
        
        # If we send too many messages to a client at once, it will consume
        # multiple messages in 1 recv call and be left waiting for a message
        # that will never come. Besides this hot fix, the options are either
        # to rework message handling or create a minimal protocol. This might
        # just be good enough for now though... 
        sleep(0.1)
    
    def unicast(self, header: str, body: str, player: Player) -> None:
        """Send a message to a single player.

        Args:
            header (str): The message header
            body (str): The message body
            player (Player): The player to send to
        """
        message = {"type": header, "data": body}
        data = pickle.dumps(message)

        player.connection.sendall(data)
        
        # Delay here, same reason as broadcast
        sleep(0.1)

    def play(self, player: Player, option: Option) -> None:
        if isinstance(option, Move):
            self.board[player.location].players.remove(player)
            self.board[option.destination].players.append(player)
            player.location = option.destination
            player.has_moved = True
            # In case the player was moved but chose not to suggest
            player.was_moved = False
            self.broadcast(STATE, str(self))
            self.broadcast(INFO, f"{player.name} moved to {option.destination}")

        if isinstance(option, Suggestion):
            self.current.has_suggested = True
            self.suggestor = self.current
            self.suggestion_turn = True
            self.suggestion = option
            # In case they are making a suggestion after having been moved
            self.current.was_moved = False
            # Move players into the room if they are suspected
            moved = [_ for _ in self.players if _.name == option.character and _.name != self.current.name]
            if moved:
                self.board[moved[0].location].players.remove(moved[0])
                self.board[option.room].players.append(moved[0])
                moved[0].location = option.room
                moved[0].was_moved = True
            self._next()
            self.broadcast(STATE, str(self))
            self.broadcast(INFO, f"{self.suggestor.name} is suggesting {bold(option.character)} with the {bold(option.weapon)} in the {bold(option.room)}")

        if isinstance(option, ShowCard):
            if option.card:
                self.broadcast(INFO, f"{self.current.name} showed {option.card}")
            else:
                self.broadcast(INFO, f"{self.current.name} had no cards to show")

            self._next()
            if self.current == self.suggestor:
                self.suggestion_turn = False
                self.suggestor = None

        if isinstance(option, Accusation):
            self.broadcast(INFO, f"{self.current.name} is accusing {bold(option.character)} with the {bold(option.weapon)} in the {bold(option.room)}")
            
            correct = len([card for card in self.case if card.value in [option.character, option.weapon, option.room]])
            if correct == 3:
                self.broadcast(GAME_OVER, f"{player.name} won the game!")
                self.over = True
            else:
                self.broadcast(INFO, f"{self.current.name} was wrong and is out of the game...")
                # Close out and remove the player
                message = {"type": GAME_OVER, "data": f"Game over..."}
                data = pickle.dumps(message)
                player.connection.sendall(data)

                self.board[player.location].players.remove(player)
                self.players.remove(player)
                # Recreate the cycle at the correct position
                temp = self._next()
                self.rotation = cycle(self.players)
                while self.current != temp:
                    self._next()

        if isinstance(option, End):
            player.has_moved = False
            player.has_suggested = False
            self.broadcast(INFO, f"{self.current.name} ended their turn")
            self._next()
