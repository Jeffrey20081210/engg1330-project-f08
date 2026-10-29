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
