"""The Last Train from Central - a turn-based ASCII puzzle adventure.

Run in the course container with:  python main.py
"""

import curses
import locale
import os
import sys

from engine.game import Game, run
from engine.terminal import Terminal
from scenes.title import TitleScene


def play(screen):
    game = Game()
    game.reset_to(TitleScene(game))
    run(game, Terminal(screen))


def main():
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        print("Run this game in an interactive terminal (without -T).")
        return
    locale.setlocale(locale.LC_ALL, "")   # needed for box-drawing characters
    # COLUMNS/LINES are layout defaults from the container, not the real
    # window size. Let curses read the real size so resizing works.
    os.environ.pop("COLUMNS", None)
    os.environ.pop("LINES", None)
    curses.use_env(False)
    try:
        curses.wrapper(play)
    except KeyboardInterrupt:
        pass
    print("Thanks for playing The Last Train from Central!")


if __name__ == "__main__":
    main()
