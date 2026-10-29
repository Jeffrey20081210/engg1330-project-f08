"""Shared ASCII art: the MTR train and the big pyfiglet titles."""

import config

CAR_INNER = 48


def build_train_car():
    """One train car, 50 columns wide and 4 rows tall, with a colour mask."""
    art = [
        "┌" + "─" * CAR_INNER + "┐",
        "│" + " [__] [__] ║" * 4 + "│",
        "╞" + "═" * CAR_INNER + "╡",
        "└" + ("─(O)─(O)" + "─" * 16) * 2 + "┘",
    ]
    mask = []
    for row, line in enumerate(art):
        mask_line = ""
        for char in line:
            if row == 2:
                mask_line += "r"                       # red stripe
            elif row == 1 and char in "[_]":
                mask_line += "w"                       # windows
            elif row == 3 and char in "(O)":
                mask_line += "k"                       # wheels
            else:
                mask_line += "b"                       # silver body
        mask.append(mask_line)
    return art, mask


TRAIN_ART, TRAIN_MASK = build_train_car()
TRAIN_PALETTE = {"b": "train_body", "w": "train_window", "r": "train_stripe",
                 "k": "train_wheel"}
CAR_WIDTH = len(TRAIN_ART[0])


def draw_train(canvas, row, col, cars=2):
    """Draw a train whose left end is at col (it may be partly off screen)."""
    for car in range(cars):
        canvas.draw_art(row, col + car * (CAR_WIDTH + 1), TRAIN_ART,
                        mask=TRAIN_MASK, palette=TRAIN_PALETTE)


_figlet_cache = {}


def big_text(text, fonts=("standard", "small")):
    """Render text with pyfiglet, using the first font that fits 78 columns.

    Falls back to plain spaced-out letters if pyfiglet is not available.
    """
    if text in _figlet_cache:
        return _figlet_cache[text]
    lines = [" ".join(text)]
    try:
        import pyfiglet
        for font in fonts:
            rendered = pyfiglet.figlet_format(text, font=font, width=200)
            candidate = [line.rstrip() for line in rendered.split("\n")]
            while candidate and not candidate[-1].strip():
                candidate.pop()
            if max(len(line) for line in candidate) <= config.SCREEN_WIDTH - 2:
                lines = candidate
                break
    except ImportError:
        pass
    _figlet_cache[text] = lines
    return lines
