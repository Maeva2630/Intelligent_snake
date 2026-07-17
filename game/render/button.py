from game.encapsulation.rect import Rect
from game.encapsulation.render import Render
from game.render.constants import WHITE

class Button:
    def __init__(self, rect: Rect, label: str, action: str):
        self.rect = rect
        self.label = label
        self.action = action

    def is_hovered(self, mouse_pos) -> bool:
        if mouse_pos is None:
            return False
        return self.rect.collidepoint(*mouse_pos)

    def draw(self, render: Render, font_size: int, color: tuple[int, int, int], mouse_pos: tuple[int, int]):
        if self.is_hovered(mouse_pos):
            r, g, b = color
            color = (min(r * 2, 255), min(g * 2, 255), min(b * 2, 255))

        render.draw_rect(self.rect, color, border_radius=6)
        render.draw_rect(self.rect, WHITE, width=1, border_radius=6)

        render.draw_text(self.label, self.rect.center[0], self.rect.center[1], font_size, WHITE, align="center")
