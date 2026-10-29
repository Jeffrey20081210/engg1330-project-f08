"""Human route: the ticket office. P5 safe, then P6 broadcast console."""

from puzzles.stations import logbook_lines
from rooms.route_room import ROUTE_MAP, START, back_to_concourse

OBJECTS = [
    {"pos": (20, 0), "art": ["═══════"], "style": "light_on"},
    {"pos": (52, 0), "art": ["═══════"], "style": "light_on"},
    # Wall safe (P5)
    {"pos": (6, 1),
     "art": ["╔═══════╗", "║ (o) # ║", "╚═══════╝"],
     "mask": ["sssssssss", "sssssssss", "sssssssss"],
     "palette": {"s": "safe"}},
    # Island Line staff map poster
    {"pos": (28, 0),
     "art": ["┌──────────────────┐", "│ ISLAND LINE  MAP │",
             "│o-o-o-o-O-O-o-o-o-│", "└──────────────────┘"],
     "mask": ["f" * 20, "f" + "r" * 18 + "f", "f" + "b" * 18 + "f", "f" * 20],
     "palette": {"f": "poster_frame", "r": "poster_red", "b": "poster_blue"}},
    # Broadcast console (P6)
    {"pos": (58, 1),
     "art": ["╔════════════╗", "║ ((o)) ▓▓▓▓ ║", "╚════════════╝"],
     "mask": ["m" * 14, "m" + "s" * 12 + "m", "m" * 14],
     "palette": {"m": "machine", "s": "machine_screen"}},
    # Ticket counter with a window
    {"pos": (20, 9), "solid": "box", "style": "bench",
     "art": ["╔══════════════════╗", "║  TICKET  OFFICE  ║", "╚══════════════════╝"]},
    # Desk with the drawer
    {"pos": (60, 10), "solid": "box", "style": "bench",
     "art": ["╔══════════╗", "║ =  [__]  ║", "╚══════════╝"]},
]

SPOTS = [
    {"id": "safe", "zone": (3, 4, 16, 5), "kind": "puzzle",
     "puzzle": "stations", "prompt": "Open the wall safe", "marker": (10, 0),
     "done_text": "The safe is open and empty now."},
    {"id": "line_map", "zone": (26, 4, 49, 5), "kind": "read",
     "prompt": "Look at the staff map", "title": "Island Line staff map",
     "text": [
         "The Island Line with staff numbers, from 01 Kennedy Town in the "
         "west to 17 Chai Wan in the east.",
         "",
         "Big O marks are interchange stations. The same map is shown on "
         "the safe's screen.",
     ]},
    {"id": "logbook", "zone": (18, 7, 41, 8), "kind": "read",
     "prompt": "Read the logbook on the counter", "title": "Staff logbook",
     "item": "staff_logbook",
     "text": logbook_lines() + ["", "(More pages follow. Press I later.)"]},
    {"id": "broadcast", "zone": (56, 4, 74, 5), "kind": "puzzle",
     "puzzle": "morse", "prompt": "Use the broadcast console",
     "marker": (64, 0), "requires": "safe_open",
     "locked_text": "The console is locked. The key must be somewhere safe...",
     "done_text": "The night controller is already opening the exit hall."},
    {"id": "drawer", "zone": (58, 8, 73, 9), "kind": "fragment",
     "fragment": "staff_photo", "hide_fragment": "staff_photo",
     "prompt": "Search the desk drawer", "title": "Old photograph",
     "text": [
         "Under old timetables lies a photo of the night shift, 1989.",
         "",
         "On the back: \"For Mr Leung, night controller, on his last night. "
         "He said he would keep driving the 03:00.\"",
         "",
         "The tired voice on the intercom sounds just like him.",
     ]},
]

ROOM = {
    "id": "ticket_office",
    "name": "Ticket office",
    "map": ROUTE_MAP,
    "start": START,
    "first_visit": "The office key turns. A tired voice crackles on the "
                   "intercom: \"Who is there? Tell me tonight's password.\"",
    "objects": OBJECTS,
    "spots": SPOTS,
    "exits": {"1": back_to_concourse(39)},
}
