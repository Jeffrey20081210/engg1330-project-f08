"""All rooms of the station, built from the data in each room module."""

from rooms import concourse, platform
from rooms.room import Room

ROOM_DATA = {
    "platform": platform.ROOM,
    "concourse": concourse.ROOM,
}

ROOMS = {room_id: Room(data) for room_id, data in ROOM_DATA.items()}

# Station plan for the map screen (M): name, box position (row, col) inside
# the map pop-up, and which rooms are joined by a line.
STATION_PLAN = {
    "exit_hall": ("Exit hall", 0, 25),
    "control": ("Control room", 4, 2),
    "office": ("Ticket office", 4, 25),
    "tunnel": ("Service tunnel", 4, 48),
    "concourse": ("Concourse", 8, 25),
    "platform": ("Platform 1", 12, 25),
}
STATION_LINKS = [
    ("platform", "concourse"),
    ("concourse", "control"),
    ("concourse", "office"),
    ("concourse", "tunnel"),
    ("control", "exit_hall"),
    ("office", "exit_hall"),
    ("tunnel", "exit_hall"),
]


def get_room(room_id):
    return ROOMS[room_id]
