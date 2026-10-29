"""Registry of all puzzles: puzzle id -> puzzle class."""

from puzzles.boxes import BoxesPuzzle
from puzzles.breakers import BreakersPuzzle
from puzzles.gate_code import GateCodePuzzle
from puzzles.lockers import LockersPuzzle
from puzzles.morse import MorsePuzzle
from puzzles.signals import SignalsPuzzle
from puzzles.stations import StationsPuzzle
from puzzles.tunnel import TunnelPuzzle
from puzzles.wires import WiresPuzzle

PUZZLE_CLASSES = [GateCodePuzzle, LockersPuzzle, BreakersPuzzle, WiresPuzzle,
                  StationsPuzzle, MorsePuzzle, BoxesPuzzle, TunnelPuzzle,
                  SignalsPuzzle]
PUZZLES = {cls.id: cls for cls in PUZZLE_CLASSES}


def make_puzzle(puzzle_id, state):
    """Return the puzzle object for this run, creating it the first time.

    Keeping the object in the state means that leaving a puzzle with Esc
    does not reset it (so leaving is not a free restart).
    """
    if puzzle_id not in state.puzzles:
        state.puzzles[puzzle_id] = PUZZLES[puzzle_id](state)
    return state.puzzles[puzzle_id]
