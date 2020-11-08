from configurations.helpers import Option
from .Game import ROOMS


def __make_suggestion(characters: list) -> dict:
    """Handle making a suggestion

    Args:
        characters (list): Available characters 

    Returns:
        dict: {"Suspect": character, "Room": room}
    """
    suggestion = dict()

    print("Make a suggestion!")
    
    # Choose character
    print("Available Characters")                
    for character in enumerate(characters, 1):
        print(character)

    chosen_character = -1

    while chosen_character not in range(0, len(characters)):
        chosen_character = input(f"\nChoose a number: ")
        chosen_character = int(chosen_character) - 1

    suggestion["Suspect"] = characters[chosen_character]

    # Choose room
    print("Available rooms to move to")
    for room in enumerate(ROOMS, 1):
        print(room)

    chosen_room = -1

    while chosen_room not in range(0, len(ROOMS)):
        chosen_room = input("\nChoose a room: ")
        chosen_room = int(chosen_room) - 1

    suggestion["Room"] = ROOMS[chosen_room]
    
    return suggestion


def __move_hallway():
    # TODO: to be implemented
    pass


def __secret_passage_make_suggestion():
    # TODO: to be implemented
    pass


def __stay_make_suggestion():
    # TODO: to be implemented
    pass


def __move_room_make_suggestion(data: dict) -> dict:
    """Handle moving to a room and making a suggestion

    Args:
        data (dict): {"Rooms": list, "Suggestions": list}

    Returns: 
        dict: {"Room": chosen room, "Suggestion": {"Suspect": character, "Room": room}}
    """
    res = dict()

    # Handle choosing a room
    rooms = data["Rooms"]
    print("Available rooms to move to")
    for room in enumerate(rooms, 1):
        print(room)

    chosen_room = -1

    while chosen_room not in range(0, len(rooms)):
        chosen_room = input("\nChoose a room: ")
        chosen_room = int(chosen_room) - 1

    res["Room"] = rooms[chosen_room]

    # Handle making a suggestion
    suggestion = __make_suggestion(data["Suggestions"])
    res["Suggestion"] = suggestion

    return res


def __make_accusation():
    # TODO: to be implemented
    pass


def __lose_turn():
    # TODO: to be implemented
    pass


# Map options to handlers delegates
__process_options = {Option.Move_Hallway: __move_hallway,
                     Option.Secret_Passage_Make_Suggestion: __secret_passage_make_suggestion,
                     Option.Stay_Make_Suggestion: __stay_make_suggestion,
                     Option.Move_Room_Make_Suggestion: __move_room_make_suggestion,
                     Option.Make_Accusation: __make_accusation,
                     Option.Lose_Turn: __lose_turn }


def parse_options(options: dict) -> dict:
    """Parse available options and capture player's decisions

    Args:
        options (dict): The available options

    Returns:
        dict: {"ChosenOption": option, "Play": object}
    """
    res = dict()

    # Display available options
    print("Available Options")
    options_keys = list(options.keys())
    for option in enumerate(options_keys, 1):
        print(f"{option[0]}\t{option[1].name}")

    chosen_option = -1

    # Prompt player to choose an option
    while chosen_option not in range(0, len(options)):
        chosen_option = input(f"\nChoose an option: ")
        chosen_option = int(chosen_option) - 1

    option = options_keys[chosen_option]

    # Process chosen option
    res["ChosenOption"] = option
    res["Play"] = __process_options[option](options[option])

    return res