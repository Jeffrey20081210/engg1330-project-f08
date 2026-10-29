"""Puzzle 8 (Sneak route): sneak through the maintenance tunnel.

Turn-based stealth. Every move (or wait) is one tick: cameras turn to the
next direction in their pattern and guards take one step on their patrol.
Red cells are being watched. The player is caught when they end a move on
a watched cell, or when a camera or guard turns onto them after the move.

Caught once: marched back to the start, -5 minutes. Caught twice: the
alarm goes off and the run ends (the Alarm ending).

A search over (position, tick) in the tests checks that a safe route
exists (44 moves; the shortest route ignoring the cameras is 28).
"""

from math import lcm

from puzzles.base import GAME_OVER, MOVES, SOLVED, WRONG, Puzzle

MAP = [
    "########################",
    "#S...#.........#.......#",
    "#....#..####...#..###..#",
    "#.......#..#...........#",
    "#....#..#..#....#......#",
    "###.##..#..######..#####",
    "#..........#...........#",
    "#....##....#..###....X.#",
    "#....##................#",
    "########################",
]
DIRS = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "W": (0, -1)}
ARROWS = {"N": "^", "E": ">", "S": "v", "W": "<"}
# Cameras sit on walls: (position, directions they face, one per tick).
CAMERAS = [((5, 4), "SWNS"), ((5, 16), "SSEE"), ((5, 15), "NNSN")]
CAMERA_RANGE = 4
# Guards walk back and forth along these cells.
GUARDS = [
    [(3, c) for c in range(12, 21)],
    [(8, c) for c in range(7, 17)],
]
GUARD_RANGE = 3
CAUGHT_PENALTY = 5 * 60

WALLS = {(r, c) for r, line in enumerate(MAP)
         for c, ch in enumerate(line) if ch == "#"}
FLOOR = {(r, c) for r, line in enumerate(MAP)
         for c, ch in enumerate(line) if ch != "#"}
START = next((r, c) for r, line in enumerate(MAP)
             for c, ch in enumerate(line) if ch == "S")
EXIT = next((r, c) for r, line in enumerate(MAP)
            for c, ch in enumerate(line) if ch == "X")
PERIOD = lcm(*[len(pattern) for _, pattern in CAMERAS],
             *[2 * (len(path) - 1) for path in GUARDS])


def line_clear(a, b):
    """True when no wall stands between cells a and b."""
    (r0, c0), (r1, c1) = a, b
    steps = max(abs(r1 - r0), abs(c1 - c0))
    for i in range(1, steps):
        cell = (round(r0 + (r1 - r0) * i / steps),
                round(c0 + (c1 - c0) * i / steps))
        if cell in WALLS:
            return False
    return True


def view(position, direction, reach, wide):
    """Cells seen from position. Cameras see a widening cone."""
    d_row, d_col = DIRS[direction]
    seen = set()
    for distance in range(1, reach + 1):
        half = (distance - 1) // 2 if wide else 0
        for side in range(-half, half + 1):
            cell = (position[0] + d_row * distance + d_col * side,
                    position[1] + d_col * distance + d_row * side)
            if cell in FLOOR and line_clear(position, cell):
                seen.add(cell)
    return seen


def guard_at(path, tick):
    """A guard's cell and facing direction at a tick (back and forth)."""
    period = 2 * (len(path) - 1)

    def index(t):
        t %= period
        return t if t < len(path) else period - t

    here, there = path[index(tick)], path[index(tick + 1)]
    step = (there[0] - here[0], there[1] - here[1])
    facing = next(name for name, d in DIRS.items() if d == step)
    return here, facing


def watched(tick):
    """Every cell seen by a camera or guard at this tick."""
    cells = set()
    for position, pattern in CAMERAS:
        cells |= view(position, pattern[tick % len(pattern)], CAMERA_RANGE,
                      True)
    for path in GUARDS:
        position, facing = guard_at(path, tick)
        cells |= {position} | view(position, facing, GUARD_RANGE, False)
    return cells


