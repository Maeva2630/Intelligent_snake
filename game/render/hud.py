""" In-game HUD: control panel with speed, timer, list of AIs informations and a top 3. """

from dataclasses import dataclass
import pygame
from render.button import Button
from render.constants import WHITE, ACCENT, BACKGROUND, LIGHT_GREEN

PANEL_WIDTH = 260
MAX_VISIBLE_AGENTS = 4

# Minimum des infos dont le hud a besoin sur les ia, à changer une fois que l'on aura
# vraiment notre ia
@dataclass
class AgentInfo:
    id: int
    length: int = 1
    play_time_ticks: int = 0

class Hud:
    def __init__(self, screen: pygame.Surface, panel_x: int, panel_height: int):
        self.screen = screen
        self.panel_x = panel_x
        self.panel_height = panel_height

        self.font_title = pygame.font.SysFont(None, 30)
        self.font = pygame.font.SysFont(None, 22)
        self.font_small = pygame.font.SysFont(None, 18)

        self._build_buttons()

    def _build_buttons(self):
        x = self.panel_x

        self.pause_btn = Button(pygame.Rect(x + 20, 15, 32, 32), "II", "toggle_pause")
        self.fullscreen_btn = Button(
            pygame.Rect(x + PANEL_WIDTH - 90, 15, 70, 32), "Full", "toggle_fullscreen"
        )
        self.speed_minus_btn = Button(pygame.Rect(x + 20, 135, 32, 32), "-", "speed_minus")
        self.speed_plus_btn = Button(pygame.Rect(x + PANEL_WIDTH - 52, 135, 32, 32), "+", "speed_plus")
        self.food_minus_btn = Button(pygame.Rect(x + 20, 180, 32, 32), "-", "food_minus")
        self.food_plus_btn = Button(pygame.Rect(x + PANEL_WIDTH - 52, 180, 32, 32), "+", "food_plus")
        self.add_ai_btn = Button(
            pygame.Rect(x + 20, self.panel_height - 92, PANEL_WIDTH - 40, 36), "+ Add AI", "add_ai"
        )
        self.back_btn = Button(
            pygame.Rect(x + 20, self.panel_height - 46, PANEL_WIDTH - 40, 36),
            "Back to menu", "back_to_menu",
        )

    def handle_click(self, mouse_pos) -> str | None:
        for button in (
            self.pause_btn, self.fullscreen_btn, self.speed_minus_btn, self.speed_plus_btn,
            self.food_minus_btn, self.food_plus_btn, self.add_ai_btn, self.back_btn,
        ):
            if button.is_hovered(mouse_pos):
                return button.action
        return None

    def render(self, speed_multiplier: float, elapsed_ticks: int, tick_rate: int, agents: list[AgentInfo],
               food_density: float, paused: bool, fullscreen: bool, mouse_pos):
        panel_rect = pygame.Rect(self.panel_x, 0, PANEL_WIDTH, self.panel_height)
        pygame.draw.rect(self.screen, BACKGROUND, panel_rect)
        pygame.draw.line(self.screen, WHITE, (self.panel_x, 0), (self.panel_x, self.panel_height))

        center_x = self.panel_x + PANEL_WIDTH // 2

        # Pause
        self.pause_btn.label = ">" if paused else "II"
        self.pause_btn.draw(self.screen, self.font, BACKGROUND, mouse_pos)
        pause_state_label = self.font.render(
            "Paused" if paused else "Running", True, LIGHT_GREEN
        )
        self.screen.blit(pause_state_label, (self.panel_x + 85, 25))

        # Fullscreen
        self.fullscreen_btn.label = "Window" if fullscreen else "Full"
        self.fullscreen_btn.draw(self.screen, self.font, BACKGROUND, mouse_pos)

        # Timer
        time_caption = self.font.render("TIME", True, WHITE)
        self.screen.blit(time_caption, time_caption.get_rect(center=(center_x, 75)))

        seconds = int(elapsed_ticks / tick_rate) if tick_rate else 0
        minutes, secs = divmod(seconds, 60)
        timer_label = self.font_title.render(f"{minutes:02d}:{secs:02d}", True, ACCENT)
        self.screen.blit(timer_label, timer_label.get_rect(center=(center_x, 100)))

        # Speed
        speed_label = self.font.render(f"Speed x{speed_multiplier:.2f}", True, LIGHT_GREEN)
        self.screen.blit(speed_label, speed_label.get_rect(center=(center_x, 155)))
        self.speed_minus_btn.draw(self.screen, self.font, BACKGROUND, mouse_pos)
        self.speed_plus_btn.draw(self.screen, self.font, BACKGROUND, mouse_pos)

        # Food Density
        food_label = self.font.render(f"Food density: {food_density:.0%}", True, LIGHT_GREEN)
        self.screen.blit(food_label, food_label.get_rect(center=(center_x, 195)))
        self.food_minus_btn.draw(self.screen, self.font, BACKGROUND, mouse_pos)
        self.food_plus_btn.draw(self.screen, self.font, BACKGROUND, mouse_pos)

        # Top 4
        y = 250
        leaderboard_title = self.font.render("Top 4  -  length  (alive time)", True, ACCENT)
        self.screen.blit(leaderboard_title, (self.panel_x + 20, y))
        y += 26

        top = sorted(agents, key=lambda a: a.length, reverse=True)[:MAX_VISIBLE_AGENTS]
        for rank, agent in enumerate(top, start=1):
            agent_seconds = int(agent.play_time_ticks / tick_rate) if tick_rate else 0
            line = f"{rank}. AI {agent.id}  -  {agent.length}  ({agent_seconds}s)"
            text = self.font_small.render(line, True, LIGHT_GREEN)
            self.screen.blit(text, (self.panel_x + 20, y))
            y += 20

        self.add_ai_btn.draw(self.screen, self.font, BACKGROUND, mouse_pos)
        self.back_btn.draw(self.screen, self.font, BACKGROUND, mouse_pos)
