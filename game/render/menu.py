""" Main Menu: Configure the settings before launching the game. """

import pygame
from game.render.button import Button
from game.render.constants import ACCENT, BACKGROUND, LIGHT_GREEN

GRID_PRESETS = [
    ("Small", 16, 12),
    ("Medium", 32, 24),
    ("Big", 48, 36),
]

MIN_AGENTS = 1
MAX_AGENTS = 4

MIN_FOOD_DENSITY = 0.01
MAX_FOOD_DENSITY = 2.00
FOOD_DENSITY_STEP = 0.01

class Menu:
    def __init__(self, window_width: int = 640, window_height: int = 480):
        pygame.init()

        self.screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("Intelligent Snake - Menu")
        self.clock = pygame.time.Clock()

        self.window_size = (window_width, window_height)
        self.fullscreen = False

        self.font_title = pygame.font.SysFont(None, 48)
        self.font = pygame.font.SysFont(None, 30)
        self.font_small = pygame.font.SysFont(None, 22)

        self.num_agents = MIN_AGENTS
        self.grid_preset_index = 0

        self.state = "main"
        self.food_density = 0.05

        self._build_main_buttons()
        self._build_settings_buttons()

    def _build_main_buttons(self):
        w = self.screen.get_width()
        self.main_buttons = [
            Button(pygame.Rect(w // 2 - 100, 300, 200, 40), "Start", "play"),
            Button(pygame.Rect(w // 2 - 100, 350, 200, 40), "Settings", "settings"),
            Button(pygame.Rect(w // 2 - 100, 400, 200, 40), "Exit", "exit"),
        ]

    def _build_settings_buttons(self):
        w = self.screen.get_width()
        self.settings_buttons = [
            Button(pygame.Rect(w // 2 - 40, 150, 40, 36), "-", "agents_minus"),
            Button(pygame.Rect(w // 2 + 20, 150, 40, 36), "+", "agents_plus"),
            Button(pygame.Rect(w // 2 - 40, 240, 40, 36), "-", "food_minus"),
            Button(pygame.Rect(w // 2 + 20, 240, 40, 36), "+", "food_plus"),
            Button(pygame.Rect(w // 2 - 50, 330, 120, 36), "Next size", "grid_size"),
            Button(pygame.Rect(w // 2 - 100, 400, 200, 40), "Back", "return_back"),
            Button(pygame.Rect(w - 90, 15, 70, 32), "Full", "toggle_fullscreen")
        ]

    def run(self) -> dict | None:
        running = True
        while running:
            self.clock.tick(60)

            # Potentiellement revoir cette implémentation avec l'encaspulation de Maëva car
            # pour l'instant c'est **MOCHE**
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if self.state == "settings":
                        self.state = "main"
                    else:
                        return None

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    result = self._handle_click(event.pos)
                    if result == "play":
                        return self._build_config()
                    if result == "exit":
                        return None

            self._render(pygame.mouse.get_pos())

        return None

    # Potentiellement revoir cette implémentation avec l'encaspulation de Maëva car
    # pour l'instant c'est **MOCHE**
    def _handle_click(self, mouse_pos):
        buttons = self.main_buttons if self.state == "main" else self.settings_buttons

        for button in buttons:
            if not button.is_hovered(mouse_pos):
                continue

            action = button.action
            if action == "agents_minus":
                self.num_agents = max(MIN_AGENTS, self.num_agents - 1)
            elif action == "agents_plus":
                self.num_agents = min(MAX_AGENTS, self.num_agents + 1)
            elif action == "grid_size":
                self.grid_preset_index = (self.grid_preset_index + 1) % len(GRID_PRESETS)
            elif action == "settings":
                self.state = "settings"
            elif action == "return_back":
                self.state = "main"
            elif action == "food_minus":
                self.food_density = round(max(MIN_FOOD_DENSITY, self.food_density - FOOD_DENSITY_STEP), 2)
            elif action == "food_plus":
                self.food_density = round(min(MAX_FOOD_DENSITY, self.food_density + FOOD_DENSITY_STEP), 2)
            elif action == "toggle_fullscreen":
                self._toggle_fullscreen()
            else:
                return action

        return None

    def _toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen

        if self.fullscreen:
            try:
                self.screen = pygame.display.set_mode(
                    self.window_size, pygame.FULLSCREEN | pygame.SCALED
                )

            except pygame.error:
                self.fullscreen = False
                pygame.display.quit()
                pygame.display.init()
                self.screen = pygame.display.set_mode(self.window_size)
        else:
            self.screen = pygame.display.set_mode(self.window_size)

    def _build_config(self) -> dict:
        name, grid_width, grid_height = GRID_PRESETS[self.grid_preset_index]
        return {
            "num_agents": self.num_agents,
            "grid_width": grid_width,
            "grid_height": grid_height,
            "grid_preset_name": name,
            "food_density": self.food_density,
            "fullscreen": self.fullscreen
        }

    def _render(self, mouse_pos):
        self.screen.fill(BACKGROUND)
 
        if self.state == "main":
            self._render_main(mouse_pos)
        else:
            self._render_settings(mouse_pos)

        pygame.display.flip()

    def _render_main(self, mouse_pos):
        w = self.screen.get_width()

        # titre:
        # Ouroboros (serpent infini) ?
        # King cobra (le serpent le + intelligent)
        title = self.font_title.render("Intelligent Snake", True, ACCENT)
        self.screen.blit(title, title.get_rect(center=(w // 2, 60)))

        config_label = self.font.render("Configuration", True, ACCENT)
        self.screen.blit(config_label, config_label.get_rect(center=(w // 2, 100)))

        ai_label = self.font.render(f"Number of AIs: {self.num_agents}", True, LIGHT_GREEN)
        self.screen.blit(ai_label, ai_label.get_rect(center=(w // 2, 160)))

        food_label = self.font.render(f"Food density: {self.food_density:.0%}", True, LIGHT_GREEN)
        self.screen.blit(food_label, food_label.get_rect(center=(w // 2, 210)))

        name, gw, gh = GRID_PRESETS[self.grid_preset_index]
        grid_label = self.font.render(f"Grid Size: {name} ({gw}x{gh})", True, LIGHT_GREEN)
        self.screen.blit(grid_label, grid_label.get_rect(center=(w // 2, 260)))

        for button in self.main_buttons:
            button.draw(self.screen, self.font, BACKGROUND, mouse_pos)

    def _render_settings(self, mouse_pos):
        w = self.screen.get_width()

        title = self.font_title.render("Settings", True, ACCENT)
        self.screen.blit(title, title.get_rect(center=(w // 2, 60)))

        label = self.font.render(f"Number of AIs: {self.num_agents}", True, LIGHT_GREEN)
        self.screen.blit(label, label.get_rect(center=(w // 2, 130)))

        label = self.font.render(f"Food density: {self.food_density:.0%}", True, LIGHT_GREEN)
        self.screen.blit(label, label.get_rect(center=(w // 2, 220)))

        name, gw, gh = GRID_PRESETS[self.grid_preset_index]
        grid_label = self.font.render(f"Grid Size: {name} ({gw}x{gh})", True, LIGHT_GREEN)
        self.screen.blit(grid_label, grid_label.get_rect(center=(w // 2, 310)))

        for button in self.settings_buttons:
            button.draw(self.screen, self.font, BACKGROUND, mouse_pos)
