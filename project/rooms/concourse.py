"""The concourse above the platform: the hub where the three routes split.

In this first build the three route doors and the exit hall are still
locked; they will be opened by the Act 2 puzzles.
"""

DOOR_ROW = "#" * 12 + "2" * 5 + "#" * 20 + "3" * 5 + "#" * 20 + "4" * 5 + "#" * 13

MAP = (
    ["#" * 80] * 3
    + [DOOR_ROW]
    + ["||" + "." * 76 + "||"] * 2
    + ["11" + "." * 76 + "55"] * 5
    + ["||" + "." * 76 + "||"] * 5
    + ["#" * 80] * 2
)

DOOR_ART = ["┌─────┐", "│     │", "│     │"]
DOOR_MASK = ["fffffff", "fkkkkkf", "fkkkkkf"]
DOOR_PALETTE = {"f": "door_frame", "k": "dark"}

LOCKED_TEXT = "The door is locked. (This area comes in the next build.)"

OBJECTS = [
    {"pos": (8, 0), "art": [" CONTROL ROOM "], "mask": ["s" * 14],
     "palette": {"s": "sign"}},
    {"pos": (11, 1), "art": DOOR_ART[1:], "mask": DOOR_MASK[1:],
     "palette": DOOR_PALETTE},
    {"pos": (32, 0), "art": [" TICKET OFFICE "], "mask": ["s" * 15],
     "palette": {"s": "sign"}},
    {"pos": (36, 1), "art": DOOR_ART[1:], "mask": DOOR_MASK[1:],
     "palette": DOOR_PALETTE},
    {"pos": (58, 0), "art": [" STAFF  ONLY "], "mask": ["s" * 13],
     "palette": {"s": "sign"}},
    {"pos": (61, 1), "art": DOOR_ART[1:], "mask": DOOR_MASK[1:],
     "palette": DOOR_PALETTE},
    {"pos": (48, 0), "art": ["═════════"], "style": "light_on",
     "flicker": True},
    # Row of fare gates in the middle of the concourse
    {"pos": (24, 11), "solid": True, "style": "machine",
     "art": ["[=]  [=]  [=]  [=]  [=]  [=]  [=]  [=]  [=]"]},
]

SPOTS = []

EXITS = {
    "1": {"to": "platform", "entry": (74, 8), "facing": "left",
          "look": "opening"},
    "2": {"to": None, "requires": "never", "look": "door",
          "locked": LOCKED_TEXT},
    "3": {"to": None, "requires": "never", "look": "door",
          "locked": LOCKED_TEXT},
    "4": {"to": None, "requires": "never", "look": "door",
          "locked": LOCKED_TEXT},
    "5": {"to": None, "requires": "never", "look": "shutter",
          "locked": "The exit shutter to the street is down."},
}

ROOM = {
    "id": "concourse",
    "name": "Concourse",
    "map": MAP,
    "start": (5, 8),
    "first_visit": "You climb the stairs to the concourse. Three doors lead "
                   "deeper into the station.",
    "objects": OBJECTS,
    "spots": SPOTS,
    "exits": EXITS,
}
