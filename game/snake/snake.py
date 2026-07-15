""" Snake: position, body, energy """

from game.snake.direction import Direction
from game.grid.grid import Grid
from collections import deque

DEFAULT_ENERGY = 100

class Snake:
    def __init__(self, head: tuple[int, int], direction: Direction = Direction.EAST,
                 initial_length: int = 1, energy: int = DEFAULT_ENERGY):

        self.head = head
        self.direction = direction
        self.body: deque[tuple[int, int]] = deque([head])
        self.energy = energy
        self.alive = True
        self._pending_growth = max(0, initial_length - 1)

    @property
    def length(self) -> int:
        return len(self.body)

    def turn_left(self) -> None:
        self.direction = self.direction.turn_left()

    def turn_right(self) -> None:
        self.direction = self.direction.turn_right()

    def move(self, grid: Grid) -> None:
        if not self.alive:
            return

        dx, dy = self.direction.delta()
        new_head = grid.handle_toric(self.head[0] + dx, self.head[1] + dy)
        self.head = new_head
 
        self.body.appendleft(self.head)
        if self._pending_growth > 0:
            self._pending_growth -= 1
        else:
            self.body.pop()

    def grow(self) -> None:
        self._pending_growth += 1

    def die(self) -> None:
        self.alive = False

    def occupies(self, position: tuple[int, int]) -> bool:
        return position in self.body

    def collides_with_self(self) -> bool:
        return self.head in list(self.body)[1:]
