# The Last Train from Central

A single-player, turn-based ASCII puzzle adventure for the terminal.

It is 00:42 and the last train has left MTR Central station without you. The
station seals at 01:30. Explore the station, complete the tasks (mini-puzzles)
and escape in time. A careful explorer may also find out what the mysterious
03:00 train really is.

> Status: early working version (v0.1). Platform, Act 1 puzzle, concourse
> and the "Trapped" ending are playable; the route puzzles and other endings
> are being built.

## Group

ENGG1330 Group Project 2026-27, Subclass F, Group 8

- Lo Chit Hei
- Nimmaraju Venkata Sai Bhargava Rama Anurag
- Faisal Alaeddin

Container version: `engg1330-project:2026-v03` (Python 3.13)

## How to run

From the folder that contains `compose.yaml`:

```
docker compose run --rm game python main.py
```

The game needs an interactive terminal of at least 80 x 24. If the window is
smaller, the game pauses and asks you to resize it.

## How to play

| Key | Action |
|---|---|
| W A S D / arrow keys | move (or move the cursor in a task) |
| E / Enter / Space | interact, press a button |
| M | station map |
| I | items and clues |
| H | hint inside a task (costs 2 minutes) |
| ? | help |
| Esc | leave a task / close a window |
| Q | quit (asks first) |

Rules:

- The game is turn-based: the clock only moves when you act.
- Each step costs 4 seconds, a wrong answer costs 3 minutes (and resets the
  task), a hint costs 2 minutes. Opening help, the map or items is free.
- Walk up to things and press E. Tasks are marked with a blinking `!`.
- Win: escape before 01:30. If the clock reaches 01:30 you are trapped.
- Restart: press R on the ending screen, or run the program again.

## Project structure

```
main.py        entry point (checks the terminal, starts curses)
config.py      all tunable numbers: screen layout, time costs
engine/        canvas (80x24 drawing grid), curses terminal, colours,
               game state, scene stack and main loop, player sprite
scenes/        title, intro animation, exploring, puzzle host,
               pop-ups (help, map, items, text), ending
rooms/         room data as nested dicts/lists, tile rules, drawing
puzzles/       one module per puzzle, all following puzzles/base.py
story/         story text and shared ASCII art (train, big titles)
tests/         pytest tests
```

Design notes:

- Scenes draw into a `Canvas`, never directly into curses. This keeps every
  character inside the 80 x 24 area and lets the tests check screens as text.
- Rooms are data: adding a room means adding a map, objects, spots and exits.
- Puzzle rules are separate from drawing, so the logic can be tested.
- Animations (train, flickering light, blinking markers) use a 100 ms tick
  but never change the game state.

## Tests

```
docker compose run --rm game python -m pytest
```

The tests cover the puzzle logic (exactly one answer, every clue needed,
keypad input including boundary and invalid keys), room data (size, reachable
spots and entrances), the clock (boundary at 01:30), and whole play
sequences without a terminal (wrong answer, hint, solving, running out of
time, restarting, quitting).

## Known limitations

- Act 2 routes, the exit hall, and the other endings are not built yet.
- Needs a terminal font with box-drawing characters (the default fonts of
  Windows Terminal and macOS Terminal work).

## Contributions

| Member | Contribution |
|---|---|
| Lo Chit Hei | Game design, programming |
| Nimmaraju Venkata Sai Bhargava Rama Anurag | Testing, feedback (to be completed) |
| Faisal Alaeddin | Testing, feedback (to be completed) |

## Acknowledgements and sources

- `pyfiglet` (supplied in the course container) for the big titles.
- Python standard library `curses` for the terminal interface.
- The puzzle type of Puzzle 1 (finding a lock code from "right place / wrong
  place" clues) is a well-known logic-puzzle format; our clues and setting
  are our own.
- Generative AI was used; see `ai_use.md`.
