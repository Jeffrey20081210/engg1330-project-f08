# AI Use

Generative AI used: Yes

## Entry

- Member and date: Lo Chit Hei, 2026-10-29
- Tool and model/version: Claude Code (Claude Opus 5.5)
- Purpose: Discussing and refining the game design (story, route structure,
  time rules, controls); writing the first working version of the game
  engine, the platform room, Puzzle 1 and the tests.
- Substantial parts affected (files/materials): `DESIGN.md`, all files in
  `project/` (main.py, config.py, engine/, scenes/, rooms/, puzzles/,
  story/, tests/), README.md.
- What was kept, changed, or rejected, and how results were checked (tests or
  corrections): The group set the design decisions (TUI with real-time-feel
  controls that stay turn-based, branching routes, time rules, colours and
  sprite). The AI proposed 1 minute per step; this was changed to 4 seconds
  per step after checking the room sizes. The Puzzle 1 clues were checked
  by a brute-force search and by pytest tests (exactly one answer, every
  clue needed). The whole game was run in the course container with
  pytest and in a real pseudo-terminal (normal play, small terminal,
  resizing).

## Entry

- Member and date: Lo Chit Hei, 2026-10-30
- Tool and model/version: Claude Code (Claude Opus 5.5)
- Purpose: Designing Acts 2 and 3 with the group (route choice, the eight
  new puzzles, endings) and implementing them with tests.
- Substantial parts affected (files/materials): `DESIGN.md`; new files
  `puzzles/` (lockers, breakers, wires, stations, morse, boxes, tunnel,
  signals), `rooms/` (control_room, ticket_office, storeroom, exit_hall,
  route_room), `scenes/platform_zero.py`, `story/documents.py`,
  `tests/test_route_puzzles.py`; changes to most engine and scene files.
- What was kept, changed, or rejected, and how results were checked (tests or
  corrections): The group chose the structure and rules (locker choice,
  caught-twice alarm, two true endings, free moves inside tasks). Puzzle
  data was generated or checked by search programs: locker notes (only one
  arrangement with exactly one liar), crate level (17-move solution, many
  dead ends), tunnel (safe route of 44 moves), signal and station clues.
  The tests found a redundant clue in the staff logbook ("exactly one
  YELLOW"), which was removed. A screen check found that cameras could turn
  onto the player without warning, so a "watched next" preview was added.
  All screens were rendered and inspected; the game was run in the course
  container with pytest and in a pseudo-terminal.
