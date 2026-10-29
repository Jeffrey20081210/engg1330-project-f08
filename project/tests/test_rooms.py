"""Room data must be valid: right size, reachable starts, real puzzles."""

import pytest

import config
from engine.state import GameState
from puzzles import PUZZLES
from rooms import ROOM_DATA, ROOMS
from rooms.room import check_room_data, feet_cells


@pytest.mark.parametrize("room_id", sorted(ROOM_DATA))
def test_room_data_has_no_problems(room_id):
    assert check_room_data(ROOM_DATA[room_id]) == []


def standing_ok(room, x, y):
    """The player can stand here: feet on floor, head still on the map."""
    return y >= 2 and all(room.walkable(c, r) for c, r in feet_cells(x, y))


@pytest.mark.parametrize("room_id", sorted(ROOMS))
def test_start_and_exit_entries_are_walkable(room_id):
    room = ROOMS[room_id]
    assert standing_ok(room, *room.data["start"])
    for info in room.exits.values():
        if info.get("to"):
            target = ROOMS[info["to"]]
            assert standing_ok(target, *info["entry"]), info


@pytest.mark.parametrize("room_id", sorted(ROOMS))
def test_spots_are_inside_the_map_and_reachable(room_id):
    room = ROOMS[room_id]
    for spot in room.spots:
        left, top, right, bottom = spot["zone"]
        assert 0 <= left <= right < config.SCREEN_WIDTH
        assert 0 <= top <= bottom < config.MAP_HEIGHT
        reachable = any(standing_ok(room, x, y)
                        for x in range(left, right + 1)
                        for y in range(top, bottom + 1))
        assert reachable, spot["id"]
        if spot["kind"] == "puzzle":
            assert spot["puzzle"] in PUZZLES


def test_locked_gate_opens_with_flag():
    room = ROOMS["platform"]
    state = GameState()
    assert not room.exit_open("1", state)
    state.flags.add("gate_open")
    assert room.exit_open("1", state)
