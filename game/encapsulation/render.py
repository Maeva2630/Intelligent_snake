import pygame
import game.grid.grid as grid

class Render:
    def __init__(self, screen, tile_size):
        self.screen = screen
        self.tile_size = tile_size
        self.grid = [[0 for _ in range(screen.get_width() // tile_size)] for _ in range(screen.get_height() // tile_size)]

    def draw_rect(self, x, y, color, size):
        pygame.draw.rect(self.screen, color, (x * size, y * size, size, size))

    def draw_circle(self, x, y, color, size):
        pygame.draw.circle(self.screen, color, (int(x * size + size / 2), int(y * size + size / 2)), int(size / 2))

    def draw_grid(self, grid):
        """Draw game grid in background"""
        for x in range(grid.width):
            for y in range(grid.height):
                self.draw_rect(x, y, (255, 255, 255), self.tile_size)


    def draw_text(self, text, x, y, size, color, font: pygame.font.SysFont = None):
        """Draw text"""
        font = pygame.font.SysFont(font, size)
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))
