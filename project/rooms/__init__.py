"""All rooms of the station, built from the data in each room module."""

from rooms import (concourse, control_room, exit_hall, platform, storeroom,
                   ticket_office)
from rooms.room import Room

ROOM_DATA = {
    "platform": platform.ROOM,
    "concourse": concourse.ROOM,
    "control_room": control_room.ROOM,
    "ticket_office": ticket_office.ROOM,
    "storeroom": storeroom.ROOM,
    "exit_hall": exit_hall.ROOM,
}

ROOMS = {room_id: Room(data) for room_id, data in ROOM_DATA.items()}

# Station plan for the map screen (M): name and box position (row, col)
# inside the map pop-up. The lines between boxes are drawn by the map.
STATION_PLAN = {
    "control_room": ("Control room", 1, 2),
    "ticket_office": ("Ticket office", 1, 25),
    "storeroom": ("Storeroom", 1, 48),
    "concourse": ("Concourse", 6, 25),
    "exit_hall": ("Exit hall", 6, 48),
    "platform": ("Platform 1", 11, 25),
}


def get_room(room_id):
    return ROOMS[room_id]


def enter_room(state, room_id, position=None, facing=None):
    """Put the player into a room (at its start if no position is given)."""
    room = ROOMS[room_id]
    state.room = room_id
    state.x, state.y = position or room.data["start"]
    if facing:
        state.facing = facing
    if room_id not in state.visited:
        state.visited.add(room_id)
        if room.data.get("first_visit"):
            state.say(room.data["first_visit"], "info")
