"""
HKU ENGG1330 (2026-27 Sem1) F08 Group Project - The Last Train from Central

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
    locale.setlocale(locale.LC_ALL, "")
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