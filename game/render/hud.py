""" In-game HUD: control panel with speed, timer, list of AIs informations and a top 3. """

from dataclasses import dataclass
from render.button import Button
from render.constants import WHITE, ACCENT, BACKGROUND, LIGHT_GREEN
from game.encapsulation.rect import Rect
from game.encapsulation.render import Render

PANEL_WIDTH = 260
MAX_VISIBLE_AGENTS = 4

# Minimum des infos dont le hud a besoin sur les ia, à changer une fois que
# l'on aura vraiment notre ia
@dataclass
class AgentInfo:
    id: int
    length: int = 1
    play_time_ticks: int = 0

class Hud:
    def __init__(self, render: Render, panel_x: int, panel_height: int):
        
        self.render = render
        self.panel_x = panel_x
        self.panel_height = panel_height

        self.font_title = 30
        self.font = 22
        self.font_small = 18

        self._build_buttons()

    def _build_buttons(self):
        x = self.panel_x

        self.pause_btn = Button(Rect(x + 20, 15, 32, 32), "II", "toggle_pause")
        self.fullscreen_btn = Button(Rect(x + PANEL_WIDTH - 90, 15, 70, 32), "Full", "toggle_fullscreen")
        self.speed_minus_btn = Button(Rect(x + 20, 135, 32, 32), "-", "speed_minus")
        self.speed_plus_btn = Button(Rect(x + PANEL_WIDTH - 52, 135, 32, 32), "+", "speed_plus")
        self.food_minus_btn = Button(Rect(x + 20, 180, 32, 32), "-", "food_minus")
        self.food_plus_btn = Button(Rect(x + PANEL_WIDTH - 52, 180, 32, 32), "+", "food_plus")
        self.add_ai_btn = Button(Rect(x + 20, self.panel_height - 92, PANEL_WIDTH - 40, 36), "+ Add AI", "add_ai")
        self.back_btn = Button(Rect(x + 20, self.panel_height - 46, PANEL_WIDTH - 40, 36), "Back to menu", "back_to_menu",)

    def resize(self, panel_x, panel_height):
        self.panel_x = panel_x
        self.panel_height = panel_height
        self._build_buttons()

    def handle_click(self, mouse_pos) -> str | None:
        for button in (
            self.pause_btn, self.fullscreen_btn, self.speed_minus_btn, self.speed_plus_btn,
            self.food_minus_btn, self.food_plus_btn, self.add_ai_btn, self.back_btn,
        ):
            if button.is_hovered(mouse_pos):
                return button.action
        return None

    def render_hud(self, speed_multiplier: float, elapsed_ticks: int, tick_rate: int, agents: list[AgentInfo],
               food_density: float, paused: bool, fullscreen: bool, mouse_pos):

        self.render.draw_line((self.panel_x, 0), (self.panel_x, self.panel_height), WHITE)

        center_x = self.panel_x + PANEL_WIDTH // 2

        # Pause
        self.pause_btn.label = ">" if paused else "II"
        self.pause_btn.draw(self.render, self.font, BACKGROUND, mouse_pos)
        self.render.draw_text(
            "Paused" if paused else "Running", self.panel_x + 85, 25, self.font, LIGHT_GREEN
        )
 
        # Fullscreen
        self.fullscreen_btn.label = "Window" if fullscreen else "Full"
        self.fullscreen_btn.draw(self.render, self.font, BACKGROUND, mouse_pos)
 
        # Timer
        self.render.draw_text("TIME", center_x, 75, self.font, WHITE, align="center")
 
        seconds = int(elapsed_ticks / tick_rate) if tick_rate else 0
        minutes, secs = divmod(seconds, 60)
        self.render.draw_text(
            f"{minutes:02d}:{secs:02d}", center_x, 100, self.font_title, ACCENT, align="center"
        )
 
        # Speed
        self.render.draw_text(
            f"Speed x{speed_multiplier:.2f}", center_x, 155, self.font, LIGHT_GREEN, align="center"
        )
        self.speed_minus_btn.draw(self.render, self.font, BACKGROUND, mouse_pos)
        self.speed_plus_btn.draw(self.render, self.font, BACKGROUND, mouse_pos)
 
        # Food Density
        self.render.draw_text(
            f"Food density: {food_density:.0%}", center_x, 195, self.font, LIGHT_GREEN, align="center"
        )
        self.food_minus_btn.draw(self.render, self.font, BACKGROUND, mouse_pos)
        self.food_plus_btn.draw(self.render, self.font, BACKGROUND, mouse_pos)
 
        # Top 4
        y = 250
        self.render.draw_text("Top 4  -  length  (alive time)", self.panel_x + 20, y, self.font, ACCENT)
        y += 26
 
        top = sorted(agents, key=lambda a: a.length, reverse=True)[:MAX_VISIBLE_AGENTS]
        for rank, agent in enumerate(top, start=1):
            agent_seconds = int(agent.play_time_ticks / tick_rate) if tick_rate else 0
            line = f"{rank}. AI {agent.id}  -  {agent.length}  ({agent_seconds}s)"
            self.render.draw_text(line, self.panel_x + 20, y, self.font_small, LIGHT_GREEN)
            y += 20
 
        self.add_ai_btn.draw(self.render, self.font, BACKGROUND, mouse_pos)
        self.back_btn.draw(self.render, self.font, BACKGROUND, mouse_pos)
