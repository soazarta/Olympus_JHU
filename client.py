import pickle
import select
import socket
import sys
import time

from configurations.helpers import Packet, Action


HOST = "localhost"
PORT = 54321


def handle_server_communications(s: socket.socket):
    """Handle all incoming and outgoing communication with server

    Args:
        s (socket.socket): The communication socket to listen on
    """
    # Initial communication with server
    response = s.recv(1024)
    packet = pickle.loads(response)

    while True:
        if packet.action == Action.Choose_Character:
            print(packet.state)

            # Display available characters
            characters = packet.data            
            print("Available characters: ")                
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
            s.send(pickle.dumps(packet))

            # Update packet with server response
            response = s.recv(1024)
            packet = pickle.loads(response)

        if packet.action == Action.Waiting:
            print(packet.state)

            print("Waiting for other players to join ...")
            time.sleep(3)
            s.send(pickle.dumps(packet))

            # Update packet with server response
            response = s.recv(1024)
            packet = pickle.loads(response)

        if packet.action == Action.Play_Game:
            print(packet.state)
            
            print("Playing game!")
            s.send(pickle.dumps(packet))
            break

    s.close()


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    # Handle server communications
    handle_server_communications(s)
