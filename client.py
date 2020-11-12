import pickle
import socket
import MainWindow
import GUIStatus

from configurations.helpers import Action, Packet
from configurations.helpers import process_packet


HOST = "localhost"
PORT = 54321


def handle_server_communications(s: socket.socket, gui: MainWindow.MainWindow):
    """Handle all incoming and outgoing communications with server

    Args:
        s (socket.socket): The communication socket to listen on
        gui (MainWindow.mainwindow): The client GUI that acts on packets
    """
    # Initial communication with server
    response = s.recv(1024)
    packet = pickle.loads(response)
    # Wait for user to start the game
    while gui.start is not True:
        pass
    while True:
        gui.packetHandler(packet)
        '''
        if packet.action == Action.Choose_Character:
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
            # TODO: Game logic to be integrated here
            input("It's your turn, input something... ")

            packet.action = Action.Game_Ready
            packet = process_packet(packet, s)

        if packet.action == Action.Wait:
            # Wait for other players' turn
            packet.action = Action.Game_Ready
            packet = process_packet(packet, s)
        '''
    s.close()


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    # Handle server communications
    handle_server_communications(s)

