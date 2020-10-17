# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from Game import Game


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    new_game = Game()
    new_game.load_players()
    game_continues = True
    while game_continues:
        game_continues = new_game.next_turn()
    print("GAME OVER")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
