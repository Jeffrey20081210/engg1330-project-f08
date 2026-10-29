"""Ending screen: big title, story, statistics, restart or quit."""

import config
from engine.canvas import wrap
from engine.scene import Scene
from engine.ui import draw_key_bar
from story.art import big_text
from story.text import ENDINGS


class EndingScene(Scene):
    def __init__(self, game, kind):
        super().__init__(game)
        self.kind = kind

    def handle_key(self, key):
        if key == "r":
            self.game.new_game()
        elif key in ("q", "esc"):
            self.game.running = False

    def draw(self, canvas, frame):
        ending = ENDINGS[self.kind]
        title = big_text(ending["title"])
        for index, line in enumerate(title):
            canvas.put_center(1 + index, line, ending["style"])
        row = 2 + len(title)
        for paragraph in ending["lines"]:
            for line in wrap(paragraph, 70):
                canvas.put_center(row, line, "default")
                row += 1
            row += 1

        state = self.state
        stats = [
            f"Time   {state.clock_text()}",
            f"Tasks  {state.tasks_done()}/{config.TOTAL_TASKS}",
            f"Fragments  {len(state.fragments)}/{config.TOTAL_FRAGMENTS}",
            f"Steps  {state.steps}",
            f"Mistakes  {state.wrong_answers}",
        ]
        canvas.put_center(19, "     ".join(stats), "info")
        draw_key_bar(canvas, [("R", "play again"), ("Q", "quit")])
