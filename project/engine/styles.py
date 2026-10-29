"""Named colour styles.

Each style is (foreground, background, attributes). Colours are xterm-256
colour numbers; -1 means the terminal's default colour and None as a
background means "keep whatever background is already in that cell", which
lets sprites and text sit on top of coloured floors and walls.

This module does not import curses, so drawing code can be tested without a
terminal. engine/terminal.py turns these styles into real curses attributes.
"""

DEFAULT = -1

STYLES = {
    # General text
    "default": (252, None, ""),
    "bright": (231, None, "bold"),
    "dim": (244, None, ""),
    "title": (220, None, "bold"),
    "good": (77, None, "bold"),
    "bad": (203, None, "bold"),
    "warn": (220, None, "bold"),
    "info": (117, None, ""),
    "key": (16, 250, "bold"),          # a key cap such as [E]

    # Status bar and frames
    "status": (231, 88, "bold"),
    "status_dim": (217, 88, ""),
    "status_warn": (226, 160, "bold"),
    "frame": (67, None, ""),
    "frame_title": (231, None, "bold"),
    "panel": (252, 234, ""),
    "panel_title": (220, 234, "bold"),
    "prompt": (16, 220, "bold"),
    "separator": (238, None, ""),

    # Station tiles
    "wall": (240, 237, ""),
    "wall_trim": (245, 239, ""),
    "floor_a": (238, 235, ""),
    "floor_b": (238, 236, ""),
    "tactile": (178, 235, ""),
    "screen_door": (73, 23, ""),
    "door_frame": (250, 238, "bold"),
    "track": (241, 233, ""),
    "rail": (247, 233, "bold"),
    "shutter_locked": (203, 52, "bold"),
    "shutter_open": (77, 22, "bold"),
    "dark": (236, 232, ""),

    # Objects
    "light_on": (230, 237, "bold"),
    "light_off": (242, 237, ""),
    "poster_frame": (252, 237, ""),
    "poster_red": (231, 124, "bold"),
    "poster_blue": (231, 25, "bold"),
    "poster_green": (16, 71, "bold"),
    "poster_text": (16, 223, ""),
    "sign": (231, 24, "bold"),
    "machine": (250, 238, ""),
    "machine_screen": (46, 22, "bold"),
    "machine_slot": (220, 238, "bold"),
    "keypad": (231, 240, "bold"),
    "keypad_light": (196, 240, "bold"),
    "bench": (180, None, "bold"),
    "bin": (108, None, "bold"),
    "pillar": (245, 239, ""),
    "task_marker": (226, None, "bold"),
    "fragment": (219, None, "bold"),
    "train_body": (252, 240, ""),
    "train_window": (117, 24, ""),
    "train_stripe": (231, 160, "bold"),
    "train_wheel": (244, 233, "bold"),

    # Player sprite
    "skin": (223, None, "bold"),
    "shirt": (39, None, "bold"),
    "pants": (180, None, ""),
    "backpack": (208, None, "bold"),

    # Puzzle widgets
    "btn": (252, 238, "bold"),
    "btn_sel": (16, 220, "bold"),
    "lcd": (46, 22, "bold"),
    "lcd_bad": (231, 124, "bold"),
    "lcd_good": (16, 77, "bold"),
    "receipt": (16, 230, ""),
    "receipt_missing": (244, 236, ""),
    "receipt_text": (230, None, ""),

    # Route puzzles and rooms
    "locker": (252, 24, "bold"),
    "switch_on": (16, 77, "bold"),
    "switch_off": (231, 124, "bold"),
    "cable_on": (226, None, "bold"),
    "cable_off": (250, None, ""),
    "cable_sel": (16, None, "bold"),
    "cable_sel_on": (124, None, "bold"),
    "watch_next": (203, None, "bold"),
    "tile_a": (244, 236, ""),
    "tile_b": (244, 237, ""),
    "track0": (77, 22, "bold"),
    "safe": (250, 59, "bold"),
    "crate": (223, 94, "bold"),
    "crate_text": (223, None, "bold"),
    "shelf": (240, 236, ""),
    "hatch": (16, 71, "bold"),
    "camera": (231, 160, "bold"),
    "guard": (231, 25, "bold"),
    "player_cell": (231, 39, "bold"),
    "watched": (203, 52, ""),
    "signal": (244, 233, ""),
    "signal_frame": (250, None, ""),
    "lamp_r": (196, None, "bold"),
    "lamp_y": (226, None, "bold"),
    "lamp_g": (46, None, "bold"),
    "lamp_off": (239, None, ""),
    "secret_door": (51, 17, "bold"),
    "platform0": (67, 17, ""),
    "old_train": (223, 94, ""),
    "old_window": (230, 136, "bold"),
    "old_stripe": (231, 88, "bold"),
}


def style(name):
    """Return the (fg, bg, attrs) tuple for a style name."""
    return STYLES.get(name, STYLES["default"])
