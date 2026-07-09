import pygame
from game.encaspulation.render import Render


class Window:
    def __init__(self, screen_width: int, screen_height: int, tile_size: int):
        self.tile_size = tile_size
        self.screen_width = screen_width
        self.screen_height = screen_height

        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.running = True

    def clear(self):
        """Clear screen by filling it with a black color"""
        self.screen.fill((0, 0, 0))

    def update(self):
        """Update the screen"""
        pygame.display.flip()


    def tick(self, fps: int = 60) -> float:
        """Update deltatime in seconds"""
        return self.clock.tick(fps) / 1000.0


    def get_events(self) -> list:
        """Return pygame events"""
        return pygame.event.get()

    def quit(self):
        """Quit pygame"""
        self.running = False
        pygame.quit()
