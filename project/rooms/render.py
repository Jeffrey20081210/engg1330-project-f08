"""Draw a room: map tiles, objects, task markers and the player sprite."""

import config
from engine.sprite import draw_player
from rooms.room import condition_met
from rooms.tiles import render_tile

TOP = config.MAP_TOP


def light_is_on(frame, seed):
    """A deterministic flicker pattern for a failing fluorescent light."""
    beat = (frame + seed * 7) % 40
    return beat not in (3, 5, 6, 21, 22, 23, 24)


def draw_object(canvas, obj, state, frame):
    if not condition_met(obj, state):
        return
    blink = obj.get("blink")
    if blink == "rare" and frame % 30 >= 4:      # a faint, rare glint
        return
    if blink is True and frame % 10 >= 6:
        return
    palette = obj.get("palette")
    swap = obj.get("flag_palette")
    if swap and swap["flag"] in state.flags:
        palette = swap["palette"]
    style_name = obj.get("style", "default")
    if obj.get("flicker") and not light_is_on(frame, obj["pos"][0]):
        style_name, palette = "light_off", None
    col, row = obj["pos"]
    canvas.draw_art(TOP + row, col, obj["art"], style_name, obj.get("mask"),
                    palette)


def draw_room(canvas, room, state, frame, show_player=True):
    # 1. Tiles
    for row, line in enumerate(room.map):
        for col, char in enumerate(line):
            glyph, style_name = render_tile(char, col, row, room, state)
            canvas.set_cell(TOP + row, col, glyph, style_name)

    # 2. Objects behind the player, the player, then objects in front.
    #    An object is "in front" when its bottom row is below the feet row.
    def bottom(obj):
        return obj["pos"][1] + len(obj["art"]) - 1

    objects = sorted(room.objects, key=bottom)
    behind = [obj for obj in objects if bottom(obj) <= state.y]
    in_front = [obj for obj in objects if bottom(obj) > state.y]
    for obj in behind:
        draw_object(canvas, obj, state, frame)
    if show_player:
        draw_player(canvas, TOP, state.x, state.y, state.facing, state.steps)
    for obj in in_front:
        draw_object(canvas, obj, state, frame)

    # 3. Blinking "!" above unfinished tasks, like task markers in Among Us.
    for spot in room.spots:
        marker = spot.get("marker")
        if not marker or not condition_met(spot, state):
            continue
        if spot.get("puzzle") in state.solved:
            continue
        if frame % 8 < 5:
            canvas.set_cell(TOP + marker[1], marker[0], "!", "task_marker")
