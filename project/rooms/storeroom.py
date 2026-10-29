"""Sneak route: the storeroom. P7 crates, then P8 down the hatch."""

from rooms.route_room import ROUTE_MAP, START, back_to_concourse

CRATE = ["╔══╗", "╚══╝"]

OBJECTS = [
    {"pos": (36, 0), "art": ["═══════"], "style": "light_on", "flicker": True},
    {"pos": (5, 1),
     "art": ["┌────────────┐", "│ TUNNEL 3   │", "│ STAFF ONLY │", "└────────────┘"],
     "mask": ["f" * 14, "f" + "r" * 12 + "f", "f" + "r" * 12 + "f", "f" * 14],
     "palette": {"f": "poster_frame", "r": "poster_red"}},
    # Shelves along the walls
    {"pos": (4, 6), "solid": True, "style": "shelf",
     "art": ["████████████", "▒▒▒▒▒▒▒▒▒▒▒▒"]},
    {"pos": (64, 6), "solid": True, "style": "shelf",
     "art": ["████████████", "▒▒▒▒▒▒▒▒▒▒▒▒"]},
    # Crates piled on the floor hatch
    {"pos": (36, 6), "solid": True, "style": "crate", "art": CRATE,
     "hide_flags": ["hatch_clear"]},
    {"pos": (40, 6), "solid": True, "style": "crate", "art": CRATE,
     "hide_flags": ["hatch_clear"]},
    {"pos": (38, 8), "solid": True, "style": "crate", "art": CRATE,
     "hide_flags": ["hatch_clear"]},
    {"pos": (36, 8), "art": ["[ HATCH ]"], "style": "hatch",
     "needs_flags": ["hatch_clear"]},
    {"pos": (20, 10), "solid": True, "style": "crate", "art": CRATE},
    {"pos": (54, 12), "solid": True, "style": "crate", "art": CRATE},
    # Fragment 3 (Sneak): an old conductor's cap on the shelf
    {"pos": (70, 5), "art": ["*"], "style": "fragment", "blink": "rare",
     "hide_fragment": "conductor_cap"},
]

SPOTS = [
    {"id": "tunnel_hatch", "zone": (30, 6, 50, 13), "kind": "puzzle",
     "puzzle": "tunnel", "prompt": "Climb down into the tunnel",
     "needs_flags": ["hatch_clear"]},
    {"id": "crates", "zone": (30, 10, 50, 13), "kind": "puzzle",
     "puzzle": "boxes", "prompt": "Move the crates off the hatch",
     "marker": (39, 5), "hide_flags": ["hatch_clear"]},
    {"id": "sign", "zone": (3, 4, 19, 5), "kind": "read",
     "prompt": "Read the sign", "title": "Sign",
     "text": [
         "TUNNEL 3 - STAFF ONLY. Cameras in operation. Security patrols "
         "all night.",
         "",
         "Underneath, in marker: \"cams turn every step. guards never look "
         "back.\"",
     ]},
    {"id": "cap", "zone": (64, 4, 77, 5), "kind": "fragment",
     "fragment": "conductor_cap", "hide_fragment": "conductor_cap",
     "prompt": "Look at the top shelf", "title": "Conductor's cap",
     "text": [
         "A dusty conductor's cap from a uniform that MTR stopped using "
         "long ago. A paper tag is tied to it:",
         "",
         "\"03:00 service - for everyone who missed the last train.\"",
     ]},
]

ROOM = {
    "id": "storeroom",
    "name": "Storeroom",
    "map": ROUTE_MAP,
    "start": START,
    "first_visit": "The maintenance key opens the storeroom. Crates are "
                   "piled on a floor hatch marked TUNNEL 3.",
    "objects": OBJECTS,
    "spots": SPOTS,
    "exits": {"1": back_to_concourse(64)},
}
