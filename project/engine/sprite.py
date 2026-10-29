"""The player's 3 x 3 coloured sprite.

The sprite's position (x, y) is the middle of its feet. Only the feet row is
used for collisions, so the head and body may overlap the wall behind the
player, which gives the room a little depth.
"""

BODIES = {
    "down": "/|\\",
    "up": "/#\\",      # back view: the '#' is a backpack
    "left": "<|\\",
    "right": "/|>",
}
LEGS = ("/ \\", " | ")   # two walking poses


def sprite_lines(facing, steps):
    return [" o ", BODIES.get(facing, BODIES["down"]), LEGS[steps % 2]]


def draw_player(canvas, top, x, y, facing, steps):
    """Draw the sprite with its feet at map (x, y); top is the map's screen row."""
    head, body, legs = sprite_lines(facing, steps)
    row = top + y
    canvas.put(row - 2, x, "o", "skin")
    for offset, char in enumerate(body):
        if char == " ":
            continue
        name = "backpack" if char == "#" else "shirt"
        canvas.set_cell(row - 1, x - 1 + offset, char, name)
    for offset, char in enumerate(legs):
        if char != " ":
            canvas.set_cell(row, x - 1 + offset, char, "pants")
