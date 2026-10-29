# The Last Train from Central

A single-player, turn-based ASCII puzzle adventure for the terminal.

It is 00:42 and the last train has left MTR Central station without you. The
station seals at 01:30. Explore the station, complete the tasks (mini-puzzles)
and escape in time. A careful explorer may also find out what the mysterious
03:00 train really is.

> Status: v0.2, complete playthrough. All three routes, all 9 puzzles and
> all 5 endings are playable. Balancing and playtesting are next.

## The story in three acts

1. **Platform** - find three torn receipt pieces and open the gate keypad.
2. **Concourse** - the shift lockers allow one access per shift; the tool
   you take chooses your route:
   - **Tech** (control room): breaker panel, then wiring panel
   - **Human** (ticket office): station-number safe, then Morse broadcast
   - **Sneak** (storeroom): crate pushing, then a stealth tunnel
3. **Exit hall** - set the emergency release signals using the document
   your route gave you, and walk out.

Endings: Escaped, Trapped (01:30), Alarm (caught twice in the tunnel), and
two true endings for players who find all three hidden fragments.

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
- Moves inside a task are free; leaving a task with Esc keeps its progress.
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

The tests (84) cover:

- puzzle logic: every puzzle has exactly one answer (or a route) and every
  clue is needed - checked by brute force or a breadth-first search, so a
  change to the puzzle data that breaks it fails the tests
- input: wrong answers, boundary cases (4th digit, 10th breaker flip,
  restart before moving) and unknown keys
- room data: 18 x 80 maps, reachable spots and entrances, real style names
- the clock boundary at 01:30, the trapped and alarm endings
- whole playthroughs of all three routes and the true ending, by sending
  keys to the game without a terminal

## Known limitations

- Timing is not balanced yet (a careful run uses about 30 of the 48
  in-game minutes); the numbers are in `config.py`.
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
- Several puzzles use well-known puzzle types, adapted to the story with our
  own data: lock-code clues (P1), knights-and-knaves style liar logic (P2),
  Lights Out (P3), pipe rotation (P4), crate pushing as in Sokoban (P7) and
  turn-based stealth (P8). Levels, clues and code are our own.
- Island Line station names and interchanges are public MTR information.
- Generative AI was used; see `ai_use.md`.
