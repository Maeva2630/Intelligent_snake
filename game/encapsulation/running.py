import pygame
from game.render.render import Render

class Running:
    def __init__(self, screen_width: int, screen_height: int, tile_size: int):
        self.tile_size = tile_size
        self.screen_width = screen_width
        self.screen_height = screen_height
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width * self.tile_size, self.screen_height * self.tile_size))
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
        self.render = Render(self.screen, self.tile_size)

    def run(self, grid, foods, snakes):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
        
            self.render.render_scene(self.grid, self.foods, self.snakes)
            pygame.display.flip()

            self.dt = self.clock.tick(60) / 1000

        pygame.quit()