class TunnelPuzzle(Puzzle):
    id = "tunnel"
    title = "Maintenance tunnel"
    hints = [
        "Red cells are watched right now: you cannot step on them. Dots are "
        "watched after your move: do not stop on them.",
        "Waiting (Space) is free and also moves the world one tick. Watch a "
        "camera for four ticks to learn its pattern.",
        "Guards (G) walk back and forth and only look ahead. Follow behind a "
        "guard instead of walking towards it.",
    ]
    help_keys = [("WASD", "move"), ("Space", "wait")]
    penalty_seconds = CAUGHT_PENALTY
    ending_kind = "alarm"

    def __init__(self, state):
        self.times_caught = 0
        super().__init__(state)

    def reset(self):
        self.player = START
        self.tick = 0

    def handle_key(self, key):
        if key in MOVES:
            d_row, d_col = MOVES[key]
            target = (self.player[0] + d_row, self.player[1] + d_col)
            if target in WALLS:
                return None              # bumping a wall is not a turn
        elif key in ("space", "e"):
            target = self.player         # wait one tick
        else:
            return None
        # Caught walking into view, or when the world turns towards you.
        if target in watched(self.tick):
            return self.caught()
        self.player = target
        self.tick += 1
        if self.player in watched(self.tick):
            return self.caught()
        if self.player == EXIT:
            return SOLVED
        return None

    def caught(self):
        self.times_caught += 1
        return GAME_OVER if self.times_caught >= 2 else WRONG

    def wrong_message(self):
        return ("SPOTTED! A guard marches you back to the hatch. -5 min. "
                "If you are caught again, the alarm will sound!")

    def on_solved(self):
        from rooms import enter_room       # avoid a circular import
        self.state.flags.add("exit_hall_open")
        enter_room(self.state, "exit_hall", (11, 14), "up")

    def success_lines(self):
        return [
            ("You made it through unseen.", "good"),
            ("", "default"),
            ("A ladder at the end of the tunnel brings you up through a "
             "floor hatch... into the EXIT HALL.", "default"),
        ]

    # ----- drawing -----------------------------------------------------
    def draw(self, canvas, top, left, height, width, frame):
        grid_top, grid_left = top + 2, 4
        canvas.box(top + 1, 2, 12, 76, "frame", "double",
                   "MAINTENANCE TUNNEL", fill_style="default")
        seen = watched(self.tick)
        soon = watched(self.tick + 1)       # do not END a move on these
        cameras = {pos: pattern[self.tick % len(pattern)]
                   for pos, pattern in CAMERAS}
        guards = {}
        for path in GUARDS:
            position, facing = guard_at(path, self.tick)
            guards[position] = facing
        for r, line in enumerate(MAP):
            for c in range(len(line)):
                cell = (r, c)
                row, col = grid_top + r, grid_left + c * 3
                if cell in cameras:
                    canvas.put(row, col, f"[{ARROWS[cameras[cell]]}]",
                               "camera")
                elif cell in WALLS:
                    canvas.put(row, col, "███", "shelf")
                elif cell in guards:
                    canvas.put(row, col, f"G{ARROWS[guards[cell]]} ", "guard")
                elif cell == self.player:
                    canvas.put(row, col, " o ", "player_cell")
                elif cell == EXIT:
                    canvas.put(row, col, "|=|", "hatch")
                elif cell in seen:
                    canvas.put(row, col, "░░░", "watched")
                elif cell in soon:
                    floor = "floor_a" if (r + c) % 2 else "floor_b"
                    canvas.put(row, col, "   ", floor)
                    canvas.set_cell(row, col + 1, ".", "watch_next")
                else:
                    floor = "floor_a" if (r + c) % 2 else "floor_b"
                    canvas.put(row, col, "   ", floor)
        legend = [("[>] cam", "camera"), ("G> guard", "guard"),
                  ("░ seen now", "watched"), (". seen next", "watch_next"),
                  ("|=| exit", "hatch"),
                  (f"caught {self.times_caught}/2", "bad"
                   if self.times_caught else "dim")]
        col = 3
        for text, style_name in legend:
            canvas.put(top + 14, col, text, style_name)
            col += len(text) + 3
        canvas.put(top + 16, 3, "Each move/wait: cams turn, guards step. "
                   "Red = never step. Dot = never stop.", "dim")
