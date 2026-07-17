""" Snake: position, body, energy """

from game.snake.direction import Direction
from collections import deque

MAX_SELF_COLLISIONS = 3

class Snake:
    def __init__(self, head: tuple[int, int], direction: Direction = Direction.EAST,
                 initial_length: int = 1):

        self.head = head
        self.direction = direction
        self.body: deque[tuple[int, int]] = deque([head])
        self.alive = True
        self._pending_growth = max(0, initial_length - 1)
        self.self_collision_count = MAX_SELF_COLLISIONS

    @property
    def length(self) -> int:
        return len(self.body)

    @property
    def tail(self) -> tuple[int, int] | None:
        return self.body[-1] if len(self.body) > 1 else None

    def will_vacate_tail(self) -> bool:
        return self._pending_growth <= 0

    def turn_left(self) -> None:
        self.direction = self.direction.turn_left()

    def turn_right(self) -> None:
        self.direction = self.direction.turn_right()

    def move(self, grid) -> None:
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

    def truncate_at_self_collision(self) -> None:
        body_list = list(self.body)
        try:
            collision_index = body_list.index(self.head, 1)
        except ValueError:
            return

        self.self_collision_count -= 1
        if self.self_collision_count <= 0:
            self.die()
            return

        self.body = deque(body_list[:collision_index])
