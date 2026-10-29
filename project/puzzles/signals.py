"""Puzzle 9 (all routes): the emergency shutter release in the exit hall.

Four signals must be set to the release pattern. Each route's document
(signal log, staff logbook or tunnel map) describes the pattern with
different clues. For every route, exactly one pattern fits all of its clues,
and every clue is needed (checked in tests/test_route_puzzles.py).
"""

from itertools import product

from puzzles.base import MOVES, PRESS_KEYS, SOLVED, WRONG, Puzzle

COLOURS = ["R", "Y", "G"]
COLOUR_NAMES = {"R": "RED", "Y": "YELLOW", "G": "GREEN"}
ANSWER = ("G", "R", "Y", "G")


def no_neighbours_match(p):
    return all(p[i] != p[i + 1] for i in range(3))


# Clues per route document: (text, test of a pattern (s1, s2, s3, s4)).
CLUES = {
    "signal_log": [
        ("S2 showed RED.", lambda p: p[1] == "R"),
        ("S3 was not GREEN.", lambda p: p[2] != "G"),
        ("No two neighbouring signals showed the same colour.",
         no_neighbours_match),
        ("S1 and S4 showed the same colour.", lambda p: p[0] == p[3]),
    ],
    "staff_logbook": [
        ("Exactly one signal is RED, and it is not at either end.",
         lambda p: p.count("R") == 1 and p[0] != "R" and p[3] != "R"),
        ("The two end signals show the same colour.", lambda p: p[0] == p[3]),
        ("The YELLOW is to the right of the RED.",
         lambda p: "Y" in p and "R" in p and p.index("Y") > p.index("R")),
    ],
    "tunnel_map": [
        ("No two lamps next to each other match.", no_neighbours_match),
        ("Lamp 1 and lamp 4 match.", lambda p: p[0] == p[3]),
        ("Lamps 3 and 4 are not RED.", lambda p: p[2] != "R" and p[3] != "R"),
        ("Lamp 3 is not GREEN.", lambda p: p[2] != "G"),
    ],
}
DOCUMENT_TITLES = {
    "signal_log": "SIGNAL LOG: last release",
    "staff_logbook": "STAFF LOGBOOK: release",
    "tunnel_map": "TUNNEL MAP: painted note",
}


def matching_patterns(clues):
    return [p for p in product(COLOURS, repeat=4)
            if all(test(p) for _, test in clues)]


def clue_lines(document):
    """Text of the release clues in a document, for reading and the puzzle."""
    return [f"- {text}" for text, _ in CLUES[document]]


class SignalsPuzzle(Puzzle):
    id = "signals"
    title = "Shutter release"
    hints = [
        "Your document has the release clues. Go through the four signals "
        "and cross out colours that a clue forbids.",
        "Start with the clue about RED: it tells you where the red signal "
        "is (or is not).",
        "Signal 2 is RED and signal 3 is YELLOW.",
        "The pattern is GREEN, RED, YELLOW, GREEN.",
    ]
    help_keys = [("A/D", "signal"), ("W/S", "colour"), ("E", "pull lever")]

    def reset(self):
        self.pattern = ["R", "R", "R", "R"]
        self.selected = 0
        self.flash = False

    def documents(self):
        return [doc for doc in CLUES if self.state.has(doc)]

    def handle_key(self, key):
        if key in MOVES:
            self.flash = False
            d_row, d_col = MOVES[key]
            self.selected = (self.selected + d_col) % 4
            if d_row:
                index = COLOURS.index(self.pattern[self.selected])
                self.pattern[self.selected] = COLOURS[(index - d_row) % 3]
        elif key in PRESS_KEYS:
            if tuple(self.pattern) == ANSWER:
                return SOLVED
            self.flash = True
            return WRONG
        return None

    def after_wrong(self):
        self.reset()
        self.flash = True

    def wrong_message(self):
        return ("The lever jams and every signal falls back to RED. -3 min.")

    def on_solved(self):
        self.state.flags.add("shutter_released")

    def success_lines(self):
        lines = [
            ("RELEASE ACCEPTED", "good"),
            ("", "default"),
            ("With a roar the street shutter starts to rise. Cold night air "
             "rushes in. The exit is on the right.", "default"),
        ]
        if len(self.state.fragments) >= 3:
            lines += [("", "default"),
                      ("Behind you, a crack of blue light appears in the old "
                       "wall on the left...", "fragment")]
        return lines

    # ----- drawing -----------------------------------------------------
    def draw(self, canvas, top, left, height, width, frame):
        canvas.box(top + 1, 2, 16, 40, "machine", "double",
                   "EMERGENCY RELEASE", "machine_slot", fill_style="machine")
        for index, colour in enumerate(self.pattern):
            self.draw_signal(canvas, top + 3, 5 + index * 9, index, colour)
        if self.flash:
            canvas.put(top + 14, 5, " LEVER JAMMED - TRY AGAIN ", "lcd_bad")
        else:
            canvas.put(top + 14, 5, "Set all four, then pull the lever.",
                       "machine")

        canvas.box(top + 1, 43, 16, 36, "frame", "single", "YOUR NOTES",
                   fill_style="default")
        row = top + 2
        documents = self.documents()
        if not documents:
            canvas.put(row, 45, "You have no notes about the", "dim")
            canvas.put(row + 1, 45, "release pattern.", "dim")
        from engine.canvas import wrap
        for document in documents:
            canvas.put(row, 45, DOCUMENT_TITLES[document], "info")
            row += 1
            for text, _ in CLUES[document]:
                for index, line in enumerate(wrap(text, 30)):
                    canvas.put(row, 45, ("- " if index == 0 else "  ") + line,
                               "receipt_text")
                    row += 1
            row += 1

    def draw_signal(self, canvas, top, col, index, colour):
        selected = index == self.selected
        frame_style = "btn_sel" if selected else "signal_frame"
        canvas.box(top, col, 7, 7, frame_style, "single", fill_style="signal")
        for offset, lamp in enumerate(COLOURS):
            lit = lamp == colour
            style_name = f"lamp_{lamp.lower()}" if lit else "lamp_off"
            canvas.put(top + 1 + offset * 2, col + 2, "(@)" if lit else "( )",
                       style_name)
        canvas.put(top + 7, col + 3, "│", "signal_frame")
        canvas.put(top + 8, col + 1, f"S{index + 1}", "bright" if selected
                   else "machine")
        canvas.put(top + 9, col, f"{COLOUR_NAMES[colour]:^7}",
                   f"lamp_{colour.lower()}")
