"""Registry of all puzzles: puzzle id -> puzzle class."""

from puzzles.gate_code import GateCodePuzzle

PUZZLES = {
    GateCodePuzzle.id: GateCodePuzzle,
}


def make_puzzle(puzzle_id, state):
    return PUZZLES[puzzle_id](state)
