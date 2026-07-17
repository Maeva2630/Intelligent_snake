""" Load the 4 snake sprites (head/body/tail/turn), then select the
correct rotation based on the connection directions of each segment.
"""

import os
import pygame
from game.snake.direction import Direction

_ASSET_DIR = "assets/snake/"

_FACING_ROTATION = {
    Direction.NORTH: 0,
    Direction.WEST: 90,
    Direction.SOUTH: 180,
    Direction.EAST: 270,
}

# frozenset is used to create a set that disregards both order and duplicates
_TURN_ROTATION = {
    frozenset((Direction.SOUTH, Direction.EAST)): 0, # or (Direction.EAST, Direction.SOUTH) with frozenset
    frozenset((Direction.EAST, Direction.NORTH)): 90, # or (Direction.NORTH, Direction.EAST) with frozenset
    frozenset((Direction.NORTH, Direction.WEST)): 180, # or (Direction.WEST, Direction.NORTH) with frozenset
    frozenset((Direction.WEST, Direction.SOUTH)): 270, # or (Direction.SOUTH, Direction.WEST) with frozenset
}

def _direction_between(grid, frm: tuple[int, int], to: tuple[int, int]) -> Direction | None:
    for direction in Direction:
        dx, dy = direction.delta()
        if grid.handle_toric(frm[0] + dx, frm[1] + dy) == to:
            return direction
    return None

class SnakeSprites:
    def __init__(self, tile_size: int, asset_dir: str = _ASSET_DIR):
        self.tile_size = tile_size
        self._asset_dir = asset_dir
        
        self._base = {name: self._load(name) for name in ("body", "tail", "turn")}
        self._head_shape = self._load("head_shape")
        self._head_eyes = {
            False: self._load("eyes_normal"),
            True: self._load("eyes_hunting"),
        }
        
        self._cache: dict[tuple, pygame.Surface] = {}

    def _load(self, name: str) -> pygame.Surface:
        image = pygame.image.load(os.path.join(self._asset_dir, f"{name}.png")).convert_alpha()
        return pygame.transform.smoothscale(image, (self.tile_size, self.tile_size))

    def _rotated(self, sprite: pygame.Surface, angle: int) -> pygame.Surface:
        if not angle:
            return sprite
        rotated = pygame.transform.rotate(sprite, angle)
        if rotated.get_size() != (self.tile_size, self.tile_size):
            rotated = pygame.transform.smoothscale(rotated, (self.tile_size, self.tile_size))
        return rotated

    def _get(self, name: str, angle: int, color: tuple[int, int, int]) -> pygame.Surface:
        key = (name, angle, color)
        cached = self._cache.get(key)
        if cached is not None:
            return cached

        sprite = self._rotated(self._base[name], angle)
        tinted = sprite.copy()
        tinted.fill(color + (255,), special_flags=pygame.BLEND_RGBA_MULT)
        self._cache[key] = tinted
        return tinted

    def head_sprite(self, direction: Direction, color: tuple[int, int, int], hunting: bool = False) -> pygame.Surface:
        angle = _FACING_ROTATION[direction]
        key = ("head", angle, color, hunting)
        cached = self._cache.get(key)
        if cached is not None:
            return cached

        shape = self._rotated(self._head_shape, angle)
        tinted_shape = shape.copy()
        tinted_shape.fill(color + (255,), special_flags=pygame.BLEND_RGBA_MULT)

        eyes = self._rotated(self._head_eyes[hunting], angle)

        composite = tinted_shape.copy()
        composite.blit(eyes, (0, 0))

        self._cache[key] = composite
        return composite

    def tail_sprite(self, direction_towards_body: Direction, color: tuple[int, int, int]) -> pygame.Surface:
        return self._get("tail", _FACING_ROTATION[direction_towards_body], color)

    def body_sprite(self, direction_a: Direction, direction_b: Direction,
                     color: tuple[int, int, int]) -> pygame.Surface:
        if direction_a == direction_b or direction_a == direction_b.turn_left().turn_left():
            angle = 90 if direction_a in (Direction.EAST, Direction.WEST) else 0
            return self._get("body", angle, color)

        angle = _TURN_ROTATION[frozenset((direction_a, direction_b))]
        return self._get("turn", angle, color)

    def draw_snake(self, render, grid, snake, color: tuple[int, int, int], hunting: bool = False) -> None:
        body = list(snake.body)
        n = len(body)

        for index, position in enumerate(body):
            x, y = position
            dest = (x * self.tile_size, y * self.tile_size)

            if index == 0:
                sprite = self.head_sprite(snake.direction, color, hunting)
            elif index == n - 1:
                direction_to_body = _direction_between(grid, position, body[index - 1])
                sprite = self.tail_sprite(direction_to_body, color)
            else:
                direction_to_head = _direction_between(grid, position, body[index - 1])
                direction_to_tail = _direction_between(grid, position, body[index + 1])
                sprite = self.body_sprite(direction_to_head, direction_to_tail, color)

            render.draw_surface(sprite, dest)
