# AI Use

Generative AI used: Yes

## Entry

- **Member and date:** Lo Chit Hei, 2026-10-29
- **Tool and model/version:** Claude Code (Claude Opus 5.5)
- **Purpose:** Discussing and refining the game design (story, route structure, time rules, controls) (by asking for ideas from AI, i.e. brainstorming); dealing with some advanced parts of the code when writing the first working version of the game engine, the platform room, Puzzle 1 and the tests.
- **Relevant prompts and outputs used, or retained transcript location:** For the prompt, we told our initial thoughts (what we already had at that time) first, and told it which parts of the game design we haven't come up with an idea in, and then asked it to give multiple ideas for us to select. Then its output was some possible directions that we could choose to continue with, then we chose, and continued for other parts. After several rounds of conversation like this, we confirmed our whole game design. For the "dealing with some advanced parts of the code" part, it's just that we found that some functions and effects that we wanted to make couldn't be implemented using our current programming knowledge, so we prompted it to deal with those parts.
- **Files/materials affected:** `DESIGN.md`, `README.md`, parts of the code of the .py files in `project/` (main.py, config.py, engine/, scenes/, rooms/, puzzles/, story/, tests/).
- **What we kept, changed, or rejected, and How we checked it; tests and corrections:** We set the design decisions (TUI with real-time-feel controls that stay turn-based, branching routes, time rules, colours and sprite). The AI suggested 1 minute per step; this was changed to 4 seconds per step after further considering the room sizes.
  The Puzzle 1 clues were checked by a brute-force search and by pytest tests (exactly one answer, every clue needed). The whole game was run in the course container with pytest and in a real pseudo terminal (normal play, small terminal, resizing).

## Entry

- **Member and date:** Lo Chit Hei, 2026-10-30
- **Tool and model/version:** Claude Code (Claude Opus 5.5)
- **Purpose:** Designing Acts 2 and 3 with the group (route choice, the eight new puzzles, endings) (ask for AI's opinions and suggestions to improve decision) and implementing them with tests.
- **Relevant prompts and outputs used, or retained transcript location:** Our prompt was similar in form with the above previous one, we also prompted it to give some possible ideas (directions) of the acts 2 and 3 that we can go with, and we chose from those directions, finally we confirmed our acts 2 and 3. Also, to patch as many "vulnerabilities" as possible in the program, we asked AI to write some tests to check any possibly existing "bugs" in the program, and its output were just the test .py files in `tests/`.
- **Files/materials affected:** `DESIGN.md`, new files in `puzzles/` (lockers, breakers, wires, stations, morse, boxes, tunnel, signals), `rooms/` (control_room, ticket_office, storeroom, exit_hall, route_room), `scenes/platform_zero.py`, `story/documents.py`, `tests/test_route_puzzles.py`, changes to most engine and scene files.
- **What we kept, changed, or rejected, and How we checked it; tests and corrections:** We chose the structure and rules (locker choice, caught-twice alarm, two true endings, free moves inside tasks). Puzzle data was generated and checked by search programs: locker notes (only one arrangement with exactly one liar), crate level (17-move solution, many dead ends), tunnel (safe route of 44 moves), signal and station clues.
  The tests found a redundant clue in the staff logbook ("exactly one YELLOW"), which was removed. A screen check found that cameras could turn onto the player without warning, so a "watched next" preview was added.
  All screens were rendered and inspected; the game was run in the course container with pytest and in a pseudo-terminal.
