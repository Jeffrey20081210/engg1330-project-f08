"""Act 3: the exit hall. P9 shutter release, the street exit and, for
players with all three fragments, the hidden door to Platform 0."""

# Exits: "1" back to the concourse, "2" the street (needs the release),
# "3" the hidden door in the back wall (needs the release + 3 fragments).
DOOR_ROW = "#" * 8 + "3" * 5 + "#" * 67

MAP = (
    ["#" * 80] * 3
    + [DOOR_ROW]
    + ["||" + "." * 76 + "||"] * 2
    + ["11" + "." * 76 + "22"] * 5
    + ["||" + "." * 76 + "||"] * 5
    + ["#" * 80] * 2
)

OBJECTS = [
    {"pos": (30, 0), "art": ["═════════"], "style": "light_on"},
    {"pos": (56, 0), "art": ["═════════"], "style": "light_on", "flicker": True},
    {"pos": (60, 1), "art": ["  EXIT  ->  STREET  "], "mask": ["s" * 20],
     "palette": {"s": "sign"}},
    # Emergency release console (P9)
    {"pos": (30, 1),
     "art": ["╔══════════════╗", "║ (o)(o)(o)(o) ║", "╚══════════════╝"],
     "mask": ["m" * 16, "m" + "s" * 14 + "m", "m" * 16],
     "palette": {"m": "machine", "s": "lamp_r"},
     "flag_palette": {"flag": "shutter_released",
                      "palette": {"m": "machine", "s": "lamp_g"}}},
    # A faint crack of blue light in the old wall (3 fragments only)
    {"pos": (10, 1), "art": ["│", "│"], "style": "secret_door",
     "blink": "rare", "needs_fragments": 3},
    {"pos": (8, 1), "art": ["┌───┐", "│   │"], "style": "secret_door",
     "needs_fragments": 3, "needs_flags": ["shutter_released"]},
    # Floor hatch where the tunnel comes up
    {"pos": (9, 15), "art": ["[=====]"], "style": "hatch"},
    # Row of fare gates
    {"pos": (40, 12), "solid": True, "style": "machine",
     "art": ["[=]  [=]  [=]  [=]  [=]"]},
]

SPOTS = [
    {"id": "release_console", "zone": (28, 4, 47, 5), "kind": "puzzle",
     "puzzle": "signals", "prompt": "Use the emergency release",
     "marker": (37, 0), "done_text": "The street shutter is already open."},
]

EXITS = {
    "1": {"to": "concourse", "entry": (74, 8), "facing": "left",
          "look": "opening"},
    "2": {"ending": "escape", "requires": "shutter_released",
          "look": "shutter",
          "locked": "The street shutter is down. The emergency release "
                    "console is on the back wall."},
    "3": {"scene": "platform0", "requires": "shutter_released",
          "requires_fragments": 3, "look": "hidden",
          "locked": None},          # looks like wall: no message
}

ROOM = {
    "id": "exit_hall",
    "name": "Exit hall",
    "map": MAP,
    "start": (5, 8),
    "first_visit": "The exit hall. Beyond the shutter on the right is the "
                   "street. The release console is on the back wall.",
    "objects": OBJECTS,
    "spots": SPOTS,
    "exits": EXITS,
}
