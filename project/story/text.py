"""Story text: intro, help screen, endings and item names."""

INTRO_LINES = [
    "00:38. The last train leaves Central without you.",
    "You had fallen asleep on a bench after a very long day.",
    "00:42. You wake up. The station is empty and the lights are dim.",
    "A voice on the speakers: \"This station will close and seal at 01:30.\"",
    "Then, much quieter: \"...the 03:00 service departs from Platform 1.\"",
    "There is no 03:00 service. Find a way out before 01:30.",
]

START_MESSAGES = [
    ("You wake up on the bench at Central. The gate to the exit is locked.",
     "default"),
    ("Explore the platform. Walk up to things and press E. Press ? for help.",
     "info"),
]

HELP_LINES = [
    ("GOAL", "title"),
    ("Escape from Central station before it seals at 01:30.", "default"),
    ("Complete the tasks (marked with a blinking !) to open the way out.",
     "default"),
    ("", "default"),
    ("TIME", "title"),
    ("The game is turn-based: the clock only moves when you act.", "default"),
    ("Each step costs 4 seconds. A wrong answer costs 3 minutes and resets "
     "the task. Each hint (H inside a task) costs 2 minutes.", "default"),
    ("Opening help, the map or your items costs no time.", "default"),
    ("", "default"),
    ("KEYS", "title"),
    ("WASD / arrows  move        E  interact / press", "default"),
    ("M  station map   I  items and clues   ?  this help   Q  quit",
     "default"),
    ("", "default"),
    ("A careful explorer may find out what the 03:00 train really is...",
     "dim"),
]

FRAGMENT_NAMES = {
    "ticket_0300": "Old paper ticket: CENTRAL -> ??? 03:00 one way",
}

CLUE_NAMES = {
    "receipt_a": "Receipt piece (ticket machine)",
    "receipt_b": "Receipt piece (rubbish bin)",
    "receipt_c": "Receipt piece (bench)",
}

ENDINGS = {
    "trapped": {
        "title": "TRAPPED",
        "style": "bad",
        "lines": [
            "01:30. The lights go out with a heavy clunk and every shutter "
            "slams shut.",
            "You sit down on the cold floor and wait for the first train at "
            "dawn. Somewhere far away, at exactly 03:00, you hear a train "
            "that should not exist.",
        ],
    },
}
