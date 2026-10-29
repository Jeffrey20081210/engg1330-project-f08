"""The scene stack and the main loop.

The game is turn-based: the state only changes inside handle_key(), which is
called once per key press. Between key presses the loop wakes up every tick
only to redraw animations such as flickering lights.
"""

from engine.canvas import Canvas
from engine.state import GameState


class Game:
    def __init__(self):
        self.state = GameState()
        self.scenes = []
        self.running = True
        self.frame = 0

    # ----- scene stack -------------------------------------------------
    def push(self, scene):
        """Open a scene on top, e.g. the help screen or a puzzle."""
        self.scenes.append(scene)

    def pop(self):
        """Close the top scene and return to the one below."""
        if len(self.scenes) > 1:
            self.scenes.pop()

    def replace(self, scene):
        """Swap the top scene for another one."""
        if self.scenes:
            self.scenes.pop()
        self.scenes.append(scene)

    def reset_to(self, scene):
        """Throw away every scene and start again from this one."""
        self.scenes = [scene]

    @property
    def top(self):
        return self.scenes[-1]

    # ----- one turn ----------------------------------------------------
    def handle_key(self, key):
        if key == "quit_now":            # Ctrl+C quits at once
            self.running = False
            return
        self.top.handle_key(key)
        self.check_time()

    def check_time(self):
        """When the clock reaches 01:30 the run ends, whatever is open."""
        from scenes.ending import EndingScene   # avoid a circular import
        if self.state.out_of_time() and self.state.ending is None:
            self.state.ending = "trapped"
            self.reset_to(EndingScene(self, "trapped"))

    def new_game(self):
        """Fresh state, starting at the intro animation."""
        from scenes.intro import IntroScene
        self.state = GameState()
        self.reset_to(IntroScene(self))

    # ----- drawing -----------------------------------------------------
    def draw(self, canvas):
        """Draw the top scene and, under overlays, the scenes below it."""
        first = len(self.scenes) - 1
        while first > 0 and self.scenes[first].overlay:
            first -= 1
        canvas.clear()
        for scene in self.scenes[first:]:
            scene.draw(canvas, self.frame)


def run(game, terminal):
    """Main loop: draw, wait for one key (or one tick), react."""
    canvas = Canvas()
    while game.running:
        terminal.update_size()
        if not terminal.big_enough():
            # Pause: show the resize message and ignore everything but quit.
            terminal.show_resize_message()
            key = terminal.read_key()
            if key in ("q", "quit_now"):
                game.running = False
            continue
        game.draw(canvas)
        terminal.show(canvas)
        key = terminal.read_key()
        if key is None:
            game.frame += 1              # animation only, no turn passes
        elif key != "resize":
            game.handle_key(key)
