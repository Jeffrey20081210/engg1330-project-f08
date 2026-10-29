# The Last Train from Central — Design Document (draft v1)

ENGG1330 Group Project, Subclass F Group 8. Environment `engg1330-project:2026-v03` (Python 3.13).

## 1. Concept

It is 00:42. The player wakes up on a bench at MTR Central station after the last
train has left. The station seals at **01:30**. The player explores the station,
completes "task spots" (mini-puzzles, Among Us style) and escapes. A careful
player also uncovers the secret **03:00 train**.

Target playthrough: 5–10 minutes. All text in English.

## 2. Controls and turn rule

- Keys act immediately (no Enter), read with `curses`.
- **One key press = one turn.** If the player does nothing, the world does not change.
- Animations are decoration only (intro, flickering lights, train arriving).

| Key | Action |
|---|---|
| W A S D / arrows | Move (map) or move cursor (puzzle) |
| E | Interact with a task spot / object |
| M | Station map |
| I | Inventory and clues |
| H | Hint inside a puzzle (costs time) |
| ? | Help screen (any time) |
| Esc | Leave puzzle / close overlay |
| Q | Quit (with confirmation) |

## 3. Time and failure

- Clock starts at 00:42, seal at 01:30 (48 in-game minutes).
- Each step on the map = **4 seconds** (changed from 1 minute: a room is ~38
  steps wide, so 1 minute per step would use up the whole clock in one room).
  One horizontal step moves 2 columns, one vertical step moves 1 row.
- Each wrong puzzle answer = 3 minutes and the puzzle resets.
- Each hint = 2 minutes (tunable).
- Time reaches 01:30 → **Trapped** ending. Opening overlays (map, help, inventory) costs no time.
- All numbers kept in one config file for balancing.

## 4. Structure: shared start → branch → shared finish

| Act | Area | Puzzles |
|---|---|---|
| 1 (shared) | Platform | P1 Ticket-machine receipt (find poster clues, build override code)<br>P2 Gate: three ways to open it → **chooses the route** |
| 2 (branch) | Tech: control room | P3 Breaker panel (Lights Out logic)<br>P4 Wire / pipe rotation |
| 2 (branch) | Human: ticket office | P5 MTR line deduction (code for the safe)<br>P6 Morse broadcast |
| 2 (branch) | Sneak: service tunnel | P7 Box pushing in the storeroom<br>P8 CCTV stealth (turn-based guard patrol) |
| 3 (shared) | Exit hall | P9 Final lock using clues from earlier acts |

Each run plays about 5 puzzles; 9 puzzles are built in total. "Who is lying"
(staff notes) is used as the P2 "Human" way, or as P1 if it fits better.

### P1 as built (v0.1): gate keypad

- The gate keypad needs a 3-digit staff code with three different digits (answer `964`).
- The ticket machine's maintenance log lists 5 earlier failed attempts, each with
  how many digits were correct (right place / wrong place). The log is torn into
  3 pieces: ticket machine (2 entries), rubbish bin (2), bench (1).
- Exactly one code fits all 5 entries, and **every entry is needed** (checked by tests),
  so the player must explore the whole platform.
- 4 hints, from "find all pieces" to "the code ends in 4".
- Fragment 1 (old 03:00 paper ticket) glints rarely in the dark left corner.

Open question: in this build P1 opens the way to the **concourse**, where the
three route doors are. P2 (choosing the route) will happen there.

## 5. Endings

| Ending | Condition |
|---|---|
| Normal escape | Solve P9 before 01:30 |
| True ending: The 03:00 Train | Also collected **3 hidden fragments** in the same run (hidden corners of shared and branch areas); player chooses whether to board |
| Trapped | Clock reaches 01:30 |
| Alarm | Caught during the Sneak route (CCTV / guard) |

After any ending: press R to restart or Q to quit.

## 6. Screen layout (80 × 24)

```
row 0        status bar: time | route | tasks done | fragments
rows 1–18    room view (rooms are separate screens joined by doors)
rows 19–23   message log (3 lines) + key hints
```

- Fully coloured: walls, floor, doors, task spots (highlighted), NPCs, status bar, warnings.
- Smaller than 80 × 24 → pause and show a resize message.
- Messages: 3 lines, the newest message is bright and older ones are dimmed.

### Player sprite

A coloured, human-shaped sprite instead of a single `@`. Proposal: a 3×3 sprite
whose collision box is its feet row.

```
 o      head (skin colour)
/|\     body (shirt colour)
/ \     legs (trouser colour)
```

It turns to face the direction of movement (e.g. `o/` arm raised when interacting).

## 7. Intro and title

- ASCII intro animation: train leaving the platform, lights going out (skippable with any key).
- Title in big letters with `pyfiglet`.
- Instruction screen before play, also reachable later with `?`.

## 8. Code structure

```
project/
  main.py              entry point
  config.py            tunable numbers (time costs, colours)
  engine/              canvas, curses terminal, colours, state, game loop
  scenes/              title, intro, explore, puzzle host, overlays, ending
  rooms/               room maps and data (nested dicts)
  puzzles/             one file per puzzle, shared Puzzle interface
  story/               intro, endings, text
  tests/               pytest: puzzle logic, time, endings, input validation
README.md  ai_use.md  acknowledgements
```

Puzzle logic is kept separate from drawing, so it can be tested with `pytest`
without a terminal. Version control with git.

## 9. Run

```
docker compose run --rm game python main.py
```
