"""The interface every puzzle (task) follows.

The puzzle scene (scenes/puzzle_scene.py) handles the parts that are the
same for every puzzle: the frame, hints, time costs and leaving with Esc.
A puzzle only has to implement its own rules and drawing.

Moves inside a puzzle cost no time. Only a wrong answer (or a restart),
which the puzzle reports by returning WRONG, and hints cost time.
"""

import config

SOLVED = "solved"
WRONG = "wrong"
GAME_OVER = "game_over"     # the run ends at once (e.g. the alarm ending)


class Puzzle:
    id = ""
    title = ""
    hints = []          # shown one at a time when the player presses H
    help_keys = []      # extra key reminders for the bottom bar
    penalty_seconds = config.WRONG_ANSWER_SECONDS
    ending_kind = None  # which ending GAME_OVER leads to

    def __init__(self, state):
        self.state = state
        self.reset()

    def reset(self):
        """Put the puzzle back to its starting position."""

    def handle_key(self, key):
        """Return SOLVED, WRONG, GAME_OVER or None (nothing decided yet)."""
        return None

    def after_wrong(self):
        """Called after a wrong answer. By default the puzzle resets."""
        self.reset()

    def wrong_message(self):
        minutes = self.penalty_seconds // 60
        return f"Wrong! -{minutes} min. The task resets."

    def draw(self, canvas, top, left, height, width, frame):
        """Draw inside the given area of the screen."""

    def on_solved(self):
        """Change the world when the puzzle is solved (flags, items)."""

    def success_lines(self):
        """Text shown in the TASK COMPLETE pop-up: list of (text, style)."""
        return [(f"{self.title}: done.", "good")]


# Shared key handling for puzzles with a cursor on a grid.
MOVES = {"w": (-1, 0), "up": (-1, 0), "s": (1, 0), "down": (1, 0),
         "a": (0, -1), "left": (0, -1), "d": (0, 1), "right": (0, 1)}
PRESS_KEYS = ("e", "space", "enter")
