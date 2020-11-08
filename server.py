import logging
import socket

from _thread import start_new_thread, allocate_lock
from configurations.helpers import Action, Packet
from configurations.helpers import process_packet
from src.Player import Player
from src.Game import Game


logging.basicConfig(level=logging.DEBUG)

HOST = "localhost"
PORT = 54321


def play_game(game: Game, lock) -> Packet:
    """Handle players' turns during gameplay

    Args:
        game (Game): The game instance
        lock: The threading lock object

    Returns:
        The packet
    """
    # Packet for current player's turn
    turn = Packet(Action.Play, game.game_state(), None)
    
    # Packet for all other players
    wait = Packet(Action.Wait, game.game_state(), None)

    # Update next player's turn
    lock.acquire()
    
    current_turn = game.turns.popleft()
    turn.data = game.possible_options(current_turn)    
    logging.debug(f"{current_turn} is playing ...")    

    res = process_packet(turn, current_turn.connection)
    logging.debug(f"{current_turn} played {res.data}")

    for player in game.turns:
        process_packet(wait, player.connection)

    logging.debug(f"{current_turn} is done playing")
    game.turns.append(current_turn)

    lock.release()

    return res 


def handle_client(connection: socket.socket, game: Game, packet: Packet, lock):
    """Handle client communications

    Args:
        connection (socket.socket): The client connection
        game (Game): The game isntance
        packet (Packet): The socket communication packet
        lock: The threading lock object
    """
    player = None
    
    while True:
        if packet.action == Action.Choose_Character:
            # Send a copy of available characters
            packet.data = game.characters
            packet = process_packet(packet, connection)

        if packet.action == Action.Ready:
            # Update available characters
            character = packet.data["character"]
            logging.debug(f"Player {character} has joined")

            # TODO: Use thread lock to synchronize available characters update
            game.characters = packet.data["characters"]

            # Create and add player to game
            player = Player(character, connection)
            if not game.add_player(player):
                logging.error(f"Unable to add player {character}")

            # Check whether enough players have joined
            packet.action = Action.Game_Ready if game.game_ready() else Action.Waiting
            packet.state = game.game_state()
            packet.data = None

            packet = process_packet(packet, connection)

        if packet.action == Action.Waiting:
            # Continue to wait until game is ready
            if game.game_ready():
                packet.action = Action.Game_Ready
                packet.state = game.game_state()
            
            packet = process_packet(packet, connection)

        if packet.action == Action.Game_Ready:
            packet = play_game(game, lock)
        
    connection.close()


def handle_clients(s: socket.socket):
    """Handle clients communication with game server

    Args:
        s (socket.socket): The communication socket to listen on
    """
    # TODO: Support multiple games at once
    game = Game()

    # Threading lock
    lock = allocate_lock()

    while True:
        connection, address = s.accept()
        client_id = address[1]
        logging.debug(f"Connected to client: {str(client_id)}")

        # Pass initial packet to new client
        packet = Packet(Action.Choose_Character, game.game_state(), None)

        # Handle each client's communication on a new thread
        start_new_thread(handle_client, (connection, game, packet, lock, ))

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