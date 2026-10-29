"""Puzzle 1 (gate keypad): the logic must have exactly one answer."""

from engine.state import GameState
from puzzles.base import SOLVED, WRONG
from puzzles.gate_code import (CODE, LOG, PIECE_ORDER, GateCodePuzzle,
                               all_entries, describe, matching_codes,
                               receipt_lines, score)


def test_score_counts_right_and_misplaced_digits():
    assert score("964", "964") == (3, 0)
    assert score("957", "964") == (1, 0)
    assert score("149", "964") == (0, 2)
    assert score("823", "964") == (0, 0)


def test_log_matches_the_real_code():
    for attempt, right, wrong in all_entries():
        assert score(attempt, CODE) == (right, wrong), attempt


def test_exactly_one_code_fits_all_pieces():
    assert matching_codes(all_entries()) == [CODE]


def test_every_log_entry_is_needed():
    entries = all_entries()
    for index in range(len(entries)):
        fewer = entries[:index] + entries[index + 1:]
        assert len(matching_codes(fewer)) > 1, f"entry {index} is not needed"


def test_receipt_lines_fit_in_the_log_panel():
    for piece in PIECE_ORDER:
        for line in receipt_lines(piece):
            assert len(line) <= 33
    assert describe(0, 0) == "nothing is correct"
    assert set(LOG) == set(PIECE_ORDER)


def type_keys(puzzle, keys):
    result = None
    for key in keys:
        result = puzzle.handle_key(key)
    return result


def test_typing_the_right_code_solves_the_puzzle():
    puzzle = GateCodePuzzle(GameState())
    assert type_keys(puzzle, ["9", "6", "4", "enter"]) == SOLVED


def test_wrong_code_is_reported_and_entry_cleared():
    puzzle = GateCodePuzzle(GameState())
    assert type_keys(puzzle, ["1", "2", "3", "enter"]) == WRONG
    puzzle.after_wrong()
    assert puzzle.entry == ""
    assert puzzle.flash == "123"


def test_short_code_is_not_submitted():
    """Pressing OK with fewer than 3 digits does nothing (no time penalty)."""
    puzzle = GateCodePuzzle(GameState())
    assert type_keys(puzzle, ["9", "6", "enter"]) is None
    assert puzzle.entry == "96"


def test_fourth_digit_and_backspace():
    puzzle = GateCodePuzzle(GameState())
    type_keys(puzzle, ["1", "2", "3", "4"])
    assert puzzle.entry == "123"            # boundary: max 3 digits
    type_keys(puzzle, ["backspace", "backspace"])
    assert puzzle.entry == "1"
    type_keys(puzzle, ["backspace", "backspace"])
    assert puzzle.entry == ""               # deleting from empty is safe


def test_keypad_cursor_wraps_and_presses_buttons():
    puzzle = GateCodePuzzle(GameState())
    puzzle.handle_key("up")                 # from "1" wraps to the bottom row
    assert (puzzle.row, puzzle.col) == (3, 0)
    puzzle.handle_key("d")
    puzzle.handle_key("e")                  # presses "0"
    assert puzzle.entry == "0"


def test_unknown_keys_are_ignored():
    puzzle = GateCodePuzzle(GameState())
    for key in ["x", "z", "!", "tab"]:
        assert puzzle.handle_key(key) is None
    assert puzzle.entry == ""


def test_solving_opens_the_gate():
    state = GameState()
    puzzle = GateCodePuzzle(state)
    puzzle.on_solved()
    assert "gate_open" in state.flags
