import logging
import pickle
import select
import socket
import time
from typing import Dict, List

from src.constants import CHARACTERS
from src.messages import *
from src.Game import Game
from src.validator import get_options, validate

logging.basicConfig(level=logging.DEBUG)

HOST = "localhost"
PORT = 54321

MAX_PLAYERS = 2


def handle_game(players: Dict[str, socket.socket]) -> None:
    """Start and handle a game instance
    Args:
        players (Dict[str, socket.socket]): Mapping of character names to
            connections
    """
    game = Game(players)

    logging.debug(f"Case: {game.case}")

    while not game.over:
        options = get_options(game, game.current)
        logging.debug(f"Options for {game.current.name}: {list(options.keys())}")
        request = {"type": OPTIONS, "data": options}
        pickled = pickle.dumps(request)
        time.sleep(.5)
        game.current.connection.sendall(pickled)

        played = False
        while True:
            readable, _, _ = select.select(game.players, [], [])

            for player in readable:
                if player == game.current:
                    data = pickle.loads(player.connection.recv(4096))
                    validate(game, player, data)
                    logging.debug("Validated move")
                    game.play(player, data)
                    played = True
                else:
                    # TODO: Handle if another client sends out of order
                    pass
            if played:
                break


def handle_clients(s: socket.socket) -> None:
    """Handle clients communication with game server.
    Args:
        s (socket.socket): The communication socket to listen on
    """

    players = dict.fromkeys(CHARACTERS)  # type: Dict[str, socket.socket]
    connections = []  # type: List[socket.socket]

    while True:
        # If 2 players have selected their character, start game
        if len([conn for _, conn in players.items() if conn]) == MAX_PLAYERS:
            # TODO: Add a thread for each game, take players out of connections
            handle_game(players)
            s.close()
            return

        # Listen on the socket for new connections and the list of players
        rlist = [s] + connections
        readable, _, _ = select.select(rlist, [], [])

        for fd in readable:
            if fd in connections:
                data = fd.recv(1024).decode()
                logging.debug(f"Received: {data}")
                if data:
                    # Character selection
                    if data in CHARACTERS and players[data] == None:
                        logging.debug(f"{data} has joined!")
                        players[data] = fd
                else:
                    connections.remove(fd)
                    fd.close()

            elif fd is s:
                connection, address = s.accept()
                connections.append(connection)
                logging.debug(f"Connection from {address[0]}:{address[1]}")

                # Send the new connection the character list
                data = pickle.dumps([character for character, connection in players.items() if not connection])
                connection.sendall(data)


if __name__ == "__main__":
    # Server socket setup
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(4)

    logging.debug(f"Listening on {HOST}:{PORT}")

    # Handle client connections
    handle_clients(s)