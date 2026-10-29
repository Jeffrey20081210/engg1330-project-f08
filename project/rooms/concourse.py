"""The concourse above the platform: the hub where the three routes split.

Task: P2, the shift lockers. The key from the locker opens one of the three
route doors in the back wall. The exit hall (right) opens when the route's
work is done.
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

DOOR_ART = ["│     │", "│     │"]
DOOR_MASK = ["fkkkkkf", "fkkkkkf"]
DOOR_PALETTE = {"f": "door_frame", "k": "dark"}
DOOR_LOCKED = "Locked. A sign says: staff keys are kept in the shift lockers."

OBJECTS = [
    {"pos": (8, 0), "art": [" CONTROL ROOM "], "mask": ["s" * 14],
     "palette": {"s": "sign"}},
    {"pos": (11, 1), "art": DOOR_ART, "mask": DOOR_MASK,
     "palette": DOOR_PALETTE},
    {"pos": (32, 0), "art": [" TICKET OFFICE "], "mask": ["s" * 15],
     "palette": {"s": "sign"}},
    {"pos": (36, 1), "art": DOOR_ART, "mask": DOOR_MASK,
     "palette": DOOR_PALETTE},
    {"pos": (58, 0), "art": [" STAFF  ONLY "], "mask": ["s" * 13],
     "palette": {"s": "sign"}},
    {"pos": (61, 1), "art": DOOR_ART, "mask": DOOR_MASK,
     "palette": DOOR_PALETTE},
    {"pos": (48, 0), "art": ["═════════"], "style": "light_on",
     "flicker": True},
    # Row of fare gates in the middle of the concourse
    {"pos": (24, 11), "solid": True, "style": "machine",
     "art": ["[=]  [=]  [=]  [=]  [=]  [=]  [=]  [=]  [=]"]},
    # Shift lockers (P2), against the bottom wall
    {"pos": (5, 12), "solid": True,
     "art": ["┌───┬───┬───┬───┐", "│ 1 │ 2 │ 3 │ 4 │",
             "│ = │ = │ = │ = │", "└───┴───┴───┴───┘"],
     "mask": ["l" * 17] * 4, "palette": {"l": "locker"}},
    # Notes taped next to the lockers
    {"pos": (23, 13), "art": ["▒▒", "▒▒"], "style": "receipt"},
    # Fragment 2: a newspaper clipping in the far corner
    {"pos": (76, 15), "art": ["*"], "style": "fragment", "blink": "rare",
     "hide_fragment": "newspaper"},
]

SPOTS = [
    {"id": "lockers", "zone": (3, 9, 26, 11), "kind": "puzzle",
     "puzzle": "lockers", "prompt": "Use the shift lockers",
     "marker": (13, 11),
     "done_text": "The lockers are locked for the rest of the shift."},
    {"id": "corner", "zone": (70, 13, 77, 15), "kind": "fragment",
     "fragment": "newspaper", "hide_fragment": "newspaper",
     "prompt": "Pick up the scrap of paper", "title": "Newspaper clipping",
     "text": [
         "A brittle newspaper clipping, the date torn off:",
         "",
         "\"...MTR denies rumours of a secret 'Platform 0' under Central. "
         "Night staff still report a train at 03:00 that appears on no "
         "timetable...\"",
     ]},
]

EXITS = {
    "1": {"to": "platform", "entry": (74, 8), "facing": "left",
          "look": "opening"},
    "2": {"to": "control_room", "requires": "route_tech", "look": "door",
          "entry": (39, 14), "facing": "up", "locked": DOOR_LOCKED},
    "3": {"to": "ticket_office", "requires": "route_human", "look": "door",
          "entry": (39, 14), "facing": "up", "locked": DOOR_LOCKED},
    "4": {"to": "storeroom", "requires": "route_sneak", "look": "door",
          "entry": (39, 14), "facing": "up", "locked": DOOR_LOCKED},
    "5": {"to": "exit_hall", "requires": "exit_hall_open", "look": "shutter",
          "entry": (5, 8), "facing": "right",
          "locked": "The shutter to the exit hall is down."},
}

ROOM = {
    "id": "concourse",
    "name": "Concourse",
    "map": MAP,
    "start": (5, 8),
    "first_visit": "You climb the stairs to the concourse. Three locked doors "
                   "lead deeper into the station. Shift lockers stand on the "
                   "left.",
    "objects": OBJECTS,
    "spots": SPOTS,
    "exits": EXITS,
}
