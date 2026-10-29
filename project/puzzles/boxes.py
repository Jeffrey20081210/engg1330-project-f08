"""Puzzle 7 (Sneak route): crates in the storeroom block the floor hatch.

Push the crates out of the way and stand on the hatch. Crates can only be
pushed (never pulled), one at a time, and not onto the hatch. A crate pushed
into a corner is stuck, so the player may need to restart (R), which costs
time like a wrong answer.

The level was checked with a search program: it can be solved in 17 moves,
and about half of the possible crate positions are dead ends. The tests
solve it again with the same kind of search.
"""

from puzzles.base import MOVES, SOLVED, WRONG, Puzzle

LEVEL = [
    "############",
    "#P  #   ##H#",
    "# B # ###  #",
    "#  #### #B #",
    "#   # B  B #",
    "#     B  B #",
    "############",
]
CELL_W, CELL_H = 4, 2


def parse(level=LEVEL):
    """Return walls, crates, player start and hatch as (row, col) cells."""
    walls, crates = set(), set()
    player = hatch = None
    for r, line in enumerate(level):
        for c, char in enumerate(line):
            if char == "#":
                walls.add((r, c))
            elif char == "B":
                crates.add((r, c))
            elif char == "P":
                player = (r, c)
            elif char == "H":
                hatch = (r, c)
    return walls, crates, player, hatch


WALLS, CRATES, START, HATCH = parse()


def try_move(player, crates, d_row, d_col):
    """Return the new (player, crates) after one move, or None if blocked."""
    target = (player[0] + d_row, player[1] + d_col)
    if target in WALLS:
        return None
    if target in crates:
        beyond = (target[0] + d_row, target[1] + d_col)
        if beyond in WALLS or beyond in crates or beyond == HATCH:
            return None
        crates = (crates - {target}) | {beyond}
    return target, crates


class BoxesPuzzle(Puzzle):
    id = "boxes"
    title = "Storeroom crates"
    hints = [
        "Crates can only be pushed, never pulled. A crate pushed against a "
        "wall is often stuck for good: press R to start again (-3 min).",
        "The crate just below where you start can be pushed straight down, "
        "out of your way.",
        "Walk along the bottom row and push its crates to the right.",
        "In the right corner: push the middle crate right, then the crate "
        "above it up, and walk up the far right side.",
    ]
    help_keys = [("WASD", "push"), ("R", "restart -3 min")]

    def reset(self):
        self.player = START
        self.crates = set(CRATES)
        self.moves = 0

    def handle_key(self, key):
        if key in MOVES:
            result = try_move(self.player, self.crates, *MOVES[key])
            if result:
                self.player, self.crates = result
                self.moves += 1
                if self.player == HATCH:
                    return SOLVED
        elif key == "r" and self.moves > 0:
            return WRONG          # restarting costs time like a mistake
        return None

    def wrong_message(self):
        return "You drag every crate back to where it was. -3 min."

    def on_solved(self):
        self.state.flags.add("hatch_clear")
        self.state.give("tunnel_map")

    def success_lines(self):
        return [
            ("The hatch is clear!", "good"),
            ("", "default"),
            ("You lift the heavy lid. A ladder leads down into a dark "
             "maintenance tunnel.", "default"),
            ("Under the last crate lies an old TUNNEL MAP with a painted "
             "note about the exit release. You keep it (press I).", "bright"),
        ]

    # ----- drawing -----------------------------------------------------
    def draw(self, canvas, top, left, height, width, frame):
        grid_top, grid_left = top + 2, 4
        canvas.box(top + 1, 2, 16, 52, "frame", "double", "STOREROOM",
                   fill_style="default")
        for r, line in enumerate(LEVEL):
            for c in range(len(line)):
                self.draw_cell(canvas, grid_top + r * CELL_H,
                               grid_left + c * CELL_W, (r, c))
        canvas.box(top + 1, 55, 16, 24, "frame", "single", "GOAL",
                   fill_style="default")
        lines = [("Reach the hatch", "bright"), ("", "default"),
                 ("╔══╗ crate", "crate_text"), ("┌──┐ hatch", "good"),
                 ("", "default"), ("Push, never pull.", "default"),
                 ("One crate at a time.", "default"), ("", "default"),
                 (f"Moves: {self.moves}", "info")]
        for index, (text, style_name) in enumerate(lines):
            canvas.put(top + 3 + index, 57, text, style_name)

    def draw_cell(self, canvas, row, col, cell):
        if cell in WALLS:
            canvas.put(row, col, "████", "shelf")
            canvas.put(row + 1, col, "████", "shelf")
            return
        floor = "floor_a" if (cell[0] + cell[1]) % 2 else "floor_b"
        canvas.fill(row, col, CELL_H, CELL_W, " ", floor)
        if cell == HATCH:
            canvas.put(row, col, "┌──┐", "hatch")
            canvas.put(row + 1, col, "└──┘", "hatch")
        if cell in self.crates:
            canvas.put(row, col, "╔══╗", "crate")
            canvas.put(row + 1, col, "╚══╝", "crate")
        if cell == self.player:
            canvas.put(row, col + 1, "o", "skin")
            canvas.put(row + 1, col, "/|\\", "shirt")
