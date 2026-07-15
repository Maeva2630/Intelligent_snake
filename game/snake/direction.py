""" Direction """

from enum import Enum 

class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def delta(self) -> tuple[int, int]:
        return _DELTAS[self]

    def turn_left(self) -> "Direction":
        return Direction((self.value - 1) % 4)

    def turn_right(self) -> "Direction":
        return Direction((self.value + 1) % 4)

_DELTAS = {
    Direction.NORTH: (0, -1),
    Direction.EAST: (1, 0),
    Direction.SOUTH: (0, 1),
    Direction.WEST: (-1, 0),
}
