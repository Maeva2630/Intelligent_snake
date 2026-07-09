""" Main game engine: Pygame loop """

import pygame
from game.grid.grid import Grid
from game.render.render import Render

class Game:
    def __init__(self, grid_width: int = 32, grid_height: int = 24,
                 tile_size: int = 35, tick_rate: int = 10, food_density: float = 0.05):
        pygame.init()

        self.tile_size = tile_size
        self.grid = Grid(grid_width, grid_height)
        self.food_density = food_density

        self.screen = pygame.display.set_mode(
            (grid_width * tile_size, grid_height * tile_size)
        )
        self.render = Render(self.screen, tile_size)
        self.clock = pygame.time.Clock()

        self.running = True
        self.paused = False

        self._next_screen = "quit"

        self.tick_rate = tick_rate
        self.speed_multiplier: float = 1.0
        self._accumulator: float = 0.0

    def run(self) -> str:
        while self.running:
            dt = self.clock.tick(60) / 1000 # 60 fps

            self._handle_input()

            if not self.paused:
                self._accumulator += dt * self.speed_multiplier
                tick_duration = 1 / self.tick_rate

                while self._accumulator >= tick_duration:
                    self._update()
                    self._accumulator -= tick_duration

            self._render()

        return self._next_screen

    # Potentiellement revoir cette implémentation avec l'encaspulation de Maëva car
    # pour l'instant c'est **MOCHE**
    # Commentaires car c'est une idée de features et sans serpent la vitesse ne sert à rien
    # à moins que je mette un timer ? *smiley qui reflechit*
    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self._next_screen = "quit"

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    self._next_screen = "menu"
            # elif event.key == pygame.K_SPACE:
            #     self.paused = not self.paused
            # elif event.key == pygame.K_PLUS:
            #     self.speed_multiplier = min(self.speed_multiplier + 0.5, 6.0)
            # elif event.key == pygame.K_MINUS:
            #     self.speed_multiplier = max(self.speed_multiplier - 0.5, 0.5)

    def _update(self):
        pass

    def _render(self):
        self.screen.fill((0,0,0))
        self.render.draw_grid(self.grid)
        pygame.display.flip()
