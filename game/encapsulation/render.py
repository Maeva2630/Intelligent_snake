import pygame
import game.grid.grid as grid
from game.encapsulation.rect import Rect 

class Render:
    """Encapsulate pygame rendering"""
    def __init__(self, screen, tile_size):
        self.screen = screen
        self.tile_size = tile_size
        self._fonts = {}
        if tile_size and tile_size > 0:
            self.grid = [[0 for _ in range(screen.get_width() // tile_size)] for _ in range(screen.get_height() // tile_size)]
        else:
            self.grid = []

    def draw_grid_cell(self, x, y, color, size, border_radius: int = 0):
        pygame.draw.rect(self.screen, color, (x * size, y * size, size, size), border_radius)

    def draw_rect(self, rect: Rect, color, width: int = 0, border_radius: int = 0):
        pygame.draw.rect(self.screen, color, (rect.x, rect.y, rect.width, rect.height), width, border_radius)

    def draw_circle(self, x, y, color, size):
        pygame.draw.circle(self.screen, color, (int(x * size + size / 2), int(y * size + size / 2)), int(size / 2))

    def draw_grid(self, grid):
        """Draw game grid in background"""
        for x in range(grid.width):
            for y in range(grid.height):
                self.draw_grid_cell(x, y, (255, 255, 255), self.tile_size)


    def _get_font(self, size: int):
        if size not in self._fonts:
            self._fonts[size] = pygame.font.SysFont(None, size)
        return self._fonts[size]

    def draw_text(self, text: str, x: int, y: int, size: int, color: tuple[int, int, int], align: str = "left"):
        """Draw text with alignment"""
        font = self._get_font(size)
        text_surface = font.render(text, True, color)
        rect = text_surface.get_rect()
        if align == "center":
            rect.center = (x, y)
        elif align == "left":
            rect.topleft = (x, y)
        self.screen.blit(text_surface, rect)

    def draw_surface(self, surface: pygame.Surface, dest):
        """Draw surface (rect or coordinates)"""
        self.screen.blit(surface, dest)

