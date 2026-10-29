"""How each map character looks and whether the player can walk on it.

Room maps are lists of strings made of these characters:

    #  back wall          |  side wall          .  floor
    _  yellow tactile strip (walkable)          =  platform screen doors
    ~  track bed          -  rails              1-9  exits (see room "exits")
"""

WALKABLE = {".", "_"}
EXIT_CHARS = set("123456789")


def floor_style(col, row):
    """Floor tiles alternate in 4 x 2 blocks so the floor looks tiled."""
    return "floor_a" if (col // 4 + row // 2) % 2 == 0 else "floor_b"


def exit_look(exit_info, is_open, col, row):
    """Exits are drawn as shutters, doors or plain openings."""
    look = exit_info.get("look", "shutter")
    if is_open:
        if look == "opening":
            return " ", floor_style(col, row)
        return "░", "shutter_open"
    if look == "door":
        return "▒", "door_frame"
    return "║", "shutter_locked"


def render_tile(char, col, row, room, state):
    """Return (glyph, style name) for one map cell."""
    if char == "#":
        return ("│" if col % 16 == 8 else " "), "wall"
    if char == "|":
        return " ", "wall_trim"
    if char == ".":
        return " ", floor_style(col, row)
    if char == "_":
        return "░", "tactile"
    if char == "=":
        if col % 12 == 0:
            return "█", "door_frame"
        if col % 12 == 6:
            return "│", "door_frame"
        return ("╱" if col % 12 == 3 else " "), "screen_door"
    if char == "~":
        return ("┼" if col % 4 == 0 else " "), "track"
    if char == "-":
        return ("╪" if col % 4 == 0 else "═"), "rail"
    if char in EXIT_CHARS:
        info = room.exits.get(char, {})
        return exit_look(info, room.exit_open(char, state), col, row)
    return " ", "default"
