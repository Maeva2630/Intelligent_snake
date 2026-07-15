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

    def draw_grid_cell(self, x, y, color, size, border_radius: int = 0):
        pygame.draw.rect(self.screen, color, (x * size, y * size, size, size), border_radius)

    def draw_rect(self, rect: Rect, color, width: int = 0, border_radius: int = 0):
        pygame.draw.rect(self.screen, color, (rect.x, rect.y, rect.width, rect.height), width, border_radius)

    def draw_circle(self, x, y, color, size):
        pygame.draw.circle(self.screen, color, (int(x * size + size / 2), int(y * size + size / 2)), int(size / 2))

    def draw_line(self, start: tuple[int, int], end: tuple[int, int], color, width: int = 1):
        """Draw a straight line"""
        pygame.draw.line(self.screen, color, start, end, width)

    def draw_grid(self, grid):
        """Draw game grid in background"""
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

    def draw_snake(self, snake, body_color, head_color = None, border_radius: int = 4):
        """Draw a snake's body cell by cell"""
        head_color = head_color or body_color

        for index, segment in enumerate(snake.body):
            color = head_color if index == 0 else body_color
            self.draw_grid_cell(segment[0], segment[1], color, self.tile_size, border_radius=border_radius)

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
