""" Main Menu: Configure the settings before launching the game. """

from game.encapsulation.rect import Rect
from game.encapsulation.event import EventType, Key
from game.encapsulation.window import Window
from game.encapsulation.render import Render
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
    def __init__(self, window: Window, screen_width: int = 640, screen_height: int = 480):

        self.window = window
        self.window.resize(screen_width, screen_height)

        self.render = Render(self.window.screen, tile_size=0)

        self.logo = self.render.load_image("assets/logo/Ouroboros.png", (48, 48))

        self.font_title = 48
        self.font = 30
        self.font_small = 22

        self.num_agents = MIN_AGENTS
        self.grid_preset_index = 0

        self.state = "main"
        self.food_density = 0.05
        self.fullscreen = self.window.fullscreen

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
            Button(Rect(w - 90, 15, 70, 32), "Full", "toggle_fullscreen"),
        ]

    def run(self) -> dict | None:
        running = True
        while running:
            self.window.tick(60)

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

            self._render(self.window.get_mouse_pos())

        return None

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
        self.window.toggle_fullscreen()
        self.fullscreen = self.window.fullscreen
        self.render.screen = self.window.screen

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
        self.window.clear()
 
        if self.state == "main":
            self._render_main(mouse_pos)
        else:
            self._render_settings(mouse_pos)

        self.window.update()

    def _render_main(self, mouse_pos):
        w = self.window.get_width()

        bg_rect = Rect(0, 0, w, self.window.get_height())
        self.render.draw_rect(bg_rect, BACKGROUND)

        title_x = w // 2
        title_y = 60

        self.render.draw_image(self.logo, title_x - 76, title_y - 10, align="center" )
        self.render.draw_text("     uroboros", title_x, title_y, self.font_title,  ACCENT, align="center")

        self.render.draw_text("Configuration", w // 2, 100, self.font, ACCENT, align="center")
        self.render.draw_text(f"Number of AIs: {self.num_agents}", w // 2, 160, self.font, LIGHT_GREEN, align="center")
        self.render.draw_text(f"Food density: {self.food_density:.0%}", w // 2, 210, self.font, LIGHT_GREEN, align="center")
        
        name, gw, gh = GRID_PRESETS[self.grid_preset_index]
        self.render.draw_text(f"Grid Size: {name} ({gw}x{gh})", w // 2, 260, self.font, LIGHT_GREEN, align="center")

        for button in self.main_buttons:
            button.draw(self.render, self.font, BACKGROUND, mouse_pos)

    def _render_settings(self, mouse_pos):
        w = self.window.get_width()

        bg_rect = Rect(0, 0, w, self.window.get_height())
        self.render.draw_rect(bg_rect, BACKGROUND)

        self.render.draw_text("Settings", w // 2, 60, self.font_title, ACCENT, align="center")
        self.render.draw_text(f"Number of AIs: {self.num_agents}", w // 2, 130, self.font, LIGHT_GREEN, align="center")
        self.render.draw_text(f"Food density: {self.food_density:.0%}", w // 2, 220, self.font, LIGHT_GREEN, align="center")

        name, gw, gh = GRID_PRESETS[self.grid_preset_index]
        self.render.draw_text(f"Grid Size: {name} ({gw}x{gh})", w // 2, 310, self.font, LIGHT_GREEN, align="center")

        for button in self.settings_buttons:
            button.draw(self.render, self.font, BACKGROUND, mouse_pos)
