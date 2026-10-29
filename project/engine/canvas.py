"""An 80 x 24 grid of coloured characters that every scene draws into.

Scenes never talk to curses directly. They draw into a Canvas, and the
terminal copies the finished canvas to the screen once per frame. Because
every write goes through put(), nothing can ever be drawn outside the
80 x 24 game area, and tests can inspect the canvas as plain text.
"""

import config
from engine.styles import style

BOX = {
    "single": ("┌", "┐", "└", "┘", "─", "│"),
    "double": ("╔", "╗", "╚", "╝", "═", "║"),
    "round": ("╭", "╮", "╰", "╯", "─", "│"),
}


class Canvas:
    def __init__(self, width=config.SCREEN_WIDTH, height=config.SCREEN_HEIGHT):
        self.width = width
        self.height = height
        self.clear()

    def clear(self):
        """Fill the whole canvas with blank default cells."""
        # Each cell is [character, foreground, background, attributes].
        self.cells = [[[" ", -1, -1, ""] for _ in range(self.width)]
                      for _ in range(self.height)]

    def inside(self, row, col):
        return 0 <= row < self.height and 0 <= col < self.width

    def set_cell(self, row, col, char, style_name="default"):
        """Write one character. A style with background None keeps the old one."""
        if not self.inside(row, col):
            return
        fg, bg, attrs = style(style_name)
        cell = self.cells[row][col]
        cell[0] = char
        cell[1] = fg
        if bg is not None:
            cell[2] = bg
        cell[3] = attrs

    def put(self, row, col, text, style_name="default"):
        """Write text from (row, col), clipped at the canvas edges."""
        for offset, char in enumerate(text):
            self.set_cell(row, col + offset, char, style_name)

    def put_center(self, row, text, style_name="default", left=0, width=None):
        """Write text centred inside the columns left .. left + width."""
        if width is None:
            width = self.width - left
        col = left + max(0, (width - len(text)) // 2)
        self.put(row, col, text, style_name)

    def fill(self, row, col, height, width, char=" ", style_name="default"):
        for r in range(row, row + height):
            self.put(r, col, char * width, style_name)

    def recolour(self, row, col, height, width, style_name):
        """Change the colours of an area but keep its characters."""
        for r in range(row, row + height):
            for c in range(col, col + width):
                if self.inside(r, c):
                    self.set_cell(r, c, self.cells[r][c][0], style_name)

    def box(self, row, col, height, width, style_name="frame", kind="single",
            title=None, title_style="frame_title", fill_style=None):
        """Draw a frame. fill_style, if given, also clears the inside."""
        tl, tr, bl, br, horizontal, vertical = BOX[kind]
        if fill_style is not None:
            self.fill(row + 1, col + 1, height - 2, width - 2, " ", fill_style)
        self.put(row, col, tl + horizontal * (width - 2) + tr, style_name)
        for r in range(row + 1, row + height - 1):
            self.set_cell(r, col, vertical, style_name)
            self.set_cell(r, col + width - 1, vertical, style_name)
        self.put(row + height - 1, col, bl + horizontal * (width - 2) + br,
                 style_name)
        if title:
            self.put(row, col + 2, f" {title} ", title_style)

    def draw_art(self, row, col, lines, style_name="default", mask=None,
                 palette=None):
        """Draw multi-line ASCII art.

        mask, if given, has the same shape as lines; each mask character is
        looked up in palette to choose the style of that art character.
        Spaces are transparent unless the mask has a character there, so a
        mask can paint a solid background behind the art.
        """
        for r, line in enumerate(lines):
            mask_line = mask[r] if mask is not None and r < len(mask) else ""
            for c, char in enumerate(line):
                key = mask_line[c] if c < len(mask_line) else " "
                if char == " " and key == " ":
                    continue
                name = style_name
                if palette is not None:
                    name = palette.get(key, style_name)
                self.set_cell(row + r, col + c, char, name)

    def text_lines(self):
        """The canvas as plain strings (used by tests and debugging)."""
        return ["".join(cell[0] for cell in line) for line in self.cells]

    def char_at(self, row, col):
        return self.cells[row][col][0]


def wrap(text, width):
    """Split text into lines no longer than width, breaking at spaces."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split(" ")
        line = ""
        for word in words:
            while len(word) > width:      # a single very long word
                if line:
                    lines.append(line)
                    line = ""
                lines.append(word[:width])
                word = word[width:]
            if not line:
                line = word
            elif len(line) + 1 + len(word) <= width:
                line += " " + word
            else:
                lines.append(line)
                line = word
        lines.append(line)
    return lines
