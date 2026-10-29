"""The only module that talks to curses.

It copies a Canvas to the real screen, turns raw key codes into simple key
names ("up", "enter", "e", "7" ...) and pauses the game when the terminal is
smaller than 80 x 24.
"""

import curses
import os
import sys

import config

# Map raw curses keys to the key names used by the rest of the game.
SPECIAL_KEYS = {
    curses.KEY_UP: "up",
    curses.KEY_DOWN: "down",
    curses.KEY_LEFT: "left",
    curses.KEY_RIGHT: "right",
    curses.KEY_ENTER: "enter",
    curses.KEY_BACKSPACE: "backspace",
    curses.KEY_DC: "backspace",
}
CHAR_KEYS = {
    "\n": "enter",
    "\r": "enter",
    "\x1b": "esc",
    "\x7f": "backspace",
    "\x08": "backspace",
    " ": "space",
    "\x03": "quit_now",      # Ctrl+C
}

RESIZE_LINES = ("Resize to 80 x 24", "Press q to quit")


def normalise_key(key):
    """Return a key name, or None for keys the game does not use."""
    if isinstance(key, int):
        return SPECIAL_KEYS.get(key)
    if key in CHAR_KEYS:
        return CHAR_KEYS[key]
    if len(key) == 1 and key.isprintable():
        return key.lower()
    return None


def xterm_to_basic(colour):
    """Approximate an xterm-256 colour with one of the 8 basic colours."""
    if colour < 0:
        return -1
    if colour < 16:
        return colour % 8
    if colour >= 232:                       # greyscale ramp
        return curses.COLOR_WHITE if colour >= 244 else curses.COLOR_BLACK
    colour -= 16
    red, green, blue = colour // 36, (colour // 6) % 6, colour % 6
    bits = 0
    if red >= 3:
        bits |= 1
    if green >= 3:
        bits |= 2
    if blue >= 3:
        bits |= 4
    # curses basic colours: 1 red, 2 green, 4 blue, combined like RGB bits.
    return bits


class Terminal:
    def __init__(self, screen):
        self.screen = screen
        self.pairs = {}          # (fg, bg) -> curses colour pair number
        self.colours = 0
        self.size = screen.getmaxyx()
        curses.noecho()
        screen.keypad(True)
        screen.timeout(config.TICK_MS)
        try:
            curses.set_escdelay(25)  # make Esc respond quickly
        except (AttributeError, curses.error):
            pass
        try:
            curses.curs_set(0)
        except curses.error:
            pass  # some terminals cannot hide the cursor
        self._setup_colours()

    def _setup_colours(self):
        if not curses.has_colors():
            return
        try:
            curses.start_color()
            curses.use_default_colors()
            self.colours = curses.COLORS
        except curses.error:
            self.colours = 0

    def _attr(self, fg, bg, attrs):
        """Build a curses attribute, creating colour pairs when needed."""
        value = 0
        if "bold" in attrs:
            value |= curses.A_BOLD
        if self.colours >= 8:
            if self.colours < 256:
                fg, bg = xterm_to_basic(fg), xterm_to_basic(bg)
            key = (fg, bg)
            if key not in self.pairs:
                number = len(self.pairs) + 1
                if number < curses.COLOR_PAIRS:
                    try:
                        curses.init_pair(number, fg, bg)
                        self.pairs[key] = number
                    except curses.error:
                        self.pairs[key] = 0
                else:
                    self.pairs[key] = 0
            value |= curses.color_pair(self.pairs[key])
        elif "bold" not in attrs and bg not in (-1, None):
            value |= curses.A_REVERSE   # monochrome: show filled areas
        return value

    def update_size(self):
        """Follow the real terminal size (also when the window is resized)."""
        try:
            actual = os.get_terminal_size(sys.stdin.fileno())
            size = (max(1, actual.lines), max(1, actual.columns))
        except OSError:
            size = self.screen.getmaxyx()
        if size != self.screen.getmaxyx():
            try:
                curses.resizeterm(*size)
            except curses.error:
                pass
        self.size = size
        return size

    def big_enough(self):
        rows, cols = self.size
        return rows >= config.SCREEN_HEIGHT and cols >= config.SCREEN_WIDTH

    def show(self, canvas):
        """Copy the canvas to the screen, one run of equal colours at a time."""
        self.screen.erase()
        for row, line in enumerate(canvas.cells):
            col = 0
            while col < canvas.width:
                char, fg, bg, attrs = line[col]
                start = col
                text = char
                col += 1
                while col < canvas.width and line[col][1:] == [fg, bg, attrs]:
                    text += line[col][0]
                    col += 1
                try:
                    self.screen.addstr(row, start, text,
                                       self._attr(fg, bg, attrs))
                except curses.error:
                    pass  # writing the bottom-right cell raises; it is drawn
        self.screen.refresh()

    def show_resize_message(self):
        """A short message that fits even a very small terminal."""
        self.screen.erase()
        rows, cols = self.size
        for row, line in enumerate(RESIZE_LINES):
            if row < rows and cols > 1:
                try:
                    self.screen.addnstr(row, 0, line, cols - 1)
                except curses.error:
                    pass
        self.screen.refresh()

    def read_key(self):
        """Wait up to one tick for a key. Returns a key name or None."""
        try:
            key = self.screen.get_wch()
        except curses.error:
            return None          # no key during this tick
        if key == curses.KEY_RESIZE:
            return "resize"
        return normalise_key(key)
