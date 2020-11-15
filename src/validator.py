from typing import Dict, List

from .constants import HALLWAYS, ROOMS, CHARACTERS, WEAPONS
from .game import Game
from .models import Player
from .options import Option, Move, ShowCard, Suggestion, Accusation, End
from .messages import *


def get_options(game: Game, player: Player) -> Dict[str, List[str]]:
    """Get the possible options a player can make.

    Args:
        game (Game): The current game state
        player (Player): The player

    Returns:
        List[str]: The dictionary of valid options and their valid parameters
    """
    options = {} # type: Dict[str, List[str]]
    suggestion_data = {"characters": CHARACTERS, "weapons": WEAPONS, "rooms": player.location}
    accusation_data = {"characters": CHARACTERS, "weapons": WEAPONS, "rooms": ROOMS}

    # Pseudo-turn for show the suggestor cards
    if game.suggestion_turn:
        matching = [card.value for card in player.cards if card.value in [game.suggestion.character, game.suggestion.weapon, game.suggestion.room]]
        if matching:
            options[SHOW_CARD] = {"player": game.suggestor.name, "cards": matching}
        else:
            options[SHOW_CARD] = {"cards": None}
        return options

    # Can make an accusation at any point in the turn
    options[ACCUSATION] = accusation_data

    # If a player has moved this turn, they must make an accusation or suggestion
    # if they are in a room.
    # If a player has moved and made a suggestion, they can make an accusation
    # or end their turn
    if player.has_moved:
        if player.has_suggested:
            options[END] = None
            return options
        elif player.location in ROOMS:
            options[SUGGESTION] = suggestion_data
            return options
        else:
            options[END] = None
            return options

    # Can only move into rooms, non-full hallways, and secret passages
    possible = [_.name for _ in game.board[player.location].neighbors if not _.full]
    if possible:
        options[MOVE] = possible

    # A player moved to a room may make a suggestion first
    if player.was_moved:
        options[SUGGESTION] = suggestion_data

    return options


def validate(game: Game, player: Player, option: Option) -> None:
    """Check that a given option is valid for the game state.

    Args:
        game (Game): The game instance
        player (Player): The player making the move
        option (Option): The move made

    Raises:
        ValueError: On invalid moves
    """
    if isinstance(option, Move):
        _validate_move(game, player, option)
    if isinstance(option, Suggestion):
        _validate_suggestion(game, player, option)
    if isinstance(option, Accusation):
        _validate_accusation(game, player, option)
    if isinstance(option, ShowCard):
        _validate_show_card(game, player, option)
    if isinstance(option, End):
        _validate_end(game, player, option)
    if not isinstance(option, Option):
        raise ValueError("Invalid option")


def _validate_move(game: Game, player: Player, move: Move):
    if not len([tile for tile in game.board[player.location].neighbors if tile.name == move.destination]):
        raise ValueError(f"You must move into an adjacent hallway or room")
    if move.destination in HALLWAYS and game.board[move.destination].full:
        raise ValueError(f"You cannot move into an occupied hallway")


def _validate_suggestion(game: Game, player: Player, suggestion: Suggestion):
    if suggestion.character not in CHARACTERS:
        raise ValueError(f"Invalid character: {suggestion.character}")
    if suggestion.weapon not in WEAPONS:
        raise ValueError(f"Invalid weapon: {suggestion.weapon}")
    if suggestion.room not in ROOMS:
        raise ValueError(f"Invalid room: {suggestion.room}")
    if suggestion.room != player.location:
        raise ValueError(f"Suggestion room must be the room you are in")


def _validate_accusation(game: Game, player: Player, accusation: Accusation):
    if accusation.character not in CHARACTERS:
        raise ValueError(f"Invalid character: {accusation.character}")
    if accusation.weapon not in WEAPONS:
        raise ValueError(f"Invalid weapon: {accusation.weapon}")
    if accusation.room not in ROOMS:
        raise ValueError(f"Invalid room: {accusation.room}")


def _validate_show_card(game: Game, player: Player, show_card: ShowCard):
    if not any(card.value == show_card.card for card in player.cards):
        if show_card.card:
            raise ValueError("No possible matching cards")
    else:
        if not show_card.card:
            raise ValueError("Must show a matching card")
    if show_card.card and show_card.card not in [game.suggestion.character, game.suggestion.weapon, game.suggestion.room]:
        raise ValueError("Not a valid card to show.")


def _validate_end(game: Game, player: Player, end: End):
    if not player.has_moved and not game.suggestion_turn:
        raise ValueError("You must move in your turn")
    if player.has_moved and player.location in ROOMS and not player.has_suggested:
        raise ValueError("You must make a suggestion if you are in a room.")
    