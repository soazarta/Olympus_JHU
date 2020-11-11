import os
import pickle
import socket

from configurations.helpers import Action, Packet
from configurations.helpers import process_packet
from src.GamePlay import *


HOST = "localhost"
PORT = 54321


def handle_server_communications(s: socket.socket):
    """Handle all incoming and outgoing communications with server

    Args:
        s (socket.socket): The communication socket to listen on
    """
    # Initial communication with server
    response = s.recv(4096)
    packet = pickle.loads(response)

    while True:
        if packet.action == Action.Choose_Character:
            # Display available characters
            characters = packet.data
            print("Available Characters")
            for character in enumerate(characters, 1):
                print(character)

            chosen_character = -1

            # Prompt player to choose character
            while chosen_character not in range(0, len(characters)):
                chosen_character = input(f"\nChoose a number: ")
                chosen_character = int(chosen_character) - 1

            # Update packet with character choice
            name = characters.pop(chosen_character)
            packet.action = Action.Ready
            packet.data = {"character": name, "characters": characters}

            packet = process_packet(packet, s)
            print("Waiting for other players to join ...")

        if packet.action == Action.Waiting:
            # Wait for other players to join
            packet = process_packet(packet, s)

        if packet.action == Action.Game_Ready:
            print("Ready to play game!")
            packet = process_packet(packet, s)

        if packet.action == Action.Play:
            print(packet.state)
            player_move = parse_options(packet.data)

            packet.action = Action.Game_Ready
            packet.data = player_move
            packet = process_packet(packet, s)

        if packet.action == Action.Wait:
            # Wait for other players' turn
            packet.action = Action.Game_Ready
            packet = process_packet(packet, s)


    s.close()


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    # Enable colors in the terminal for Windows, no need for Linux/macOS
    if os.name == "nt":
        os.system("color")

    # Handle server communications
    handle_server_communications(s)
