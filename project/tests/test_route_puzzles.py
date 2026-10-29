"""Puzzles 2-9: every puzzle has exactly one answer or is solvable."""

from collections import deque
from itertools import product

import pytest

from engine.state import GameState
from puzzles import PUZZLES, boxes, breakers, lockers, morse, signals, stations
from puzzles import tunnel, wires
from puzzles.base import GAME_OVER, SOLVED, WRONG


def press(puzzle, keys):
    result = None
    for key in keys:
        result = puzzle.handle_key(key)
        if result:
            return result
    return result


# ----- P2 lockers ---------------------------------------------------------
def test_lockers_have_exactly_one_answer_and_every_note_matters():
    found = lockers.arrangements_with_one_liar()
    assert found == [{"office_key": 1, "empty": 2, "keycard": 3,
                      "maintenance_key": 4}]
    for index in range(len(lockers.NOTES)):
        fewer = lockers.NOTES[:index] + lockers.NOTES[index + 1:]
        # Without this note, "at most one lie" no longer pins the answer.
        count = 0
        for order in product(range(1, 5), repeat=4):
            if len(set(order)) < 4:
                continue
            where = dict(zip(lockers.ITEMS, order))
            if sum(not test(where) for _, _, test in fewer) <= 1:
                count += 1
        assert count > 1, f"note {index} is not needed"


def test_contents_match_the_logic():
    where = lockers.arrangements_with_one_liar()[0]
    assert {locker: item for item, locker in where.items()} == lockers.CONTENTS


@pytest.mark.parametrize("keys, route", [
    (["3", "e", "y"], "tech"),
    (["s", "1", "e", "y"], "human"),
    (["s", "s", "4", "e", "y"], "sneak"),
])
def test_each_tool_chooses_its_route(keys, route):
    state = GameState()
    puzzle = lockers.LockersPuzzle(state)
    assert press(puzzle, keys) == SOLVED
    puzzle.on_solved()
    assert state.route == route and f"route_{route}" in state.flags


def test_wrong_locker_and_cancel():
    puzzle = lockers.LockersPuzzle(GameState())
    assert press(puzzle, ["2", "e", "n"]) is None      # cancelled: no cost
    assert press(puzzle, ["e", "y"]) == WRONG           # locker 2 is empty
    puzzle.after_wrong()
    assert puzzle.flash == 2


# ----- P3 breakers --------------------------------------------------------
def test_breakers_shortest_solution_is_the_scramble():
    best = None
    cells = [(r, c) for r in range(3) for c in range(3)]
    for mask in range(1 << 9):
        grid = breakers.start_grid()
        chosen = [cells[i] for i in range(9) if mask >> i & 1]
        for row, col in chosen:
            breakers.flip(grid, row, col)
        if breakers.all_on(grid) and (best is None or len(chosen) < len(best)):
            best = chosen
    assert sorted(best) == sorted(breakers.SCRAMBLE)
    assert len(best) <= breakers.MAX_FLIPS - 4
    assert not breakers.all_on(breakers.start_grid())


def test_breakers_solve_and_overheat():
    puzzle = breakers.BreakersPuzzle(GameState())
    assert press(puzzle, ["w", "e", "s", "a", "e", "d", "d", "e", "s",
                          "e"]) == SOLVED
    puzzle = breakers.BreakersPuzzle(GameState())
    assert press(puzzle, ["e"] * breakers.MAX_FLIPS) == WRONG   # boundary


# ----- P4 wires -----------------------------------------------------------
WIRE_SOLUTION = {(1, 0): 1, (1, 1): 3, (0, 1): 1, (0, 2): 1, (0, 3): 2,
                 (1, 3): 0, (2, 3): 0, (2, 4): 1, (2, 5): 1}


def test_wires_start_unsolved_and_have_a_solution():
    start = [[rotation for _, rotation in row] for row in wires.GRID]
    assert not wires.motor_powered(start)
    solved = [row[:] for row in start]
    for (r, c), rotation in WIRE_SOLUTION.items():
        solved[r][c] = rotation
    assert wires.motor_powered(solved)


