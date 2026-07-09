""" Graphic rendering: Draw the grid on a Pygame screen that has already been created by Game. """

from pygame import Surface, draw

class Render:
    def __init__(self, screen: Surface, tile_size: int):
        if tile_size < 0:
            raise Exception(f"The size of the tiles can't be negative: size={tile_size}")

        self.screen = screen
        self.tile_size = tile_size

    def draw_rect(self, x: int, y: int, color: tuple[int, int, int],
                  size: int | None = None, width: int = 0):
        size = size or self.tile_size
        draw.rect(self.screen, color, (x * size, y * size, size, size), width)

    def draw_grid(self, grid, color: tuple[int, int, int] = (255, 255, 255)):
        for x in range(grid.width):
            for y in range(grid.height):
                self.draw_rect(x, y, color, width=1)
