"""Intro animation: the last train leaves, the lights go out, the story.

The animation runs on ticks, but it is only a cut-scene: no game state
changes until the player presses a key to start.
"""

import config
from engine.scene import Scene
from engine.ui import draw_popup, draw_status_bar
from rooms import get_room
from rooms.render import draw_room
from scenes.explore import ExploreScene
from story.art import draw_train
from story.text import INTRO_LINES, START_MESSAGES

TRAIN_ROW = config.MAP_TOP + 14      # the track rows of the platform map
DEPART_AT = 12                       # ticks before the train starts moving
LIGHTS_OUT_AT = 42
TEXT_AT = 56
TICKS_PER_LINE = 9
END = TEXT_AT + TICKS_PER_LINE * len(INTRO_LINES)


class IntroScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.start_frame = game.frame
        self.skipped = False

    def ticks(self, frame):
        return END if self.skipped else frame - self.start_frame

    def handle_key(self, key):
        if self.ticks(self.game.frame) < END:
            self.skipped = True          # first key: jump to the full text
            return
        self.start_game()

    def start_game(self):
        scene = ExploreScene(self.game)
        scene.enter_room("platform")
        for text, style_name in START_MESSAGES:
            self.state.say(text, style_name)
        self.game.reset_to(scene)

    def draw(self, canvas, frame):
        t = self.ticks(frame)
        room = get_room("platform")
        draw_status_bar(canvas, self.state, room.name)
        draw_room(canvas, room, self.state, frame, show_player=False)

        # The train pulls away, faster and faster.
        if t < LIGHTS_OUT_AT:
            moving = max(0, t - DEPART_AT)
            draw_train(canvas, TRAIN_ROW, 2 + moving * moving // 4)
        # "z z z" above the bench where the player sleeps.
        if t < TEXT_AT:
            canvas.put(config.MAP_TOP + 6, 44, "z Z z"[: 1 + (frame // 4) % 5],
                       "info")
        # Lights go out row by row, from the top.
        if t >= LIGHTS_OUT_AT:
            dark_rows = min(config.MAP_HEIGHT, (t - LIGHTS_OUT_AT) * 2)
            canvas.recolour(config.MAP_TOP, 0, dark_rows, canvas.width, "dark")

        if t >= TEXT_AT:
            shown = min(len(INTRO_LINES), (t - TEXT_AT) // TICKS_PER_LINE + 1)
            lines = []
            for index in range(shown):
                last = index == len(INTRO_LINES) - 1
                lines.append((INTRO_LINES[index], "warn" if last else "bright"))
                lines.append(("", "default"))
            footer = None
            if t >= END:
                footer = "Press any key to begin" if frame % 10 < 7 else " "
            draw_popup(canvas, "00:42", lines[:-1], 74, footer=footer)
        else:
            canvas.put(config.PROMPT_ROW + 2, 2, "Press any key to skip",
                       "dim")