def wire_keys():
    """Keys that walk the cursor to each tile and turn it into place."""
    keys, row, col = [], wires.SOURCE_ROW, 0
    for (r, c), target in WIRE_SOLUTION.items():
        keys += ["s" if r > row else "w"] * abs(r - row)
        keys += ["d" if c > col else "a"] * abs(c - col)
        row, col = r, c
        start = wires.GRID[r][c][1]
        keys += ["e"] * ((target - start) % 4)
    return keys


def test_wires_solved_by_turning_tiles():
    puzzle = wires.WiresPuzzle(GameState())
    assert press(puzzle, wire_keys()) == SOLVED


# ----- P5 stations --------------------------------------------------------
def test_station_clues_have_one_answer_each_and_every_clue_matters():
    assert stations.safe_code() == "1504"
    for who, clues in stations.CLUES.items():
        assert len(stations.matching_stations(clues)) == 1, who
        for index in range(len(clues)):
            fewer = clues[:index] + clues[index + 1:]
            assert len(stations.matching_stations(fewer)) > 1, (who, index)


def test_station_facts_on_the_map():
    names = [name for name, _ in stations.STATIONS]
    assert len(names) == 17
    assert names[0] == "Kennedy Town" and names[-1] == "Chai Wan"
    assert names[stations.CENTRAL - 1] == "Central"
    assert names[stations.ADMIRALTY - 1] == "Admiralty"


def test_safe_keypad():
    puzzle = stations.StationsPuzzle(GameState())
    assert press(puzzle, ["1", "5", "0", "enter"]) is None   # too short
    assert press(puzzle, ["9", "enter"]) == WRONG
    puzzle.after_wrong()
    assert puzzle.entry == ""
    assert press(puzzle, ["1", "5", "0", "4", "4", "enter"]) == SOLVED


# ----- P6 Morse -----------------------------------------------------------
def test_only_the_answer_matches_the_tape():
    matches = [w for w in morse.CANDIDATES if morse.to_morse(w) == morse.TAPE]
    assert matches == [morse.ANSWER]
    same_length = [w for w in morse.CANDIDATES
                   if len(morse.to_morse(w)) == len(morse.TAPE)]
    assert len(same_length) >= 3     # counting symbols alone is not enough


def test_morse_choice():
    puzzle = morse.MorsePuzzle(GameState())
    assert press(puzzle, ["e"]) == WRONG                     # TUNNEL
    puzzle.after_wrong()
    assert press(puzzle, ["d", "e"]) == SOLVED               # RETURN


# ----- P7 crates ----------------------------------------------------------
def solve_boxes():
    start = (boxes.START, frozenset(boxes.CRATES))
    previous = {start: None}
    queue = deque([start])
    while queue:
        state = queue.popleft()
        player, crates = state
        if player == boxes.HATCH:
            keys = []
            while previous[state]:
                state, key = previous[state]
                keys.append(key)
            return keys[::-1]
        for key, (d_row, d_col) in (("w", (-1, 0)), ("s", (1, 0)),
                                    ("a", (0, -1)), ("d", (0, 1))):
            moved = boxes.try_move(player, set(crates), d_row, d_col)
            if moved:
                nxt = (moved[0], frozenset(moved[1]))
                if nxt not in previous:
                    previous[nxt] = (state, key)
                    queue.append(nxt)
    return None


def test_boxes_level_is_solvable_but_not_trivial():
    keys = solve_boxes()
    assert keys is not None and len(keys) == 17
    puzzle = boxes.BoxesPuzzle(GameState())
    assert press(puzzle, keys) == SOLVED


def test_boxes_restart_costs_only_after_moving():
    puzzle = boxes.BoxesPuzzle(GameState())
    assert puzzle.handle_key("r") is None          # nothing to restart
    puzzle.handle_key("d")
    assert puzzle.handle_key("r") == WRONG


def test_crate_cannot_be_pushed_into_a_wall_or_another_crate():
    assert boxes.try_move((1, 1), {(1, 2), (1, 3)}, 0, 1) is None
    assert boxes.try_move((1, 1), set(), -1, 0) is None


