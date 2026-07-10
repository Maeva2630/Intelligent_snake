""" Main Menu: Configure the settings before launching the game. """

# import pygame

from game.encapsulation.rect import Rect
from game.encapsulation.event import Event, EventType, Key
from game.encapsulation.window import Window
from game.encapsulation.render import Render
from game.render.button import Button

from game.render.constants import ACCENT, BACKGROUND, LIGHT_GREEN, WHITE

GRID_PRESETS = [
    ("Small", 16, 12),
    ("Medium", 32, 24),
    ("Big", 48, 36),
]

MIN_AGENTS = 2
MAX_AGENTS = 42

MIN_FOOD_DENSITY = 0.01
MAX_FOOD_DENSITY = 2.00
FOOD_DENSITY_STEP = 0.01

class Menu:
    def __init__(self, window: Window):
        self.window = window
        self.render = Render(window.screen, tile_size=0)
        self.font_title = 48
        self.font = 30
        self.font_small = 22

        self.num_agents = MIN_AGENTS
        self.grid_preset_index = 0

        self.state = "main"
        self.food_density = 0.05

        self._build_main_buttons()
        self._build_settings_buttons()

    def _build_main_buttons(self):
        w = self.window.get_width()
        self.main_buttons = [
            Button(Rect(w // 2 - 100, 300, 200, 40), "Start", "play"),
            Button(Rect(w // 2 - 100, 350, 200, 40), "Settings", "settings"),
            Button(Rect(w // 2 - 100, 400, 200, 40), "Exit", "exit"),
        ]

    def _build_settings_buttons(self):
        w = self.window.get_width()
        self.settings_buttons = [
            Button(Rect(w // 2 - 40, 150, 40, 36), "-", "agents_minus"),
            Button(Rect(w // 2 + 20, 150, 40, 36), "+", "agents_plus"),
            Button(Rect(w // 2 - 40, 240, 40, 36), "-", "food_minus"),
            Button(Rect(w // 2 + 20, 240, 40, 36), "+", "food_plus"),
            Button(Rect(w // 2 - 50, 330, 120, 36), "Next size", "grid_size"),
            Button(Rect(w // 2 - 100, 400, 200, 40), "Back", "return_back"),
        ]

    def run(self) -> dict | None:
        running = True
        while running:
            delta_time = self.window.tick(60)

            # Potentiellement revoir cette implémentation avec l'encaspulation de Maëva car
            # pour l'instant c'est **MOCHE**
            for event in self.window.get_events():
                if event.type == EventType.QUIT:
                    return None

                if event.type == EventType.KEY_DOWN and event.key == Key.ESCAPE:
                    if self.state == "settings":
                        self.state = "main"
                    else:
                        return None

                if event.type == EventType.MOUSE_CLICK:
                    result = self._handle_click(event.mouse_pos)
                    if result == "play":
                        return self._build_config()
                    if result == "exit":
                        return None

            mouse_pos = self.window.get_mouse_pos()
            self._render(mouse_pos)

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
            else:
                return action

        return None

    def _build_config(self) -> dict:
        name, grid_width, grid_height = GRID_PRESETS[self.grid_preset_index]
        return {
            "num_agents": self.num_agents,
            "grid_width": grid_width,
            "grid_height": grid_height,
            "grid_preset_name": name,
            "food_density": self.food_density,
        }

    def _render(self, mouse_pos):
        self.window.clear()
 
        if self.state == "main":
            self._render_main(mouse_pos)
        else:
            self._render_settings(mouse_pos)

        self.window.update()

    def _render_main(self, mouse_pos):
        w = self.window.get_width()

        # titre:
        # Ouroboros (serpent infini) ?
        # King cobra (le serpent le + intelligent)
        # oulala je sais pas 
        self.render.draw_text("Intelligent Snake", w // 2, 60, self.font_title, ACCENT, align="center")
        self.render.draw_text("Configuration", w // 2, 100, self.font, ACCENT, align="center")
        self.render.draw_text(f"Number of AIs: {self.num_agents}", w // 2, 160, self.font, LIGHT_GREEN, align="center")
        self.render.draw_text(f"Food density: {self.food_density:.0%}", w // 2, 210, self.font, LIGHT_GREEN, align="center")
        
        name, gw, gh = GRID_PRESETS[self.grid_preset_index]
        self.render.draw_text(f"Grid Size: {name} ({gw}x{gh})", w // 2, 260, self.font, LIGHT_GREEN, align="center")

        for button in self.main_buttons:
            button.draw(self.render, self.font, BACKGROUND, mouse_pos)

    def _render_settings(self, mouse_pos):
        w = self.window.get_width()

        self.render.draw_text("Settings", w // 2, 60, self.font_title, ACCENT, align="center")
        self.render.draw_text(f"Number of AIs: {self.num_agents}", w // 2, 130, self.font, LIGHT_GREEN, align="center")
        self.render.draw_text(f"Food density: {self.food_density:.0%}", w // 2, 220, self.font, LIGHT_GREEN, align="center")

        name, gw, gh = GRID_PRESETS[self.grid_preset_index]
        self.render.draw_text(f"Grid Size: {name} ({gw}x{gh})", w // 2, 310, self.font, LIGHT_GREEN, align="center")

        for button in self.settings_buttons:
            button.draw(self.render, self.font, BACKGROUND, mouse_pos)
