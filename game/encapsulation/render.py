import pygame
from game.encapsulation.rect import Rect
from game.render.constants import WHITE, BACKGROUND

class Render:
    """Encapsulate pygame rendering"""
    def __init__(self, screen, tile_size):
        self.screen = screen
        self.tile_size = tile_size
        self._fonts = {}
        self._images = {}

        if tile_size and tile_size > 0:
            self.grid = [[0 for _ in range(screen.get_width() // tile_size)] for _ in range(screen.get_height() // tile_size)]
        else:
            self.grid = []

    def draw_grid_cell(self, x: int, y: int, color: tuple[int, int, int], size: int, border_radius: int = 0):
        pygame.draw.rect(self.screen, color, (x * size, y * size, size, size), border_radius)

    def draw_vision(self, x: int, y: int, color: tuple[int, int, int], alpha: int = 50):
        """Draw vision field"""
        s = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
        s.fill((*color, alpha))
        self.screen.blit(s, (x * self.tile_size, y * self.tile_size))

    def draw_dim_overlay(self, color: tuple[int, int, int], alpha: int = 150):
        """Draw a semi-transparent screen overlay"""
        s = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        s.fill((*color, alpha))
        self.screen.blit(s, (0, 0))

    def draw_rect(self, rect: Rect, color: tuple[int, int, int], width: int = 0, border_radius: int = 0):
        pygame.draw.rect(self.screen, color, (rect.x, rect.y, rect.width, rect.height), width, border_radius)

    def draw_circle(self, x: int, y: int, color: tuple[int, int, int], size: int):
        pygame.draw.circle(self.screen, color, (int(x * size + size / 2), int(y * size + size / 2)), int(size / 2))

    def draw_line(self, start: tuple[int, int], end: tuple[int, int], color: tuple[int, int, int], width: int = 1):
        """Draw a straight line"""
        pygame.draw.line(self.screen, color, start, end, width)

    def draw_grid(self, grid, tile_size: int = None):
        """Draw game grid in background"""
        if tile_size is None:
            tile_size = self.tile_size
            
        for x in range(grid.width):
            for y in range(grid.height):

                pygame.draw.rect(
                    self.screen,
                    WHITE,
                    (
                        x * self.tile_size,
                        y * self.tile_size,
                        self.tile_size,
                        self.tile_size,
                    ),
                    1
                )

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

    def load_image(self, path: str, size: tuple[int, int] | None = None) -> pygame.Surface:
        """Load an image only once"""
        key = (path, size)

        if key not in self._images:
            image = pygame.image.load(path).convert_alpha()

            if size is not None:
                image = pygame.transform.smoothscale(image, size)

            self._images[key] = image

        return self._images[key]


    def draw_image(self, image: pygame.Surface, x: int, y: int, align: str = "topleft"):
        """Draw an image with alignment"""
        rect = image.get_rect()

        if align == "center":
            rect.center = (x, y)
        elif align == "midleft":
            rect.midleft = (x, y)
        elif align == "midright":
            rect.midright = (x, y)
        else:
            rect.topleft = (x, y)

        self.screen.blit(image, rect)
