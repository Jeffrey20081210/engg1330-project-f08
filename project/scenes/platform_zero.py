"""The secret Platform 0: the 03:00 train arrives and the player chooses.

Like the intro this is a cut-scene: the animation only decorates. The
choice (board or walk away) decides which true ending the player gets.
"""

import config
from engine.scene import Scene
from engine.ui import draw_popup, draw_status_bar
from rooms import get_room
from rooms.render import draw_room
from story.art import draw_train

TRAIN_ROW = config.MAP_TOP + 14
ARRIVE_TICKS = 40          # the train slows down and stops
STOP_COL = 4
OLD_TRAIN = {"b": "old_train", "w": "old_window", "r": "old_stripe",
             "k": "train_wheel"}


class PlatformZeroScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.start_frame = game.frame
        self.skipped = False

    def ticks(self, frame):
        return ARRIVE_TICKS if self.skipped else frame - self.start_frame

    def handle_key(self, key):
        if self.ticks(self.game.frame) < ARRIVE_TICKS:
            self.skipped = True
            return
        if key == "b":
            self.finish("true_board")
        elif key == "l":
            self.finish("true_leave")
        elif key == "esc":
            self.game.pop()          # step back into the exit hall

    def finish(self, kind):
        from scenes.ending import EndingScene
        self.state.ending = kind
        self.game.reset_to(EndingScene(self.game, kind))

    def draw(self, canvas, frame):
        t = self.ticks(frame)
        draw_status_bar(canvas, self.state, "Platform 0")
        # Platform 0 looks like Platform 1, only older and lit in blue.
        draw_room(canvas, get_room("platform"), self.state, frame,
                  show_player=False)
        canvas.recolour(config.MAP_TOP, 0, 14, canvas.width, "platform0")
        canvas.put(config.MAP_TOP + 1, 30, "   P L A T F O R M   0   ",
                   "old_stripe")
        # The old train glides in from the left and stops.
        remaining = max(0, ARRIVE_TICKS - t)
        col = STOP_COL - remaining * remaining // 8
        draw_train(canvas, TRAIN_ROW, col, palette=OLD_TRAIN)
        if t >= ARRIVE_TICKS:
            draw_popup(canvas, "03:00", [
                ("The old train stops without a sound. Its doors open. Warm "
                 "light spills onto the platform.", "default"),
                ("", "default"),
                ("A conductor in a very old uniform smiles at you. \"Missed "
                 "the last train? We all did, once. Coming home?\"", "bright"),
                ("", "default"),
                ("B  board the 03:00 train        L  walk away", "warn"),
            ], 64, footer="Esc  step back")
