import logging
import pickle
import select
import socket
import time

from _thread import *
from configurations.helpers import load_game_data, Packet, Action
from src.Player import Player
from src.Game import Game


logging.basicConfig(level=logging.DEBUG)

HOST = "localhost"
PORT = 54321


def game_ready(game: Game) -> bool:
    """Checks if all players are ready to play.

    Args:
        game (Game): The current game

    Returns:
        bool: If all players are ready
    """
    # TODO: configure this value dynamically on server startup
    return len(game.players) == 2


def handle_client(connection: socket.socket, game: Game, packet: Packet):
    """Handle client communication

    Args:
        connection (socket.socket): The client connection
        game (Game): The current game isntance
        packet (Packet): The socket communication packet
    """
    response = None
    player = None

    while True:
        if packet.action == Action.Choose_Character:
            # Send a copy of available characters
            packet.data = game.characters
            connection.send(pickle.dumps(packet))
            
            response = connection.recv(1024)
            packet = pickle.loads(response)

        if packet.action == Action.Ready:
            # Update available characters
            game.characters = packet.data["characters"]
            logging.debug(f"Available characters left: {game.characters}")

            # Create and add player to game
            character = packet.data["character"]
            player = Player(character)
            game.players.append(player)

            # Check whether enough players have joined
            packet.action = Action.Play_Game if game_ready(game) else Action.Waiting
            packet.state = game.game_state()
            packet.data = None
            connection.send(pickle.dumps(packet))
            
            response = connection.recv(1024)
            packet = pickle.loads(response)

        if packet.action == Action.Waiting:
            # Check whether enough players have joined
            if game_ready(game):                    
                packet.action = Action.Play_Game
                packet.state = game.game_state()
                
                connection.send(pickle.dumps(packet))
            else:
                time.sleep(3)
                connection.send(pickle.dumps(packet))

            logging.debug(packet.state)
            response = connection.recv(1024)
            packet = pickle.loads(response)

        if packet.action == Action.Play_Game:
            logging.debug(game.game_state())
            logging.debug(f"Playing Game!")
            # TODO: gameplay logic to be integrated here
            break

    connection.close()


def handle_clients(s: socket.socket):
    """Handle clients communication with game server

    Args:
        s (socket.socket): The communication socket to listen on
    """
    clients = set()

    # Game instance setup
    # TODO: Support multiple games at once
    game_data = load_game_data()
    game = Game(game_data)

    while True:
        connection, address = s.accept()
        client_id = address[1]
        logging.debug(f"Connected to client: {str(client_id)}")

        # Pass initial packet to new client
        packet = Packet(Action.Choose_Character, game.game_state(), None)

        # Start a new thread per each client
        start_new_thread(handle_client, (connection, game, packet, ))
        clients.add(client_id)
        logging.debug(f"{game.game_state()}")

    s.close()


if __name__ == "__main__":
    # Server socket setup
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(4)

    logging.debug(f"Listening on {HOST}:{PORT}")

    # Handle clients connections
    handle_clients(s)