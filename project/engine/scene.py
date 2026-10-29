"""Base class for every screen of the game (title, room, puzzle, ending ...)."""


class Scene:
    # An overlay (help, map, pop-up text) is drawn on top of the scene below
    # it instead of replacing the whole screen.
    overlay = False

    def __init__(self, game):
        self.game = game

    @property
    def state(self):
        return self.game.state

    def handle_key(self, key):
        """React to one key press. This is the only place a turn happens."""

    def draw(self, canvas, frame):
        """Draw the scene. frame counts animation ticks (decoration only)."""
