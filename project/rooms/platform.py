"""Act 1: Central station, Platform 1. The player wakes up here.

Task: open the platform gate with the staff override code (puzzle
"gate_code"). The code is hidden in three torn pieces of a receipt.
"""

# Map rows: 0-3 back wall, 4-11 floor, 12 tactile strip, 13 screen doors,
# 14-17 track. Exit "1" on the right is the gate to the concourse.
MAP = (
    ["#" * 80] * 4
    + ["||" + "." * 76 + "||"] * 2
    + ["||" + "." * 76 + "11"] * 5
    + ["||" + "." * 76 + "||"]
    + ["||" + "_" * 76 + "||"]
    + ["||" + "=" * 76 + "||"]
    + ["~" * 80]
    + ["-" * 80] * 2
    + ["~" * 80]
)

POSTER_MASK = ["ffffffffffff", "frrrrrrrrrrf", "fbbbbbbbbbbf", "ffffffffffff"]

OBJECTS = [
    # Ceiling lights; the middle one is failing and flickers.
    {"pos": (19, 0), "art": ["═════════"], "style": "light_on"},
    {"pos": (34, 0), "art": ["═══════════"], "style": "light_on",
     "flicker": True},
    # Safety poster
    {"pos": (4, 0),
     "art": ["┌──────────┐", "│ MIND THE │", "│   GAP    │", "└──────────┘"],
     "mask": ["ffffffffffff", "frrrrrrrrrrf", "frrrrrrrrrrf", "ffffffffffff"],
     "palette": {"f": "poster_frame", "r": "poster_red"}},
    # Station name sign
    {"pos": (30, 1),
     "art": ["   C E N T R A L   ", "  Island Line   P1 "],
     "mask": ["s" * 19, "s" * 19], "palette": {"s": "sign"}},
    # Route map poster
    {"pos": (50, 0),
     "art": ["┌──────────┐", "│ROUTE  MAP│", "│o-o-o-o-o-│", "└──────────┘"],
     "mask": POSTER_MASK,
     "palette": {"f": "poster_frame", "r": "poster_red", "b": "poster_blue"}},
    # Staff notice
    {"pos": (63, 0),
     "art": ["┌─────┐", "│STAFF│", "│NOTE │", "└─────┘"],
     "mask": ["fffffff", "fpppppf", "fpppppf", "fffffff"],
     "palette": {"f": "poster_frame", "p": "poster_text"}},
    # Gate keypad: the light turns green when the gate opens.
    {"pos": (71, 1),
     "art": ["┌────┐", "│123*│", "└────┘"],
     "mask": ["kkkkkk", "kkkkLk", "kkkkkk"],
     "palette": {"k": "keypad", "L": "keypad_light"},
     "flag_palette": {"flag": "gate_open",
                      "palette": {"k": "keypad", "L": "shutter_open"}}},
    # Ticket machine (stands against the wall, blocks the floor below it)
    {"pos": (20, 2), "solid": True,
     "art": ["╔═════╗", "║ERR 7║", "║ [=] ║", "╚═════╝"],
     "mask": ["mmmmmmm", "msssssm", "mmtttmm", "mmmmmmm"],
     "palette": {"m": "machine", "s": "machine_screen", "t": "machine_slot"}},
    # Pillars
    {"pos": (10, 6), "solid": True,
     "art": ["┌──┐", "│  │", "│  │", "│  │", "└──┘"],
     "mask": ["pppp"] * 5, "palette": {"p": "pillar"}},
    {"pos": (52, 6), "solid": True,
     "art": ["┌──┐", "│  │", "│  │", "│  │", "└──┘"],
     "mask": ["pppp"] * 5, "palette": {"p": "pillar"}},
    # The bench where the player wakes up
    {"pos": (34, 8), "solid": "box", "style": "bench",
     "art": ["╔════════════╗", "╜            ╙"]},
    # Rubbish bin
    {"pos": (60, 10), "solid": True, "style": "bin", "art": [".--.", "|##|"]},
    # Hidden fragment: a faint glint in the dark corner
    {"pos": (4, 11), "art": ["*"], "style": "fragment", "blink": "rare",
     "hide_fragment": "ticket_0300"},
]

