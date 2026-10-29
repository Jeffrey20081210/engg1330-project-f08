"""Puzzle 1: the platform gate keypad.

The gate needs a 3-digit staff code made of three different digits. The
ticket machine's maintenance log printed five earlier failed attempts, each
with how many digits were right. The log was torn into three pieces that the
player must find on the platform (ticket machine, bin, bench).

The five entries were chosen so that exactly one code fits all of them, and
every entry is needed: with any one missing, several codes would fit. The
tests in tests/test_gate_code.py check both facts.
"""

from itertools import permutations

from puzzles.base import MOVES, SOLVED, WRONG, Puzzle

CODE = "964"

# (attempt, digits right and in the right place, right but in the wrong place)
LOG = {
    "receipt_a": [("957", 1, 0), ("149", 0, 2)],
    "receipt_b": [("407", 0, 1), ("276", 0, 1)],
    "receipt_c": [("823", 0, 0)],
}
PIECE_ORDER = ["receipt_a", "receipt_b", "receipt_c"]

# Keypad layout: rows of buttons. "<" deletes a digit, "OK" submits.
BUTTONS = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"], ["<", "0", "OK"]]


def score(attempt, code):
    """Return (right place, wrong place) for an attempt against a code."""
    right_place = sum(1 for a, c in zip(attempt, code) if a == c)
    common = len(set(attempt) & set(code))
    return right_place, common - right_place


def describe(right_place, wrong_place):
    """The sentence the maintenance log prints for one attempt."""
    if right_place == 0 and wrong_place == 0:
        return "nothing is correct"
    parts = []
    if right_place:
        parts.append(f"{number_word(right_place)} correct, right place")
    if wrong_place:
        parts.append(f"{number_word(wrong_place)} correct, wrong place")
    return "; ".join(parts)


def number_word(count):
    return {1: "one", 2: "two", 3: "three"}[count]


def receipt_lines(piece):
    """Text lines of one receipt piece, e.g. '957  one correct, right place'."""
    return [f"{attempt}  {describe(right, wrong)}"
            for attempt, right, wrong in LOG[piece]]


def all_entries(pieces=PIECE_ORDER):
    return [entry for piece in pieces for entry in LOG[piece]]


def matching_codes(entries):
    """Every 3-different-digit code that fits all the given log entries."""
    codes = ["".join(p) for p in permutations("0123456789", 3)]
    return [code for code in codes
            if all(score(attempt, code) == (right, wrong)
                   for attempt, right, wrong in entries)]


class GateCodePuzzle(Puzzle):
    id = "gate_code"
    title = "Platform gate keypad"
    hints = [
        "Find all three torn pieces of the receipt first: the ticket machine, "
        "the bin and the bench.",
        "823: nothing is correct, so 8, 2 and 3 are not in the code at all.",
        "149 has two correct digits, both in the wrong place. Compare it "
        "with 957 and 407 to see which two of 1, 4 and 9 they are.",
        "The code ends in 4.",
    ]
    help_keys = [("WASD", "select"), ("E", "press"), ("0-9", "type")]

    def reset(self):
        self.entry = ""
        self.row, self.col = 0, 0
        self.flash = None            # "bad" briefly after a wrong code

    def press(self, label):
        """Press one keypad button. Returns SOLVED, WRONG or None."""
        self.flash = None
        if label == "<":
            self.entry = self.entry[:-1]
        elif label == "OK":
            return self.submit()
        elif len(self.entry) < 3:
            self.entry += label
        return None

    def submit(self):
        if len(self.entry) < 3:
            return None              # nothing to check yet; no penalty
        if self.entry == CODE:
            return SOLVED
        self.flash = self.entry
        return WRONG

    def handle_key(self, key):
        if key in MOVES:
            d_row, d_col = MOVES[key]
            self.row = (self.row + d_row) % len(BUTTONS)
            self.col = (self.col + d_col) % len(BUTTONS[0])
            return None
        if len(key) == 1 and key in "0123456789":
            return self.press(key)
        if key == "backspace":
            return self.press("<")
        if key in ("e", "space"):
            return self.press(BUTTONS[self.row][self.col])
        if key == "enter":
            return self.press("OK")
        return None

    def after_wrong(self):
        """Clear the entry but keep showing which code was denied."""
        denied = self.flash
        self.reset()
        self.flash = denied

    def on_solved(self):
        self.state.flags.add("gate_open")

    def success_lines(self):
        return [
            ("ACCESS GRANTED", "good"),
            ("", "default"),
            ("With a long metal groan the platform gate slides open. Stairs "
             "lead up to the concourse.", "default"),
        ]

    # ----- drawing -----------------------------------------------------
    def draw(self, canvas, top, left, height, width, frame):
        self.draw_keypad(canvas, top + 1, left + 4, frame)
        self.draw_log(canvas, top + 1, left + 36)

    def draw_keypad(self, canvas, top, left, frame):
        canvas.box(top, left, 16, 27, "machine", "double", "STAFF OVERRIDE",
                   "machine_slot", fill_style="machine")
        # Display
        shown = (self.entry + "___")[:3]
        if self.flash:
            text, lcd = f" DENIED {self.flash} ", "lcd_bad"
        else:
            text, lcd = f"  CODE  {' '.join(shown)}  ", "lcd"
        canvas.put(top + 2, left + 3, f"{text:^21}", lcd)
        canvas.put(top + 3, left + 3, "3 different digits", "machine")
        # Buttons
        for r, button_row in enumerate(BUTTONS):
            for c, label in enumerate(button_row):
                selected = (r, c) == (self.row, self.col)
                name = "btn_sel" if selected else "btn"
                canvas.put(top + 5 + r * 2, left + 3 + c * 7, f"[{label:^4}]",
                           name)

    def draw_log(self, canvas, top, left):
        canvas.box(top, left, 16, 38, "frame", "single", "MAINTENANCE LOG",
                   fill_style="default")
        row = top + 2
        found = [p for p in PIECE_ORDER if p in self.state.clues]
        canvas.put(top + 1, left + 2, "FAILED GATE CODES", "dim")
        for piece in PIECE_ORDER:
            if piece in found:
                for line in receipt_lines(piece):
                    canvas.put(row, left + 2, f" {line:<33}", "receipt")
                    row += 1
            else:
                canvas.put(row, left + 2, f" {'~ torn piece missing ~':^33}",
                           "receipt_missing")
                row += 1
            row += 1
        canvas.put(top + 13, left + 2,
                   f"Pieces found: {len(found)}/{len(PIECE_ORDER)}",
                   "info" if len(found) < 3 else "good")
