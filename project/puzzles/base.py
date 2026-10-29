"""The interface every puzzle (task) follows.

The puzzle scene (scenes/puzzle_scene.py) handles the parts that are the
same for every puzzle: the frame, hints, time costs and leaving with Esc.
A puzzle only has to implement its own rules and drawing.
"""

SOLVED = "solved"
WRONG = "wrong"


class Puzzle:
    id = ""
    title = ""
    hints = []          # shown one at a time when the player presses H
    help_keys = []      # extra key reminders for the bottom bar

    def __init__(self, state):
        self.state = state
        self.reset()

    def reset(self):
        """Put the puzzle back to its starting position."""

    def after_wrong(self):
        """Called after a wrong answer. By default the puzzle resets."""
        self.reset()

    def success_lines(self):
        """Text shown in the TASK COMPLETE pop-up: list of (text, style)."""
        return [(f"{self.title}: done.", "good")]

    def handle_key(self, key):
        """Return SOLVED, WRONG or None (nothing decided yet)."""
        return None

    def draw(self, canvas, top, left, height, width, frame):
        """Draw inside the given area of the screen."""

    def on_solved(self):
        """Change the world when the puzzle is solved (flags, items)."""
