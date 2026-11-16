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

```
Platform (P1 keypad)
  → Concourse (P2 shift lockers: the locker you open = your route)
      ├─ Tech:  Control room   P3 breakers → P4 wiring      → signal log
      ├─ Human: Ticket office  P5 stations → P6 Morse        → staff logbook
      └─ Sneak: Storeroom      P7 crates   → P8 tunnel (CCTV) → tunnel map
  → Exit hall (P9 signal release, uses the route's document)
  → Ending
```

Each run plays 5 puzzles (P1, P2, two route puzzles, P9); 9 are built in total.
Every puzzle's data is checked by tests (unique answer or solvable).
Moves inside a puzzle cost no time; only wrong answers, restarts and hints do.
Leaving a puzzle with Esc keeps its progress.

| Puzzle | Rules | Wrong / fail |
|---|---|---|
| P1 Gate keypad | 3-digit code from 5 logged failed attempts on 3 torn receipt pieces (answer 964; every entry needed) | wrong code −3 min |
| P2 Shift lockers | 4 lockers (keycard, office key, maintenance key, empty). 4 staff notes, **exactly one lies**. Choose the tool you want, then its locker. One access per shift | wrong locker −3 min |
| P3 Breakers | 3×3 Lights Out: a switch flips itself and its 4 neighbours; all must be ON within 10 switches | over the limit −3 min, reset |
| P4 Wiring | Rotate tiles to connect the socket to the shutter motor (needs P3) | none (hints only) |
| P5 Station safe | Safe code = two staff members' station numbers on the Island Line staff map, deduced from logbook clues (answer 1504; every clue needed) | wrong code −3 min |
| P6 Morse | Broadcast tape has no letter gaps; pick the one candidate word that matches (answer RETURN) | wrong word −3 min |
| P7 Crates | Sokoban-style storeroom: push crates to reach the hatch; about half of all pushes lead to dead ends | restart (R) −3 min |
| P8 Tunnel | Turn-based stealth: 3 rotating cameras, 2 patrolling guards; red = watched now (cannot step there), dot = watched after the move (cannot stop there); safe route 44 moves | caught once: −5 min, back to start; twice: **Alarm** ending |
| P9 Signal release | Set 4 signals (R/Y/G) using the clues in the route's document (answer G R Y G, unique for every route) | wrong pattern −3 min |

P2 notes (lockers numbered 1–4 from the left; "left of" = lower number):
Ming "Locker 3 is the empty one." · Ka-yan "My office key is left of the empty
locker." · Siu-wai "The keycard is left of the maintenance key." · Uncle Chan
"The empty locker is left of my maintenance key." → Ming lies:
1 office key, 2 empty, 3 keycard, 4 maintenance key.

Route results: Tech P4 and Human P6 open the exit-hall shutter in the
concourse; Sneak P8 ends inside the exit hall through a floor hatch.

## 5. Fragments and endings

| Fragment | Where |
|---|---|
| 1 | Platform: old paper ticket in the dark corner (rare glint) |
| 2 | Concourse: old newspaper clipping in a corner |
| 3 | One in each route room, so any route can collect all three |

| Ending | Condition |
|---|---|
| Normal escape | P9 solved, walk out to the street before 01:30 |
| True ending A: board the 03:00 train | 3 fragments + P9 solved: a hidden door to "Platform 0" opens; the old train arrives; choose to board |
| True ending B: walk away | Same, but choose not to board |
| Trapped | Clock reaches 01:30 |
| Alarm | Caught a second time in the tunnel (Sneak route) |

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
