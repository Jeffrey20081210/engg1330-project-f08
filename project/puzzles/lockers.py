"""Puzzle 2: the shift lockers in the concourse. Solving it picks the route.

Four lockers hold the staff keycard (Tech route), the ticket office key
(Human route), the cleaner's maintenance key (Sneak route), and nothing.
Four staff notes say where things are, but exactly one note is a lie.
The locker system allows one access per shift, so the player chooses which
tool to collect and opens that locker. A wrong locker costs time.

Only one arrangement leaves exactly one note false, and every note is
needed for that (checked in tests/test_route_puzzles.py).
"""

from itertools import permutations

from puzzles.base import MOVES, PRESS_KEYS, SOLVED, WRONG, Puzzle

# Locker number -> what is inside (lockers are numbered 1-4 from the left).
CONTENTS = {1: "office_key", 2: "empty", 3: "keycard", 4: "maintenance_key"}

TOOLS = [  # (item, name, route)
    ("keycard", "Staff keycard", "tech"),
    ("office_key", "Ticket office key", "human"),
    ("maintenance_key", "Maintenance key", "sneak"),
]

# Each note: (who, what they wrote, test of an arrangement {item: locker}).
NOTES = [
    ("Ming, station porter",
     "Locker 3 is the empty one.",
     lambda where: where["empty"] == 3),
    ("Ka-yan, ticket office",
     "My office key is somewhere to the left of the empty locker.",
     lambda where: where["office_key"] < where["empty"]),
    ("Siu-wai, technician",
     "The keycard is somewhere to the left of the maintenance key.",
     lambda where: where["keycard"] < where["maintenance_key"]),
    ("Uncle Chan, cleaner",
     "The empty locker is somewhere to the left of my maintenance key.",
     lambda where: where["empty"] < where["maintenance_key"]),
]

ITEMS = ["keycard", "office_key", "maintenance_key", "empty"]


def arrangements_with_one_liar(notes=NOTES):
    """All arrangements in which exactly one of the notes is false."""
    found = []
    for order in permutations(range(1, 5)):
        where = dict(zip(ITEMS, order))
        false_notes = [n for n in notes if not n[2](where)]
        if len(false_notes) == 1:
            found.append(where)
    return found


class LockersPuzzle(Puzzle):
    id = "lockers"
    title = "Shift lockers"
    hints = [
        "Exactly one note is a lie. Pick one person, pretend they lie, and "
        "check whether the other three notes can all be true together.",
        "Suppose Ming tells the truth (locker 3 is empty). Then Uncle Chan's "
        "key must be in locker 4... try each other person as the liar: "
        "none of them works.",
        "So Ming is the liar: locker 3 is NOT empty. Now the other three "
        "notes are all true.",
        "Locker 2 is the empty one.",
    ]
    help_keys = [("W/S", "tool"), ("A/D", "locker"), ("E", "open")]

    def reset(self):
        self.tool = 0          # index in TOOLS
        self.locker = 1        # 1-4
        self.confirming = False
        self.flash = None

    def handle_key(self, key):
        if self.confirming:
            if key in ("y", "enter", "e"):
                self.confirming = False
                return self.open_locker()
            if key in ("n", "esc", "backspace"):
                self.confirming = False
            return None
        self.flash = None
        if key in MOVES:
            d_row, d_col = MOVES[key]
            self.tool = (self.tool + d_row) % len(TOOLS)
            self.locker = (self.locker - 1 + d_col) % 4 + 1
        elif len(key) == 1 and key in "1234":
            self.locker = int(key)
        elif key in PRESS_KEYS:
            self.confirming = True
        return None

    def open_locker(self):
        item = TOOLS[self.tool][0]
        if CONTENTS[self.locker] == item:
            return SOLVED
        self.flash = self.locker
        return WRONG

    def after_wrong(self):
        locker, tool = self.flash, self.tool
        self.reset()
        self.flash, self.tool, self.locker = locker, tool, locker

    def wrong_message(self):
        return (f"Locker {self.flash} does not hold that. Security lockout: "
                "-3 min.")

    def on_solved(self):
        item, _, route = TOOLS[self.tool]
        self.state.route = route
        self.state.flags.add(f"route_{route}")
        self.state.give(item)

    def success_lines(self):
        item, name, route = TOOLS[self.tool]
        door = {"tech": "the CONTROL ROOM", "human": "the TICKET OFFICE",
                "sneak": "the STAFF ONLY storeroom"}[route]
        return [
            (f"Locker {self.locker} clicks open: {name}!", "good"),
            ("", "default"),
            ("The other lockers lock with a heavy clunk. One access per "
             "shift.", "default"),
            (f"Your key opens {door} door in the concourse.", "bright"),
        ]

    # ----- drawing -----------------------------------------------------
    def draw(self, canvas, top, left, height, width, frame):
        self.draw_lockers(canvas, top + 1, 2)
        self.draw_notes(canvas, top + 1, 42)

    def draw_lockers(self, canvas, top, left):
        canvas.box(top, left, 16, 38, "machine", "double", "SHIFT LOCKERS",
                   "machine_slot", fill_style="machine")
        for number in range(1, 5):
            col = left + 3 + (number - 1) * 8
            selected = number == self.locker
            style_name = "btn_sel" if selected else "locker"
            if self.flash == number:
                style_name = "lcd_bad"
            canvas.box(top + 2, col, 6, 7, style_name, "single",
                       fill_style=style_name)
            canvas.put(top + 3, col + 2, f"{number}", style_name)
            canvas.put(top + 5, col + 1, " ═══ ", style_name)
        canvas.put(top + 8, left + 2, "Collect:", "machine")
        canvas.put(top + 8, left + 13, "(1-4, left to right)", "machine")
        for index, (_, name, _) in enumerate(TOOLS):
            selected = index == self.tool
            canvas.put(top + 9 + index, left + 3,
                       f"{'>' if selected else ' '} {name:<20}",
                       "btn_sel" if selected else "btn")
        if self.confirming:
            name = TOOLS[self.tool][1]
            canvas.put(top + 13, left + 2, f"Open locker {self.locker} for the",
                       "warn")
            canvas.put(top + 14, left + 2, f"{name.lower()}?  Y / N", "warn")
        else:
            canvas.put(top + 13, left + 2, "ONE ACCESS PER SHIFT.", "machine_slot")
            canvas.put(top + 14, left + 2, "Wrong locker = 3 min lockout.",
                       "machine")

    def draw_notes(self, canvas, top, left):
        canvas.box(top, left, 16, 37, "frame", "single",
                   "4 NOTES - EXACTLY ONE LIES", "warn", fill_style="default")
        row = top + 1
        for who, text, _ in NOTES:
            canvas.put(row, left + 2, who, "info")
            for line in wrap_note(text, 32):
                row += 1
                canvas.put(row, left + 3, line, "receipt")
            row += 2


def wrap_note(text, width):
    from engine.canvas import wrap
    return [f"{line:<{width}}" for line in wrap(text, width)]
