"""Puzzle 5 (Human route): the ticket office safe.

The safe code is two staff members' home station numbers on the Island
Line staff map (01 Kennedy Town ... 17 Chai Wan): Ah Fai's number, then
Mei's. The staff logbook gives a few clues about each station; only the
map shown in the puzzle is needed, no real-world MTR knowledge.

Each person's clues fit exactly one station, and every clue is needed
(checked in tests/test_route_puzzles.py).
"""

from engine.canvas import wrap
from puzzles.base import SOLVED, WRONG, Puzzle

# Island Line stations from west to east; True marks interchange stations.
STATIONS = [
    ("Kennedy Town", False), ("HKU", False), ("Sai Ying Pun", False),
    ("Sheung Wan", False), ("Central", True), ("Admiralty", True),
    ("Wan Chai", False), ("Causeway Bay", False), ("Tin Hau", False),
    ("Fortress Hill", False), ("North Point", True), ("Quarry Bay", True),
    ("Tai Koo", False), ("Sai Wan Ho", False), ("Shau Kei Wan", False),
    ("Heng Fa Chuen", False), ("Chai Wan", False),
]
CENTRAL, ADMIRALTY, CHAI_WAN = 5, 6, 17


def words(number):
    return len(STATIONS[number - 1][0].split())


# Clues: (text, test of a station number).
CLUES = {
    "Ah Fai": [
        ("My station is east of Admiralty.", lambda n: n > ADMIRALTY),
        ("Its name has three words.", lambda n: words(n) == 3),
        ("From my station to Chai Wan is an even number of stops.",
         lambda n: (CHAI_WAN - n) % 2 == 0),
    ],
    "Mei": [
        ("My station is west of Central.", lambda n: n < CENTRAL),
        ("Its number on the staff map is even.", lambda n: n % 2 == 0),
        ("Its name has more than one word.", lambda n: words(n) > 1),
    ],
}
ORDER = ["Ah Fai", "Mei"]


def matching_stations(clues):
    return [n for n in range(1, len(STATIONS) + 1)
            if all(test(n) for _, test in clues)]


def safe_code():
    return "".join(f"{matching_stations(CLUES[who])[0]:02d}" for who in ORDER)


def logbook_lines():
    """The logbook text (also shown when reading it in the room)."""
    lines = ["SAFE CODE: Ah Fai's station number, then Mei's (4 digits).", ""]
    for who in ORDER:
        lines.append(f"{who}:")
        lines += [f"  \"{text}\"" for text, _ in CLUES[who]]
    return lines


class StationsPuzzle(Puzzle):
    id = "stations"
    title = "Ticket office safe"
    hints = [
        "Use the staff map: each station has a two-digit number, from 01 in "
        "the west to 17 in the east.",
        "Ah Fai: east of Admiralty with three words leaves 14, 15 and 16. "
        "Now count the stops from each to Chai Wan (17).",
        "Mei: west of Central and even leaves 02 HKU and 04 Sheung Wan.",
        "The code starts with 15.",
    ]
    help_keys = [("0-9", "type"), ("Bksp", "delete"), ("Enter", "try")]

    def reset(self):
        self.entry = ""
        self.flash = None

    def handle_key(self, key):
        if len(key) == 1 and key in "0123456789":
            self.flash = None
            if len(self.entry) < 4:
                self.entry += key
        elif key == "backspace":
            self.flash = None
            self.entry = self.entry[:-1]
        elif key in ("enter", "e"):
            if len(self.entry) < 4:
                return None
            if self.entry == safe_code():
                return SOLVED
            self.flash = self.entry
            return WRONG
        return None

    def after_wrong(self):
        denied = self.flash
        self.reset()
        self.flash = denied

    def on_solved(self):
        self.state.flags.add("safe_open")
        self.state.give("staff_logbook")     # its last page is needed later

    def success_lines(self):
        return [
            ("The safe door swings open.", "good"),
            ("", "default"),
            ("Inside: the key to the broadcast console and a strip of "
             "punched tape from tonight's midnight broadcast.", "default"),
            ("You keep the staff logbook: its last page describes the exit "
             "release pattern (press I).", "bright"),
        ]

    # ----- drawing -----------------------------------------------------
    def draw(self, canvas, top, left, height, width, frame):
        canvas.box(top + 1, 1, 16, 40, "frame", "single",
                   "ISLAND LINE - STAFF MAP", fill_style="default")
        for index, (name, interchange) in enumerate(STATIONS):
            number = index + 1
            col = 3 if index < 9 else 22
            row = top + 3 + (index if index < 9 else index - 9)
            mark = "<>" if interchange else "  "
            canvas.put(row, col, f"{number:02d}", "lcd")
            canvas.put(row, col + 3, f"{name:<13}", "info")
            canvas.put(row, col + 16, mark, "warn")
        canvas.put(top + 13, 22, "<> interchange", "warn")
        canvas.put(top + 14, 22, "West -> East", "dim")

        canvas.box(top + 1, 42, 13, 37, "frame", "single", "STAFF LOGBOOK",
                   fill_style="default")
        row = top + 2
        for who in ORDER:
            canvas.put(row, 44, f"{who}:", "info")
            row += 1
            for text, _ in CLUES[who]:
                for index, line in enumerate(wrap(text, 32)):
                    canvas.put(row, 44, ("- " if index == 0 else "  ") + line,
                               "receipt_text")
                    row += 1
            row += 1

        canvas.box(top + 14, 42, 4, 37, "machine", "double",
                   "SAFE: AH FAI, THEN MEI", "machine_slot",
                   fill_style="machine")
        shown = " ".join((self.entry + "____")[:4])
        if self.flash:
            text, lcd = f" WRONG {self.flash} ", "lcd_bad"
        else:
            text, lcd = f"  CODE  {shown}  ", "lcd"
        canvas.put(top + 15, 48, f"{text:^25}", lcd)
