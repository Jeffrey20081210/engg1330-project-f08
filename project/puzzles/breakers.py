"""Puzzle 3 (Tech route): the breaker panel in the control room.

A 3 x 3 panel of breakers. Flipping one breaker also flips the breakers
directly above, below, left and right of it (the "Lights Out" rule). All
nine must be ON. The old panel overheats after MAX_FLIPS flips, which counts
as a wrong attempt and resets the panel.
"""

from puzzles.base import MOVES, PRESS_KEYS, SOLVED, WRONG, Puzzle

SIZE = 3
MAX_FLIPS = 10
# The panel starts as if these breakers had been flipped from "all ON",
# so flipping exactly these again is the shortest solution.
SCRAMBLE = [(0, 1), (1, 0), (1, 2), (2, 2)]


def flip(grid, row, col):
    """Flip one breaker and its four neighbours (in place)."""
    for d_row, d_col in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
        r, c = row + d_row, col + d_col
        if 0 <= r < SIZE and 0 <= c < SIZE:
            grid[r][c] = not grid[r][c]


def start_grid():
    grid = [[True] * SIZE for _ in range(SIZE)]
    for row, col in SCRAMBLE:
        flip(grid, row, col)
    return grid


def all_on(grid):
    return all(all(row) for row in grid)


class BreakersPuzzle(Puzzle):
    id = "breakers"
    title = "Breaker panel"
    hints = [
        "Each breaker flips itself AND the breakers above, below, left and "
        "right of it.",
        "Flipping the same breaker twice changes nothing, and the order does "
        "not matter. So each breaker needs flipping once or not at all.",
        "Four flips are enough. One of them is the top middle breaker.",
        "Flip: top middle, middle left, middle right, bottom right.",
    ]
    help_keys = [("WASD", "select"), ("E", "flip")]

    def reset(self):
        self.grid = start_grid()
        self.row, self.col = 1, 1
        self.flips = 0

    def handle_key(self, key):
        if key in MOVES:
            d_row, d_col = MOVES[key]
            self.row = (self.row + d_row) % SIZE
            self.col = (self.col + d_col) % SIZE
        elif key in PRESS_KEYS:
            flip(self.grid, self.row, self.col)
            self.flips += 1
            if all_on(self.grid):
                return SOLVED
            if self.flips >= MAX_FLIPS:
                return WRONG
        return None

    def wrong_message(self):
        return ("The panel overheats and trips back to the start! -3 min. "
                f"Use at most {MAX_FLIPS} flips.")

    def on_solved(self):
        self.state.flags.add("power_on")

    def success_lines(self):
        return [
            ("ALL BREAKERS ON", "good"),
            ("", "default"),
            ("The control room hums to life. The wiring panel on the right "
             "lights up.", "default"),
        ]

    # ----- drawing -----------------------------------------------------
    def draw(self, canvas, top, left, height, width, frame):
        box_left = 4
        canvas.box(top + 1, box_left, 16, 40, "machine", "double",
                   "MAIN BREAKERS", "machine_slot", fill_style="machine")
        for r in range(SIZE):
            for c in range(SIZE):
                on = self.grid[r][c]
                selected = (r, c) == (self.row, self.col)
                style_name = "switch_on" if on else "switch_off"
                col = box_left + 4 + c * 12
                row = top + 3 + r * 4
                frame_style = "btn_sel" if selected else style_name
                canvas.box(row, col, 3, 9, frame_style, "single",
                           fill_style=style_name)
                canvas.put(row + 1, col + 2, " ON  " if on else " OFF ",
                           style_name)
        flips_style = "bad" if self.flips >= MAX_FLIPS - 2 else "machine"
        canvas.put(top + 15, box_left + 3,
                   f"Flips {self.flips}/{MAX_FLIPS}", flips_style)

        info_left = 48
        canvas.box(top + 1, info_left, 16, 29, "frame", "single", "MANUAL",
                   fill_style="default")
        lines = [
            ("Turn ALL breakers ON.", "bright"),
            ("", "default"),
            ("Flipping a breaker also", "default"),
            ("flips its neighbours:", "default"),
            ("", "default"),
            ("      [ ]", "dim"),
            ("   [ ][X][ ]", "dim"),
            ("      [ ]", "dim"),
            ("", "default"),
            (f"Overheats after {MAX_FLIPS} flips.", "warn"),
        ]
        for index, (text, style_name) in enumerate(lines):
            canvas.put(top + 3 + index, info_left + 2, text, style_name)
