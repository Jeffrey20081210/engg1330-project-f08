"""Title screen with a big pyfiglet title and a train passing below."""

from engine.scene import Scene
from engine.ui import draw_key_bar
from scenes.overlays import HelpOverlay
from story.art import CAR_WIDTH, big_text, draw_train

# Colours for the title rows, from top to bottom, like station lighting.
TITLE_COLOURS = ["title", "title", "warn", "warn", "bad", "bad", "bad"]


class TitleScene(Scene):
    def handle_key(self, key):
        if key in ("enter", "space", "e"):
            self.game.new_game()
        elif key == "?":
            self.game.push(HelpOverlay(self.game))
        elif key in ("q", "esc"):
            self.game.running = False

    def draw(self, canvas, frame):
        title = big_text("LAST TRAIN")
        for index, line in enumerate(title):
            colour = TITLE_COLOURS[min(index, len(TITLE_COLOURS) - 1)]
            canvas.put_center(1 + index, f"{line:<{len(max(title, key=len))}}",
                              colour)
        row = 2 + len(title)
        canvas.put_center(row, "f r o m   C E N T R A L", "bright")
        canvas.put_center(row + 2,
                          "The last train has left. The station seals at "
                          "01:30.", "default")
        canvas.put_center(row + 3, "Find a way out... or find the 03:00 train.",
                          "dim")

        # A train that keeps passing through the station (decoration only).
        track_row = 15
        canvas.fill(track_row, 0, 4, canvas.width, " ", "track")
        canvas.put(track_row + 1, 0, "═" * canvas.width, "rail")
        canvas.put(track_row + 2, 0, "═" * canvas.width, "rail")
        length = 2 * (CAR_WIDTH + 1)
        col = canvas.width - (frame * 2) % (canvas.width + length + 40)
        draw_train(canvas, track_row, col)

        if frame % 10 < 7:
            canvas.put_center(20, "Press ENTER to start", "warn")
        canvas.put_center(22, "ENGG1330 Group Project  |  Subclass F, Group 8",
                          "dim")
        draw_key_bar(canvas, [("Enter", "new game"), ("?", "how to play"),
                              ("Q", "quit")])