# Zones are (left, top, right, bottom) in map cells, tested against the
# middle of the player's feet.
SPOTS = [
    {"id": "safety_poster", "zone": (4, 4, 16, 5), "kind": "read",
     "prompt": "Read the safety poster", "title": "Safety poster",
     "text": [
         "MIND THE GAP.",
         "Passengers must leave the station after the last train.",
         "",
         "Under it, someone has scratched: \"lost something? check the "
         "bins and the benches before you call staff\".",
     ]},
    {"id": "ticket_machine", "zone": (17, 4, 29, 7), "kind": "read",
     "prompt": "Check the ticket machine", "title": "Ticket machine",
     "clue": "receipt_a",
     "text": [
         "The screen says ERR 7. You press the service button and the "
         "printer spits out a torn strip of paper:",
     ]},
    {"id": "station_sign", "zone": (30, 4, 48, 5), "kind": "read",
     "prompt": "Read the station sign", "title": "Station sign",
     "text": [
         "CENTRAL - Island Line, Platform 1.",
         "Last train to Chai Wan: 00:38.",
         "",
         "Below it, a small line that you have never seen before: "
         "\"Special service 03:00. Destination not shown.\"",
     ]},
    {"id": "route_map", "zone": (49, 4, 62, 5), "kind": "read",
     "prompt": "Look at the route map", "title": "Route map",
     "text": [
         "The Island Line runs from Kennedy Town to Chai Wan.",
         "",
         "Someone has drawn one extra station after Chai Wan with a black "
         "marker. It has no name, only a time: 03:00.",
     ]},
    {"id": "staff_notice", "zone": (63, 4, 69, 5), "kind": "read",
     "prompt": "Read the staff notice", "title": "Staff notice",
     "text": [
         "STAFF ONLY - PLATFORM GATE OVERRIDE",
         "",
         "Enter the 3-digit staff code on the keypad. The code uses three "
         "different digits.",
         "Every failed attempt is printed on the ticket machine's "
         "maintenance log, with how many digits were right.",
     ]},
    {"id": "gate_keypad", "zone": (70, 4, 77, 8), "kind": "puzzle",
     "puzzle": "gate_code", "prompt": "Use the gate keypad",
     "marker": (73, 0)},
    {"id": "bench", "zone": (32, 7, 49, 11), "kind": "read",
     "prompt": "Search the bench", "title": "Bench", "clue": "receipt_c",
     "text": [
         "This is where you fell asleep. Something crinkles under the "
         "seat: another torn piece of the receipt.",
     ]},
    {"id": "bin", "zone": (57, 8, 66, 12), "kind": "read",
     "prompt": "Search the bin", "title": "Rubbish bin", "clue": "receipt_b",
     "text": [
         "Under an empty lemon tea carton you find a crumpled piece of "
         "the receipt.",
     ]},
    {"id": "corner_glint", "zone": (2, 9, 8, 12), "kind": "fragment",
     "fragment": "ticket_0300", "hide_fragment": "ticket_0300",
     "prompt": "Look at the glint in the corner", "title": "Old ticket",
     "text": [
         "In the dark corner lies an old paper ticket, yellow with age.",
         "",
         "CENTRAL  ->  ???     03:00     ONE WAY",
         "",
         "MTR has not used paper tickets for decades.",
     ]},
]

EXITS = {
    "1": {"to": "concourse", "entry": (5, 8), "facing": "right",
          "requires": "gate_open", "look": "shutter",
          "locked": "The gate is locked. The keypad next to it blinks red."},
}

ROOM = {
    "id": "platform",
    "name": "Platform 1",
    "map": MAP,
    "start": (41, 10),
    "objects": OBJECTS,
    "spots": SPOTS,
    "exits": EXITS,
}
