"""Pop-up screens drawn on top of the current scene. None of them cost time."""

import config
from engine.scene import Scene
from engine.ui import draw_popup
from puzzles.gate_code import PIECE_ORDER, receipt_lines
from rooms import STATION_PLAN
from story.documents import document_lines
from story.text import CLUE_NAMES, FRAGMENT_NAMES, HELP_LINES, ITEM_NAMES

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
    """Items, clues and fragments collected so far, on three pages."""
    overlay = True
    PAGES = ["CLUES", "ITEMS", "FRAGMENTS"]

    def __init__(self, game):
        super().__init__(game)
        self.page = 0

    def handle_key(self, key):
        if key in CLOSE_KEYS or key == "i":
            self.game.pop()
        elif key in ("a", "left"):
            self.page = (self.page - 1) % len(self.PAGES)
        elif key in ("d", "right", "tab"):
            self.page = (self.page + 1) % len(self.PAGES)

    def page_lines(self):
        state = self.state
        lines = []
        if self.page == 0:
            pieces = [p for p in PIECE_ORDER if p in state.clues]
            if not pieces:
                lines.append(("Nothing yet. Look around and press E.", "dim"))
            for piece in pieces:
                lines.append((CLUE_NAMES[piece], "bright"))
                for text in receipt_lines(piece):
                    lines.append(("   " + text, "info"))
        elif self.page == 1:
            if not state.inventory:
                lines.append(("You carry nothing useful yet.", "dim"))
            for item in state.inventory:
                lines.append((ITEM_NAMES[item].capitalize(), "bright"))
                lines += document_lines(item)
        else:
            lines.append((f"{len(state.fragments)} of "
                          f"{config.TOTAL_FRAGMENTS} fragments found", "title"))
            for fragment in sorted(state.fragments):
                lines.append(("- " + FRAGMENT_NAMES[fragment], "fragment"))
            if len(state.fragments) < config.TOTAL_FRAGMENTS:
                lines.append(("Some dark corners hide more than dust.", "dim"))
        return lines

    def draw(self, canvas, frame):
        tabs = "   ".join(f"[{name}]" if index == self.page else name
                           for index, name in enumerate(self.PAGES))
        draw_popup(canvas, tabs, self.page_lines(), 70,
                   footer="A/D  page    I / Esc  close")


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

        def centre(col):
            return origin_col + col + self.BOX_WIDTH // 2

        # Connecting lines (drawn first, the room boxes go on top).
        left_c, mid_c, right_c = centre(2), centre(25), centre(48)
        bar = origin_row + 4
        canvas.put(bar, left_c, "─" * (right_c - left_c + 1), "dim")
        canvas.put(bar, left_c, "└", "dim")
        canvas.put(bar, mid_c, "┼", "dim")
        canvas.put(bar, right_c, "┘", "dim")
        canvas.put(origin_row + 5, mid_c, "│", "dim")
        canvas.put(origin_row + 7, origin_col + 45, "──", "dim")
        for row in (origin_row + 4, origin_row + 5):          # the tunnel
            canvas.put(row, right_c + 4, ":", "dim")
        for row in (origin_row + 9, origin_row + 10):
            canvas.put(row, mid_c, "│", "dim")
        # Rooms
        for room_id, (name, row, col) in STATION_PLAN.items():
            here = room_id == self.state.room
            known = room_id in self.state.visited
            label = name if known or here else "???"
            box_style = "warn" if here else ("bright" if known else "dim")
            canvas.box(origin_row + row, origin_col + col, 3, self.BOX_WIDTH,
                       box_style, "single", fill_style="panel")
            if here and frame % 10 < 5:
                label = "> " + label + " <"
            canvas.put_center(origin_row + row + 1, label,
                              box_style, origin_col + col, self.BOX_WIDTH)
        canvas.put(top + config.MAP_HEIGHT - 2, left + 3,
                   "Yellow: you are here    ???: not explored yet    "
                   ": tunnel", "dim")
