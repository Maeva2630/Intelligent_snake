
from pygame import Rect, draw, Surface
from render.constants import WHITE

class Button:
    def __init__(self, rect: Rect, label: str, action: str):
        self.rect = rect
        self.label = label
        self.action = action

    def is_hovered(self, mouse_pos) -> bool:
        return self.rect.collidepoint(mouse_pos)

    def draw(self, screen: Surface, font, color: tuple[int, int, int], mouse_pos: tuple[int, int]):
        if self.is_hovered(mouse_pos):
            r, g, b = color
            color = (min(r * 2, 255), min(g * 2, 255), min(b * 2, 255))

        draw.rect(screen, color, self.rect, border_radius=6)
        draw.rect(screen, WHITE, self.rect, width=1, border_radius=6)

        text_surface = font.render(self.label, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
