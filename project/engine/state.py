"""Everything that describes one playthrough lives in a GameState."""

import config
from engine.canvas import wrap

MESSAGE_WIDTH = config.SCREEN_WIDTH - 2
MESSAGE_HISTORY = 30


class GameState:
    def __init__(self):
        self.time = config.START_TIME    # seconds after midnight
        self.room = "platform"
        self.x = 0                       # player's feet: centre column
        self.y = 0                       # player's feet: map row
        self.facing = "down"
        self.steps = 0
        self.route = None                # "tech" / "human" / "sneak"
        self.solved = set()              # ids of solved puzzles (tasks)
        self.flags = set()               # world changes, e.g. "gate_open"
        self.inventory = []              # item ids, in pick-up order
        self.clues = set()               # clue ids the player has found
        self.fragments = set()           # hidden fragments for the true ending
        self.visited = set()             # rooms the player has entered
        self.hints_used = {}             # puzzle id -> number of hints shown
        self.puzzles = {}                # puzzle id -> puzzle object, so a
                                         # puzzle keeps its progress after Esc
        self.wrong_answers = 0
        self.messages = []               # list of (text, style, message no.)
        self.message_count = 0
        self.ending = None

    # ----- clock -------------------------------------------------------
    def spend(self, seconds):
        """Move the clock forward. Never goes past the seal time."""
        self.time = min(self.time + seconds, config.SEAL_TIME)

    def time_left(self):
        return max(0, config.SEAL_TIME - self.time)

    def out_of_time(self):
        return self.time >= config.SEAL_TIME

    def clock_text(self):
        minutes = self.time // 60
        return f"{minutes // 60:02d}:{minutes % 60:02d}"

    def minutes_left(self):
        """Whole minutes left, rounded up so 00:01:30 left shows as 2."""
        return -(-self.time_left() // 60)

    # ----- messages ----------------------------------------------------
    def say(self, text, style_name="default"):
        """Add a message to the log, wrapped to the message area width.

        All lines of one message share a number, so the newest message can
        be highlighted even when it wraps onto two lines.
        """
        self.message_count += 1
        for line in wrap(text, MESSAGE_WIDTH):
            self.messages.append((line, style_name, self.message_count))
        del self.messages[:-MESSAGE_HISTORY]

    def recent_messages(self, count=config.MESSAGE_LINES):
        return self.messages[-count:]

    # ----- progress ----------------------------------------------------
    def tasks_done(self):
        return len(self.solved)

    def has(self, item):
        return item in self.inventory

    def give(self, item):
        if item not in self.inventory:
            self.inventory.append(item)
