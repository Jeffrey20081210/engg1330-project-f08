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
    ("In the concourse you choose one of three routes: Tech, Human or Sneak.",
     "default"),
    ("", "default"),
    ("TIME", "title"),
    ("The game is turn-based: the clock only moves when you act.", "default"),
    ("Each step costs 4 seconds. A wrong answer or a restart costs 3 "
     "minutes. Each hint (H inside a task) costs 2 minutes. Moves inside a "
     "task are free.", "default"),
    ("Opening help, the map or your items costs no time.", "default"),
    ("", "default"),
    ("KEYS", "title"),
    ("WASD / arrows  move        E  interact / press", "default"),
    ("M  station map   I  items and clues   ?  this help   Q  quit",
     "default"),
    ("", "default"),
    ("A careful explorer may find 3 fragments and learn what the 03:00 "
     "train really is...", "dim"),
]

FRAGMENT_NAMES = {
    "ticket_0300": "Old paper ticket: CENTRAL -> ??? 03:00 one way",
    "newspaper": "Newspaper clipping about 'Platform 0'",
    "signal_note": "Note: TRACK 0 - 03:00 - DO NOT REPORT",
    "staff_photo": "Photo of Mr Leung, night controller, 1989",
    "conductor_cap": "Old conductor's cap: 'for everyone who missed it'",
}

CLUE_NAMES = {
    "receipt_a": "Receipt piece (ticket machine)",
    "receipt_b": "Receipt piece (rubbish bin)",
    "receipt_c": "Receipt piece (bench)",
}

ITEM_NAMES = {
    "keycard": "staff keycard",
    "office_key": "ticket office key",
    "maintenance_key": "maintenance key",
    "signal_log": "signal log",
    "staff_logbook": "staff logbook",
    "tunnel_map": "tunnel map",
}

ENDINGS = {
    "escape": {
        "title": "ESCAPED",
        "style": "good",
        "lines": [
            "The shutter grinds up and you step out into the warm night air "
            "of Des Voeux Road. A red taxi slows down for you.",
            "Behind you the station lights go out. You never find out what "
            "the 03:00 train was... or did you miss something?",
        ],
    },
    "true_board": {
        "title": "03:00",
        "style": "fragment",
        "lines": [
            "TRUE ENDING - You step on board. The doors close softly and the "
            "old train glides into a tunnel that is on no map.",
            "You wake up in your own bed at 07:00, rested. On the table lies "
            "an old paper ticket, now stamped USED. Mr Leung always gets his "
            "passengers home.",
        ],
    },
    "true_leave": {
        "title": "03:00",
        "style": "info",
        "lines": [
            "TRUE ENDING - You shake your head. The conductor smiles, tips "
            "his cap, and the empty train slides away into the dark.",
            "You walk out into the street knowing Central's oldest secret: "
            "the 03:00 train waits for everyone who missed the last one.",
        ],
    },
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
    "alarm": {
        "title": "ALARM",
        "style": "bad",
        "lines": [
            "Sirens! Red lights flash all along the tunnel. Two guards march "
            "you up to the street and write down your name.",
            "You are out of the station - but you will be explaining this to "
            "MTR for a long time.",
        ],
    },
}