# ----- P8 tunnel ----------------------------------------------------------
def safe_tunnel_keys():
    """Shortest safe key sequence, searching over (cell, tick)."""
    period = tunnel.PERIOD
    views = [tunnel.watched(t) for t in range(period)]
    start = (tunnel.START, 0)
    previous = {start: None}
    queue = deque([start])
    moves = [("space", (0, 0)), ("w", (-1, 0)), ("s", (1, 0)),
             ("a", (0, -1)), ("d", (0, 1))]
    while queue:
        cell, tick = queue.popleft()
        if cell == tunnel.EXIT:
            keys, node = [], (cell, tick)
            while previous[node]:
                node, key = previous[node]
                keys.append(key)
            return keys[::-1]
        for key, (d_row, d_col) in moves:
            target = (cell[0] + d_row, cell[1] + d_col)
            nxt = (target, (tick + 1) % period)
            if (target in tunnel.WALLS or target in views[tick]
                    or target in views[nxt[1]] or nxt in previous):
                continue
            previous[nxt] = ((cell, tick), key)
            queue.append(nxt)
    return None


def test_tunnel_has_a_safe_route_that_needs_timing():
    keys = safe_tunnel_keys()
    assert keys is not None and len(keys) == 44
    assert tunnel.START not in tunnel.watched(0)
    state = GameState()
    puzzle = tunnel.TunnelPuzzle(state)
    assert press(puzzle, keys) == SOLVED


def careless_tunnel_keys():
    """The shortest route that ignores cameras and guards."""
    previous = {tunnel.START: None}
    queue = deque([tunnel.START])
    while queue:
        cell = queue.popleft()
        if cell == tunnel.EXIT:
            break
        for key, (d_row, d_col) in (("w", (-1, 0)), ("s", (1, 0)),
                                    ("a", (0, -1)), ("d", (0, 1))):
            nxt = (cell[0] + d_row, cell[1] + d_col)
            if nxt not in tunnel.WALLS and nxt not in previous:
                previous[nxt] = (cell, key)
                queue.append(nxt)
    keys, cell = [], tunnel.EXIT
    while previous[cell]:
        cell, key = previous[cell]
        keys.append(key)
    return keys[::-1]


def test_tunnel_caught_twice_sounds_the_alarm():
    puzzle = tunnel.TunnelPuzzle(GameState())
    keys = careless_tunnel_keys()
    assert len(keys) < 44
    assert press(puzzle, keys) == WRONG          # walking straight: caught
    puzzle.after_wrong()
    assert puzzle.player == tunnel.START and puzzle.tick == 0
    assert press(puzzle, keys) == GAME_OVER
    assert puzzle.ending_kind == "alarm"


def test_tunnel_wall_bump_is_not_a_turn():
    puzzle = tunnel.TunnelPuzzle(GameState())
    puzzle.handle_key("w")
    assert puzzle.tick == 0


# ----- P9 signals ---------------------------------------------------------
@pytest.mark.parametrize("document", sorted(signals.CLUES))
def test_each_route_document_gives_one_pattern(document):
    clues = signals.CLUES[document]
    assert signals.matching_patterns(clues) == [signals.ANSWER]
    for index in range(len(clues)):
        fewer = clues[:index] + clues[index + 1:]
        assert len(signals.matching_patterns(fewer)) > 1, (document, index)


def test_signal_panel():
    puzzle = signals.SignalsPuzzle(GameState())
    assert press(puzzle, ["e"]) == WRONG
    puzzle.after_wrong()
    assert press(puzzle, ["w", "w", "d", "d", "w", "d", "w", "w",
                          "e"]) == SOLVED


def test_every_puzzle_draws_and_ignores_unknown_keys():
    from engine.canvas import Canvas
    for cls in PUZZLES.values():
        puzzle = cls(GameState())
        for key in ["x", "z", "tab", "7"]:
            puzzle.handle_key(key)
        canvas = Canvas()
        puzzle.draw(canvas, 1, 0, 18, 80, 0)
        assert cls.hints and cls.title
