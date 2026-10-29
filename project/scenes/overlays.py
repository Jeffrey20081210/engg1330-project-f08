"""Pop-up screens drawn on top of the current scene. None of them cost time."""

import config
from engine.scene import Scene
from engine.ui import draw_popup
from puzzles.gate_code import PIECE_ORDER, receipt_lines
from rooms import STATION_PLAN
from story.text import CLUE_NAMES, FRAGMENT_NAMES, HELP_LINES

CLOSE_KEYS = ("esc", "e", "enter", "space", "q")


class ReadOverlay(Scene):
    """Shows a text, e.g. a poster or a receipt piece."""
    overlay = True

    def __init__(self, game, title, lines, width=62):
        super().__init__(game)
        self.title = title
        self.lines = lines          # list of (text, style name)
        self.width = width

    def handle_key(self, key):
        if key in CLOSE_KEYS:
            self.game.pop()

    def draw(self, canvas, frame):
        draw_popup(canvas, self.title, self.lines, self.width)


class HelpOverlay(Scene):
    overlay = True

    def handle_key(self, key):
        if key in CLOSE_KEYS or key == "?":
            self.game.pop()

    def draw(self, canvas, frame):
        draw_popup(canvas, "HOW TO PLAY", HELP_LINES, 72,
                   footer="? / Esc  close")


class ConfirmQuitOverlay(Scene):
    overlay = True

    def handle_key(self, key):
        if key == "y":
            self.game.running = False
        elif key in ("n", "esc", "q"):
            self.game.pop()

    def draw(self, canvas, frame):
        draw_popup(canvas, "QUIT", [
            ("Quit the game? Your progress will be lost.", "default"),
            ("", "default"),
            ("Y  quit        N  keep playing", "bright"),
        ], 50, footer=None)


class InventoryOverlay(Scene):
    """Items, clues and fragments collected so far."""
    overlay = True

    def handle_key(self, key):
        if key in CLOSE_KEYS or key == "i":
            self.game.pop()

    def draw(self, canvas, frame):
        state = self.state
        lines = [("CLUES", "title")]
        pieces = [p for p in PIECE_ORDER if p in state.clues]
        if not pieces:
            lines.append(("Nothing yet. Look around and press E.", "dim"))
        for piece in pieces:
            lines.append((CLUE_NAMES[piece], "bright"))
            for text in receipt_lines(piece):
                lines.append(("   " + text, "info"))
        lines.append(("", "default"))
        lines.append((f"FRAGMENTS  {len(state.fragments)}/"
                      f"{config.TOTAL_FRAGMENTS}", "title"))
        for fragment in sorted(state.fragments):
            lines.append((FRAGMENT_NAMES[fragment], "fragment"))
        if not state.fragments:
            lines.append(("None found. Some corners hide more than dust.",
                          "dim"))
        draw_popup(canvas, "ITEMS AND CLUES", lines, 66,
                   footer="I / Esc  close")


class MapOverlay(Scene):
    """A plan of the station. Unvisited rooms show as ???."""
    overlay = True
    BOX_WIDTH = 20

    def handle_key(self, key):
        if key in CLOSE_KEYS or key == "m":
            self.game.pop()

    def draw(self, canvas, frame):
        top, left = config.MAP_TOP, 4
        canvas.box(top, left, config.MAP_HEIGHT, 72, "panel_title", "double",
                   "STATION MAP", "panel_title", fill_style="panel")
        origin_row, origin_col = top + 1, left + 3
        # Connecting lines (drawn first, the room boxes go on top).
        centres = [origin_col + col + self.BOX_WIDTH // 2
                   for col in (2, 25, 48)]
        for bar_row in (3, 7):
            row = origin_row + bar_row
            canvas.put(row, centres[0], "─" * (centres[2] - centres[0] + 1),
                       "dim")
            canvas.put(row, centres[0], "┌", "dim")
            canvas.put(row, centres[1], "┼", "dim")
            canvas.put(row, centres[2], "┐", "dim")
        canvas.put(origin_row + 11, centres[1], "│", "dim")
        # Rooms
        for room_id, (name, row, col) in STATION_PLAN.items():
            here = room_id == self.state.room
            known = room_id in self.state.visited
            label = name if known or here else "???"
            box_style = "warn" if here else ("bright" if known else "dim")
            canvas.box(origin_row + row, origin_col + col, 3, self.BOX_WIDTH,
                       box_style, "round", fill_style="panel")
            if here and frame % 10 < 5:
                label = "> " + label + " <"
            canvas.put_center(origin_row + row + 1, label,
                              box_style, origin_col + col, self.BOX_WIDTH)
        canvas.put(top + config.MAP_HEIGHT - 2, left + 3,
                   "Yellow: you are here    ???: not explored yet", "dim")
