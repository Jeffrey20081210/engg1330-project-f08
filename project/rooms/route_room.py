"""The shared shape of the three route rooms (entered from the concourse).

Rows 0-3 back wall, rows 4-15 floor, row 16 bottom wall with the door back
to the concourse (exit "1") in the middle.
"""

ROUTE_MAP = (
    ["#" * 80] * 4
    + ["||" + "." * 76 + "||"] * 12
    + ["#" * 37 + "1" * 5 + "#" * 38]
    + ["#" * 80]
)

START = (39, 14)


def back_to_concourse(door_x):
    """Exit data for the door back to the concourse, below route door x."""
    return {"to": "concourse", "entry": (door_x, 4), "facing": "down",
            "look": "opening"}
