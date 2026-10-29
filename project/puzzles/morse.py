"""Puzzle 6 (Human route): tonight's password from the midnight broadcast.

Needs the safe (P5) first: the safe holds the punched tape. The tape shows
the password in Morse code, but the punch machine dropped the gaps between
letters. The night controller's whiteboard lists eight possible passwords;
exactly one of them gives this tape (checked in the tests).
"""

from puzzles.base import MOVES, PRESS_KEYS, SOLVED, WRONG, Puzzle

MORSE = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.",
    "G": "--.", "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..",
    "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.",
    "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
    "Y": "-.--", "Z": "--..",
}

ANSWER = "RETURN"
CANDIDATES = ["TUNNEL", "GHOST", "SILENT", "ISLAND", "RETURN", "NIGHT",
              "EASTERN", "SIGNAL"]


def to_morse(word):
    """The tape for a word: Morse letters with no gaps between them."""
    return "".join(MORSE[letter] for letter in word)


TAPE = to_morse(ANSWER)


class MorsePuzzle(Puzzle):
    id = "morse"
    title = "Broadcast console"
    hints = [
        "Count the dots and dashes on the tape. Only words whose Morse code "
        "has exactly the same length can match.",
        f"The tape has {len(TAPE)} symbols. Four of the words have that "
        "length: work out each one's Morse code letter by letter.",
        "Compare the first few symbols: the tape starts with .-..",
        "The password starts with R.",
    ]
    help_keys = [("W/S", "choose"), ("E", "broadcast")]

    def reset(self):
        self.choice = 0
        self.flash = None

    def handle_key(self, key):
        if key in MOVES:
            self.flash = None
            d_row, d_col = MOVES[key]
            # W/S move within a column, A/D jump to the other column.
            self.choice = (self.choice + d_row + 4 * d_col) % len(CANDIDATES)
        elif key in PRESS_KEYS:
            if CANDIDATES[self.choice] == ANSWER:
                return SOLVED
            self.flash = CANDIDATES[self.choice]
            return WRONG
        return None

    def after_wrong(self):
        choice, flash = self.choice, self.flash
        self.reset()
        self.choice, self.flash = choice, flash

    def wrong_message(self):
        return (f"You say \"{self.flash}\". The intercom crackles: \"That is "
                "not tonight's password.\" -3 min.")

    def on_solved(self):
        self.state.flags.add("exit_hall_open")

    def success_lines(self):
        return [
            ("\"RETURN. ...Correct.\"", "good"),
            ("", "default"),
            ("An old, tired voice on the intercom: \"Good. I am opening the "
             "exit hall for you. Go, before 01:30.\"", "default"),
            ("Far away, a shutter rattles open in the concourse.", "bright"),
        ]

    # ----- drawing -----------------------------------------------------
    def draw(self, canvas, top, left, height, width, frame):
        canvas.box(top + 1, 1, 6, 78, "machine", "double",
                   "PUNCHED TAPE - 00:00 BROADCAST", "machine_slot",
                   fill_style="machine")
        tape = " ".join(TAPE)
        canvas.put_center(top + 3, f" {tape} ", "receipt", 1, 78)
        canvas.put_center(top + 5, "(the punch machine dropped the gaps "
                          "between letters)", "machine", 1, 78)

        canvas.box(top + 7, 1, 11, 46, "frame", "single", "MORSE CODE",
                   fill_style="default")
        letters = sorted(MORSE)
        for index, letter in enumerate(letters):
            col = 3 + (index // 9) * 15
            row = top + 8 + index % 9
            canvas.put(row, col, letter, "bright")
            canvas.put(row, col + 2, MORSE[letter], "info")

        canvas.box(top + 7, 48, 11, 31, "frame", "single",
                   "WHITEBOARD: PASSWORDS", fill_style="default")
        for index, word in enumerate(CANDIDATES):
            col = 51 + (index // 4) * 13
            row = top + 9 + (index % 4) * 2
            selected = index == self.choice
            style_name = "btn_sel" if selected else "btn"
            if word == self.flash:
                style_name = "lcd_bad"
            canvas.put(row, col, f" {word:<8} ", style_name)
