"""Tech route: the control room. P3 breakers, then P4 wiring."""

from rooms.route_room import ROUTE_MAP, START, back_to_concourse

OBJECTS = [
    {"pos": (12, 0), "art": ["═══════"], "style": "light_on"},
    {"pos": (60, 0), "art": ["═══════"], "style": "light_on", "flicker": True},
    # Breaker panel (P3)
    {"pos": (5, 1),
     "art": ["┌──────────┐", "│ | | | |  │", "└──────────┘"],
     "mask": ["mmmmmmmmmmmm", "mssssssssssm", "mmmmmmmmmmmm"],
     "palette": {"m": "machine", "s": "switch_off"},
     "flag_palette": {"flag": "power_on",
                      "palette": {"m": "machine", "s": "switch_on"}}},
    # Signal screen in the middle of the back wall
    {"pos": (27, 0),
     "art": ["╔════════════════════════╗",
             "║ ─o──o──o──o──o─  TRACK1║",
             "║ ─ ─ ─ ─ ─ ─ ─ ─  TRACK0║",
             "╚════════════════════════╝"],
     "mask": ["m" * 26, "m" + "s" * 24 + "m", "m" + "t" * 24 + "m", "m" * 26],
     "palette": {"m": "machine", "s": "machine_screen", "t": "track0"}},
    # Wiring panel (P4)
    {"pos": (62, 1),
     "art": ["┌──────────┐", "│ ┼─┐ └─┼  │", "└──────────┘"],
     "mask": ["mmmmmmmmmmmm", "mccccccccccm", "mmmmmmmmmmmm"],
     "palette": {"m": "machine", "c": "cable_off"},
     "flag_palette": {"flag": "exit_hall_open",
                      "palette": {"m": "machine", "c": "cable_on"}}},
    # Server racks
    {"pos": (4, 8), "solid": True,
     "art": ["┌──┐┌──┐", "│::││::│", "│::││::│", "└──┘└──┘"],
     "mask": ["rrrrrrrr"] * 4, "palette": {"r": "machine"}},
    # Operator desk with an old monitor
    {"pos": (60, 9), "solid": "box", "style": "bench",
     "art": ["  ┌───┐   ", "  │ _ │   ", "╔═╧═══╧══╗"]},
    # Fragment 3 (Tech): a yellowed note stuck to the old monitor
    {"pos": (63, 8), "art": ["*"], "style": "fragment", "blink": "rare",
     "hide_fragment": "signal_note"},
]

SPOTS = [
    {"id": "breaker_panel", "zone": (3, 4, 19, 5), "kind": "puzzle",
     "puzzle": "breakers", "prompt": "Use the breaker panel",
     "marker": (10, 0), "done_text": "All breakers are ON."},
    {"id": "signal_screen", "zone": (26, 4, 53, 5), "kind": "read",
     "prompt": "Look at the signal screen", "title": "Signal screen",
     "text": [
         "TRACK 1 shows the Island Line, every signal red for the night.",
         "",
         "Below it is a line labelled TRACK 0. There is no Track 0 at "
         "Central. One signal on it is slowly blinking green.",
     ]},
    {"id": "wiring_panel", "zone": (60, 4, 76, 5), "kind": "puzzle",
     "puzzle": "wires", "prompt": "Use the wiring panel", "marker": (67, 0),
     "requires": "power_on",
     "locked_text": "The wiring panel is dead. Fix the main breakers first.",
     "done_text": "The shutter motor already has power."},
    {"id": "old_monitor", "zone": (56, 7, 72, 8), "kind": "fragment",
     "fragment": "signal_note", "hide_fragment": "signal_note",
     "prompt": "Look at the note on the monitor", "title": "Yellowed note",
     "text": [
         "A note in old handwriting, stuck to the monitor:",
         "",
         "\"TRACK 0 - 03:00 - DO NOT REPORT. It only stops for people who "
         "missed the last train.\"",
     ]},
]

ROOM = {
    "id": "control_room",
    "name": "Control room",
    "map": ROUTE_MAP,
    "start": START,
    "first_visit": "The keycard opens the control room. It is cold and "
                   "dark: the main breakers are off.",
    "objects": OBJECTS,
    "spots": SPOTS,
    "exits": {"1": back_to_concourse(14)},
}
