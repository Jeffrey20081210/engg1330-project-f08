"""A Room wraps the plain room data (nested dicts and lists) with helpers.

Room data keys:
    id, name    identifier and the name shown in the status bar
    map         18 strings of 80 characters (see rooms/tiles.py)
    objects     ASCII art drawn on top of the map; "solid" ones block walking
    spots       interaction zones: walking into a zone shows an [E] prompt
    exits       map character -> where the exit leads and what opens it
"""

import config
from rooms.tiles import EXIT_CHARS, WALKABLE


class Room:
    def __init__(self, data):
        self.data = data
        self.id = data["id"]
        self.name = data["name"]
        self.map = data["map"]
        self.objects = data.get("objects", [])
        self.spots = data.get("spots", [])
        self.exits = data.get("exits", {})
        self.solid = set()
        for obj in self.objects:
            if obj.get("solid"):
                self.solid |= art_cells(obj)

    def tile(self, col, row):
        """The map character at (col, row); outside the map counts as wall."""
        if 0 <= row < len(self.map) and 0 <= col < len(self.map[row]):
            return self.map[row][col]
        return "#"

    def walkable(self, col, row):
        return self.tile(col, row) in WALKABLE and (col, row) not in self.solid

    def exit_open(self, char, state):
        """An exit is open when its required flag (if any) is set."""
        needed = self.exits.get(char, {}).get("requires")
        return needed is None or needed in state.flags

    def spot_at(self, x, y, state):
        """The first visible spot whose zone contains the player's feet."""
        for spot in self.spots:
            if not condition_met(spot, state):
                continue
            left, top, right, bottom = spot["zone"]
            if left <= x <= right and top <= y <= bottom:
                return spot
        return None


def feet_cells(x, y):
    """The three cells under the player's feet (the sprite is 3 wide)."""
    return [(x - 1, y), (x, y), (x + 1, y)]


def art_cells(obj):
    """Cells an object blocks: its whole box when solid is "box", otherwise
    every cell where the art (or its mask) is not a space."""
    cells = set()
    col, row = obj["pos"]
    mask = obj.get("mask", [])
    for r, line in enumerate(obj["art"]):
        mask_line = mask[r] if r < len(mask) else ""
        for c, char in enumerate(line):
            key = mask_line[c] if c < len(mask_line) else " "
            if obj.get("solid") == "box" or char != " " or key != " ":
                cells.add((col + c, row + r))
    return cells


def condition_met(item, state):
    """Objects and spots may only appear while a flag/fragment is (not) set."""
    for flag in item.get("needs_flags", ()):
        if flag not in state.flags:
            return False
    for flag in item.get("hide_flags", ()):
        if flag in state.flags:
            return False
    fragment = item.get("hide_fragment")
    if fragment and fragment in state.fragments:
        return False
    return True


def check_room_data(data):
    """Return a list of problems with a room's data (used by the tests)."""
    problems = []
    if len(data["map"]) != config.MAP_HEIGHT:
        problems.append(f"{data['id']}: map has {len(data['map'])} rows")
    for index, line in enumerate(data["map"]):
        if len(line) != config.SCREEN_WIDTH:
            problems.append(f"{data['id']}: row {index} has {len(line)} columns")
    used_exits = {char for line in data["map"] for char in line} & EXIT_CHARS
    for char in used_exits:
        if char not in data.get("exits", {}):
            problems.append(f"{data['id']}: exit {char} has no data")
    for obj in data.get("objects", []):
        col, row = obj["pos"]
        for r, line in enumerate(obj["art"]):
            if col < 0 or col + len(line) > config.SCREEN_WIDTH:
                problems.append(f"{data['id']}: object at {obj['pos']} too wide")
            if row + r >= config.MAP_HEIGHT:
                problems.append(f"{data['id']}: object at {obj['pos']} too low")
        if "mask" in obj and [len(m) for m in obj["mask"]] != [
                len(a) for a in obj["art"]]:
            problems.append(f"{data['id']}: object at {obj['pos']} mask shape")
    return problems
