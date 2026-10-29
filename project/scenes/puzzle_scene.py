"""Hosts one puzzle: frame, hints, time costs and leaving with Esc."""

import config
from engine.scene import Scene
from engine.ui import draw_key_bar, draw_messages, draw_prompt_row, draw_status_bar
from puzzles.base import GAME_OVER, SOLVED, WRONG
from scenes.overlays import HelpOverlay, ReadOverlay


class PuzzleScene(Scene):
    def __init__(self, game, puzzle):
        super().__init__(game)
        self.puzzle = puzzle

    def handle_key(self, key):
        state = self.state
        if key == "esc":
            state.say("You step away. You can come back at any time.", "dim")
            self.game.pop()
            return
        if key == "?":
            self.game.push(HelpOverlay(self.game))
            return
        if key == "h":
            self.give_hint()
            return
        result = self.puzzle.handle_key(key)
        if result == WRONG:
            state.spend(self.puzzle.penalty_seconds)
            state.wrong_answers += 1
            state.say(self.puzzle.wrong_message(), "bad")
            self.puzzle.after_wrong()
        elif result == SOLVED:
            self.solve()
        elif result == GAME_OVER:
            from scenes.ending import EndingScene   # avoid a circular import
            state.ending = self.puzzle.ending_kind
            self.game.reset_to(EndingScene(self.game, state.ending))

    def give_hint(self):
        state = self.state
        used = state.hints_used.get(self.puzzle.id, 0)
        hints = self.puzzle.hints
        if used >= len(hints):
            state.say("No more hints for this task.", "dim")
            return
        state.spend(config.HINT_SECONDS)
        state.hints_used[self.puzzle.id] = used + 1
        state.say(f"Hint {used + 1}/{len(hints)} "
                  f"(-{config.HINT_SECONDS // 60} min): {hints[used]}", "warn")

    def solve(self):
        state = self.state
        state.solved.add(self.puzzle.id)
        self.puzzle.on_solved()
        state.say(f"Task complete: {self.puzzle.title}.", "good")
        self.game.pop()
        self.game.push(ReadOverlay(self.game, "TASK COMPLETE",
                                   self.puzzle.success_lines(), 56))

    def draw(self, canvas, frame):
        draw_status_bar(canvas, self.state, self.puzzle.title)
        self.puzzle.draw(canvas, config.MAP_TOP, 0, config.MAP_HEIGHT,
                         canvas.width, frame)
        used = self.state.hints_used.get(self.puzzle.id, 0)
        draw_prompt_row(canvas, f"TASK: {self.puzzle.title}")
        canvas.put(config.PROMPT_ROW, canvas.width - 18,
                   f" hints {used}/{len(self.puzzle.hints)} ", "dim")
        draw_messages(canvas, self.state)
        draw_key_bar(canvas, self.puzzle.help_keys + [
            ("H", "hint -2 min"), ("Esc", "leave"), ("?", "help")])
