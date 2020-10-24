
class Player:

    def __init__(self, character):
        self.character = character
        self.room = "Hallway"

    def __str__(self):
        return self.character

    def __repr__(self):
        return self.character

    def suggestion(self,special_envelope):
        characters = ["Mrs. White", "Mr. Green", "Mrs. Peacock", "Professor Plum", "Miss Scarlet", "Colonel Mustard"]
        for character in enumerate(characters):
            print(character)
        choice = ""
        while choice not in range(0,6):
            choice = input("Select a Character to Accuse")
            if not choice.isdigit():
                continue
            choice = int(choice)
        name = characters[choice]

        print(f"You accuse {name}")
        weapons = ["Candlestick", "Dagger", "Lead Pipe", "Revolver", "Rope", "Wrench"]
        for item in enumerate(weapons):
            print(item)
        choice = ""
        while choice not in range(0,6):
            choice = input("What weapons was used?")
            if not choice.isdigit():
                continue
            choice = int(choice)
        weapon = weapons[choice]
        print(f" {name} is accused of using the {weapon} in the {self.room}!")
        if ([name, weapon, self.room] == special_envelope):
            print(f" The evidence points that {name} is guilty of using the {weapon} in the {self.room}!")
            return False
        else:
            print("Sorry. That is not correct.")
            return True

    def travel(self):
        print("Where would you like to travel?")
        print(f"You are at {self.room} ")
        rooms = ["Kitchen", "Ballroom", "Conservatory", "Dining Room", "Cellar", "Billiard Room", "Library",
                      "Lounge", "Study"]
        for a in enumerate(rooms):
            print(a)
        choice = ""
        while choice not in range(0,9):
            choice = input("Please select a room")
            if not choice.isdigit():
                continue
            choice = int(choice)
        self.room = rooms[choice]
        print(f'{self.character} moved to {self.room}')