""" Main game engine: Pygame loop """

import pygame
from grid.grid import Grid
from render.render import Render

class Game:
    def __init__(self, grid_width: int = 32, grid_height: int = 24,
                 tile_size: int = 35, tick_rate: int = 10):
        pygame.init()

        self.tile_size = tile_size
        self.grid = Grid(grid_width, grid_height)

        self.screen = pygame.display.set_mode(
            (grid_width * tile_size, grid_height * tile_size)
        )
        self.render = Render(self.screen, tile_size)
        self.clock = pygame.time.Clock()

        self.running = True

        self.tick_rate = tick_rate

    def run(self):
        while self.running:
            self._handle_input()
            self._update()
            self._render()

        pygame.quit()

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def _update(self):
        pass

    def _render(self):
        self.screen.fill((0,0,0))
        self.render.draw_grid(self.grid)
        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()
