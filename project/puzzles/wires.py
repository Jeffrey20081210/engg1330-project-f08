"""Puzzle 4 (Tech route): the wiring panel. Needs the breakers (P3) first.

A grid of cable tiles. Pressing E turns the selected tile a quarter turn
clockwise. Power enters from the socket on the left of row SOURCE_ROW and
must reach the shutter motor on the right of row TARGET_ROW. Tiles that
carry power are drawn in yellow, so the player sees how far it gets.
"""

from puzzles.base import MOVES, PRESS_KEYS, SOLVED, Puzzle

N, E, S, W = "N", "E", "S", "W"
TURN = {N: E, E: S, S: W, W: N}           # a quarter turn clockwise
OPPOSITE = {N: S, S: N, E: W, W: E}
STEP = {N: (-1, 0), S: (1, 0), E: (0, 1), W: (0, -1)}

# Tile shapes in their "rotation 0" position.
SHAPES = {"I": {N, S}, "L": {N, E}, "T": {N, E, S}}

# The panel: rows of (shape, starting rotation). Rotation r means the shape
# has been turned clockwise r times.
GRID = [
    [("L", 2), ("L", 0), ("I", 0), ("L", 3), ("T", 1), ("L", 1)],
    [("I", 0), ("L", 1), ("T", 2), ("I", 1), ("L", 0), ("I", 1)],
    [("T", 0), ("I", 0), ("L", 2), ("L", 3), ("I", 0), ("I", 0)],
    [("L", 1), ("T", 3), ("I", 1), ("L", 0), ("T", 0), ("L", 2)],
]
ROWS, COLS = len(GRID), len(GRID[0])
SOURCE_ROW, TARGET_ROW = 1, 2

# Box-drawing character for each set of connections.
CENTRE = {
    frozenset({N, S}): "│", frozenset({E, W}): "─",
    frozenset({N, E}): "└", frozenset({N, W}): "┘",
    frozenset({S, E}): "┌", frozenset({S, W}): "┐",
    frozenset({N, E, S}): "├", frozenset({N, S, W}): "┤",
    frozenset({E, S, W}): "┬", frozenset({N, E, W}): "┴",
}


def connections(shape, rotation):
    sides = SHAPES[shape]
    for _ in range(rotation % 4):
        sides = {TURN[side] for side in sides}
    return sides


def powered_tiles(rotations):
    """Tiles reached by power from the socket (a flood fill)."""
    start = (SOURCE_ROW, 0)
    if W not in connections(GRID[SOURCE_ROW][0][0], rotations[SOURCE_ROW][0]):
        return set()
    seen = {start}
    todo = [start]
    while todo:
        row, col = todo.pop()
        for side in connections(GRID[row][col][0], rotations[row][col]):
            d_row, d_col = STEP[side]
            r, c = row + d_row, col + d_col
            if not (0 <= r < ROWS and 0 <= c < COLS) or (r, c) in seen:
                continue
            if OPPOSITE[side] in connections(GRID[r][c][0], rotations[r][c]):
                seen.add((r, c))
                todo.append((r, c))
    return seen


def motor_powered(rotations):
    last = (TARGET_ROW, COLS - 1)
    return (last in powered_tiles(rotations)
            and E in connections(GRID[last[0]][last[1]][0],
                                 rotations[last[0]][last[1]]))


class WiresPuzzle(Puzzle):
    id = "wires"
    title = "Wiring panel"
    hints = [
        "Power comes in on the left of row 2 and must leave on the right of "
        "row 3. Yellow cables already carry power.",
        "Work outwards from the socket: turn each tile until it joins the "
        "last yellow tile, then continue.",
        "The cable goes up into the top row, along it, and comes back down "
        "in the fourth column.",
    ]
    help_keys = [("WASD", "select"), ("E", "turn")]

    def reset(self):
        self.rotations = [[rotation for _, rotation in row] for row in GRID]
        self.row, self.col = SOURCE_ROW, 0

    def handle_key(self, key):
        if key in MOVES:
            d_row, d_col = MOVES[key]
            self.row = (self.row + d_row) % ROWS
            self.col = (self.col + d_col) % COLS
        elif key in PRESS_KEYS:
            self.rotations[self.row][self.col] += 1
            if motor_powered(self.rotations):
                return SOLVED
        return None

    def on_solved(self):
        self.state.flags.add("exit_hall_open")
        self.state.give("signal_log")

    def success_lines(self):
        return [
            ("SHUTTER MOTOR: POWER OK", "good"),
            ("", "default"),
            ("Far away, the exit hall shutter in the concourse rattles open.",
             "default"),
            ("The signal console prints a long strip of paper: the SIGNAL "
             "LOG. You take it (press I to read it).", "bright"),
        ]

    # ----- drawing -----------------------------------------------------
    def draw(self, canvas, top, left, height, width, frame):
        grid_left, grid_top = 10, top + 2
        canvas.box(top + 1, 4, 16, 52, "machine", "double", "WIRING PANEL",
                   "machine_slot", fill_style="machine")
        powered = powered_tiles(self.rotations)
        for r in range(ROWS):
            for c in range(COLS):
                sides = connections(GRID[r][c][0], self.rotations[r][c])
                self.draw_tile(canvas, grid_top + r * 3, grid_left + c * 7,
                               sides, (r, c) in powered,
                               (r, c) == (self.row, self.col), (r + c) % 2)
        # Socket and motor
        canvas.put(grid_top + SOURCE_ROW * 3 + 1, 6, "PWR", "warn")
        canvas.put(grid_top + TARGET_ROW * 3 + 1, grid_left + COLS * 7,
                   "MOT", "good" if motor_powered(self.rotations) else "bad")

        canvas.box(top + 1, 58, 16, 19, "frame", "single", "HOW",
                   fill_style="default")
        for index, text in enumerate(["Connect PWR", "to MOT.", "",
                                      "E turns the", "selected tile", "clockwise.",
                                      "", "Yellow = power"]):
            canvas.put(top + 3 + index, 60, text,
                       "warn" if "Yellow" in text else "default")

    def draw_tile(self, canvas, row, col, sides, powered, selected, shade):
        """A tile is 7 x 3 characters; neighbouring cables join up."""
        style_name = "cable_on" if powered else "cable_off"
        if selected:
            style_name = "cable_sel_on" if powered else "cable_sel"
        back = "btn_sel" if selected else ("tile_a" if shade else "tile_b")
        canvas.fill(row, col, 3, 7, " ", back)
        if N in sides:
            canvas.set_cell(row, col + 3, "│", style_name)
        if S in sides:
            canvas.set_cell(row + 2, col + 3, "│", style_name)
        if W in sides:
            canvas.put(row + 1, col, "───", style_name)
        if E in sides:
            canvas.put(row + 1, col + 4, "───", style_name)
        canvas.set_cell(row + 1, col + 3,
                        CENTRE.get(frozenset(sides), "┼"), style_name)
