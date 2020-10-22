import logging
import select
import socket

from Player import Player
from Game import Game


logging.basicConfig(level=logging.DEBUG)

HOST = "localhost"
PORT = 54321


def game_ready(game: Game) -> bool:
    """Checks if all players have readied up.

    Args:
        game (Game): The current game

    Returns:
        bool: If all players have readied up
    """
    if len(game.players) < 2:
        return False
    for player in game.players:
        if not player.ready:
            return False
    return True


def broadcast(game: Game, message: str):
    """Broadcast a message to all players.

    Args:
        game (Game): The game to broadcast to
        message (str): The message to send
    """
    logging.debug(f"BROADCAST: {message}")

    for player in game.players:
        player.connection.send(message.encode())


def handle_data(s: socket.socket):
    """Handle all incoming and outgoing messages on the socket.

    Args:
        s (socket.socket): The socket to listen on
    """
    # TODO: Support multiple games at once
    game = Game()

    while True:
        rlist = [s] + game.players
        readable, _, _ = select.select(rlist, [], [])
        for r in readable:
            if r is s:
                connection, address = s.accept()
                # Temporarily just naming the player after their port
                player = Player(str(address[1]), connection)
                game.players.append(player)
                rlist.append(player)
                broadcast(game, f"{player.character} has joined")
            else:
                data = r.connection.recv(1024).decode().strip()
                logging.debug(f"Received {data} from {r.character}")
                if data:
                    if data == "ready":
                        r.ready = True
                    if data == "unready":
                        r.ready = False
                else:
                    rlist.remove(r)
                    game.players.remove(r)
                    r.connection.close()
                    broadcast(game, f"{r.character} has left the game...")

        if game_ready(game):
            broadcast(game, "start game")
            break

    s.close()


if __name__ == "__main__":
    # Server socket setup
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(4)

    logging.debug(f"Listening on {HOST}:{PORT}")

    # Listen on our new socket
    handle_data(s)
