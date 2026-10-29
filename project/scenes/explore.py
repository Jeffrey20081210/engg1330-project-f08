"""Walking around a room: movement, exits and interacting with spots."""

import config
from engine.scene import Scene
from engine.ui import draw_key_bar, draw_messages, draw_prompt_row, draw_status_bar
from puzzles import make_puzzle
from puzzles.gate_code import PIECE_ORDER, receipt_lines
from rooms import enter_room, get_room
from rooms.render import draw_room
from rooms.room import feet_cells
from rooms.tiles import EXIT_CHARS
from scenes.overlays import (ConfirmQuitOverlay, HelpOverlay, InventoryOverlay,
                             MapOverlay, ReadOverlay)
from scenes.puzzle_scene import PuzzleScene
from story.text import FRAGMENT_NAMES, ITEM_NAMES

DIRECTIONS = {
    "w": (0, -1, "up"), "up": (0, -1, "up"),
    "s": (0, 1, "down"), "down": (0, 1, "down"),
    "a": (-1, 0, "left"), "left": (-1, 0, "left"),
    "d": (1, 0, "right"), "right": (1, 0, "right"),
}

KEYS = [("WASD", "move"), ("E", "interact"), ("M", "map"), ("I", "items"),
        ("?", "help"), ("Q", "quit")]


class ExploreScene(Scene):
    @property
    def room(self):
        return get_room(self.state.room)

    def enter_room(self, room_id, position=None, facing=None):
        enter_room(self.state, room_id, position, facing)

    # ----- turns -------------------------------------------------------
    def handle_key(self, key):
        if key in DIRECTIONS:
            self.move(*DIRECTIONS[key])
        elif key in ("e", "enter", "space"):
            self.interact()
        elif key == "m":
            self.game.push(MapOverlay(self.game))
        elif key == "i":
            self.game.push(InventoryOverlay(self.game))
        elif key == "?":
            self.game.push(HelpOverlay(self.game))
        elif key == "h":
            self.state.say("Hints are given inside tasks: press H there.",
                           "dim")
        elif key in ("q", "esc"):
            self.game.push(ConfirmQuitOverlay(self.game))

    def move(self, d_col, d_row, facing):
        state = self.state
        room = self.room
        state.facing = facing
        new_x = state.x + d_col * config.STEP_COLUMNS
        new_y = state.y + d_row
        cells = feet_cells(new_x, new_y)

        # Walking into an exit leaves the room (if it is open).
        for col, row in cells:
            char = room.tile(col, row)
            if char in EXIT_CHARS:
                self.use_exit(char)
                return

        if all(room.walkable(col, row, state) for col, row in cells):
            state.x, state.y = new_x, new_y
            state.steps += 1
            state.spend(config.STEP_SECONDS)
        # Bumping into a wall only turns the player; no time passes.

    def use_exit(self, char):
        state = self.state
        room = self.room
        info = room.exits[char]
        if not room.exit_open(char, state):
            text = info.get("locked", "It will not open.")
            if text:
                state.say(text, "warn")
            return
        state.steps += 1
        state.spend(config.STEP_SECONDS)
        if info.get("ending"):                  # walking out to the street
            from scenes.ending import EndingScene
            state.ending = info["ending"]
            self.game.reset_to(EndingScene(self.game, state.ending))
        elif info.get("scene") == "platform0":  # the secret door
            from scenes.platform_zero import PlatformZeroScene
            self.game.push(PlatformZeroScene(self.game))
        else:
            self.enter_room(info["to"], info.get("entry"), info.get("facing"))

    def interact(self):
        state = self.state
        spot = self.room.spot_at(state.x, state.y, state)
        if spot is None:
            state.say("There is nothing to use here. Walk up to something.",
                      "dim")
            return
        needed = spot.get("requires")
        if needed and needed not in state.flags:
            state.say(spot.get("locked_text", "You cannot use this yet."),
                      "warn")
            return
        kind = spot["kind"]
        if kind == "puzzle":
            if spot["puzzle"] in state.solved:
                state.say(spot.get("done_text",
                                   "You have already finished this task."),
                          "dim")
            else:
                puzzle = make_puzzle(spot["puzzle"], state)
                self.game.push(PuzzleScene(self.game, puzzle))
        elif kind == "read":
            self.read(spot)
        elif kind == "fragment":
            self.pick_fragment(spot)

    def read(self, spot):
        state = self.state
        lines = [(text, "default") for text in spot["text"]]
        clue = spot.get("clue")
        if clue:
            lines.append(("", "default"))
            lines += [(f" {text} ", "receipt") for text in receipt_lines(clue)]
            if clue not in state.clues:
                state.clues.add(clue)
                found = len([p for p in PIECE_ORDER if p in state.clues])
                state.say(f"You keep the receipt piece ({found}/"
                          f"{len(PIECE_ORDER)} found). Press I to see your "
                          "clues.", "good")
        item = spot.get("item")
        if item and not state.has(item):
            state.give(item)
            state.say(f"You take the {ITEM_NAMES[item]}. Press I to read it "
                      "again.", "good")
        self.game.push(ReadOverlay(self.game, spot["title"], lines))

    def pick_fragment(self, spot):
        state = self.state
        fragment = spot["fragment"]
        state.fragments.add(fragment)
        state.say(f"Fragment found ({len(state.fragments)}/"
                  f"{config.TOTAL_FRAGMENTS}): {FRAGMENT_NAMES[fragment]}",
                  "fragment")
        lines = [(text, "default") for text in spot["text"]]
        self.game.push(ReadOverlay(self.game, spot["title"], lines))

    # ----- drawing -----------------------------------------------------
    def draw(self, canvas, frame):
        state = self.state
        room = self.room
        draw_status_bar(canvas, state, room.name)
        draw_room(canvas, room, state, frame)
        spot = room.spot_at(state.x, state.y, state)
        draw_prompt_row(canvas, f"[E] {spot['prompt']}" if spot else None)
        draw_messages(canvas, state)
        draw_key_bar(canvas, KEYS)
