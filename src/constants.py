# Rooms
STUDY = "Study"
HALL = "Hall"
LOUNGE = "Lounge"
LIBRARY = "Library"
BILLIARD = "Billiard Room"
DINING = "Dining Room"
CONSERVATORY = "Conservatory"
BALLROOM = "Ballroom"
KITCHEN = "Kitchen"

ROOMS = [
    STUDY, HALL, LOUNGE, LIBRARY, BILLIARD, DINING, CONSERVATORY, BALLROOM, KITCHEN
]

# Hallways
STUDY_HALL = "Study-Hall"
STUDY_LIBRARY = "Study-Library"
HALL_LOUNGE = "Hall-Lounge"
HALL_BILLIARD = "Hall-Billiard"
LOUNGE_DINING = "Lounge-Dining"
LIBRARY_BILLIARD = "Library-Billiard"
LIBRARY_CONSERVATORY = "Library-Conservatory"
BILLIARD_BALLROOM = "Billiard-Ballroom"
BILLIARD_DINING = "Billiard-Dining"
DINING_KITCHEN = "Dining-Kitchen"
CONSERVATORY_BALLROOM = "Conservatory-Ballroom"
BALLROOM_KITCHEN = "Ballroom-Kitchen"

HALLWAYS = [
    STUDY_HALL, STUDY_LIBRARY, HALL_LOUNGE, HALL_BILLIARD, LOUNGE_DINING,
    LIBRARY_BILLIARD, LIBRARY_CONSERVATORY, BILLIARD_BALLROOM, BILLIARD_DINING,
    DINING_KITCHEN, CONSERVATORY_BALLROOM, BALLROOM_KITCHEN
]

# Characters
MRS_WHITE = "Mrs. White"
MR_GREEN = "Mr. Green"
MRS_PEACOCK = "Mrs. Peacock"
PROFESSOR_PLUM = "Professor Plum"
MISS_SCARLET = "Miss Scarlet"
COLONEL_MUSTARD = "Colonel Mustard"

CHARACTERS = [
    MRS_WHITE, MR_GREEN, MRS_PEACOCK, PROFESSOR_PLUM, MISS_SCARLET,
    COLONEL_MUSTARD
]

# Weapons
CANDLESTICK = "Candlestick"
DAGGER = "Dagger"
LEAD_PIPE = "Lead Pipe"
REVOLVER = "Revolver"
ROPE = "Rope"
WRENCH = "Wrench"

WEAPONS = [CANDLESTICK, DAGGER, LEAD_PIPE, REVOLVER, ROPE, WRENCH]

# Starting positions for characters
START = {
    MRS_WHITE: BALLROOM_KITCHEN,
    MR_GREEN: CONSERVATORY_BALLROOM,
    MRS_PEACOCK: LIBRARY_CONSERVATORY,
    PROFESSOR_PLUM: STUDY_LIBRARY,
    MISS_SCARLET: HALL_LOUNGE,
    COLONEL_MUSTARD: LOUNGE_DINING
}

# Sprites for each character
SPRITES = {
    MRS_WHITE : "\u001b[37;1m■\u001b[0m",
    MR_GREEN : "\u001b[32m■\u001b[0m",
    MRS_PEACOCK : "\u001b[36m■\u001b[0m",
    PROFESSOR_PLUM : "\u001b[35m■\u001b[0m",
    MISS_SCARLET : "\u001b[31m■\u001b[0m",
    COLONEL_MUSTARD : "\u001b[33m■\u001b[0m"
}

# Colored names for each character
COLOR_NAME = {
    MRS_WHITE : f"\u001b[37;1m{MRS_WHITE}\u001b[0m",
    MR_GREEN : f"\u001b[32m{MR_GREEN}\u001b[0m",
    MRS_PEACOCK : f"\u001b[36m{MRS_PEACOCK}\u001b[0m",
    PROFESSOR_PLUM : f"\u001b[35m{PROFESSOR_PLUM}\u001b[0m",
    MISS_SCARLET : f"\u001b[31m{MISS_SCARLET}\u001b[0m",
    COLONEL_MUSTARD : f"\u001b[33m{COLONEL_MUSTARD}\u001b[0m"
}
