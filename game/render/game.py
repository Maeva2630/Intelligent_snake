""" Main game engine: Pygame loop """

from game.encapsulation.window import Window
from game.encapsulation.render import Render
from game.encapsulation.event import EventType, Key
from game.encapsulation.rect import Rect
from game.render.constants import BACKGROUND
from game.render.menu import MIN_FOOD_DENSITY, MAX_FOOD_DENSITY, FOOD_DENSITY_STEP
from game.render.hud import Hud, AgentInfo, PANEL_WIDTH, MAX_VISIBLE_AGENTS
from game.grid.grid import Grid

from game.entity.food import FoodManager

MIN_WINDOW_HEIGHT = 480
MIN_SPEED_MULTIPLIER = 0.25
MAX_SPEED_MULTIPLIER = 8.0

class Game:
    def __init__(self, window: Window, grid_width: int = 32, grid_height: int = 24,
                 tile_size: int = 35, tick_rate: int = 10, num_agents: int = 2,
                 food_density: float = 0.05, fullscreen: bool = False):

        self.window = window

        self.tile_size = tile_size
        self.grid = Grid(grid_width, grid_height)
        self.food_density = food_density

        grid_pixel_width = grid_width * tile_size
        grid_pixel_height = grid_height * tile_size

        window_width = grid_pixel_width + PANEL_WIDTH
        window_height = max(grid_pixel_height, MIN_WINDOW_HEIGHT)
        self.window.resize(window_width, window_height, tile_size)
 
        self.render = Render(self.window.screen, tile_size)
        self.hud = Hud(self.render, grid_pixel_width, self.window.get_height())

        self.running = True
        self.paused = False
 
        self._next_screen = "quit"
 
        self.tick_rate = tick_rate
        self.speed_multiplier: float = 1.0
        self._accumulator: float = 0.0
        self.elapsed_ticks: int = 0
        self.food_manager = FoodManager(self.render, (grid_width, grid_height), food_density)

        self.food_manager.generate_food()
 
        self.agents: list[AgentInfo] = [
            AgentInfo(id=i + 1) for i in range(num_agents)
        ]

    def run(self) -> str:
        while self.running:
            dt = self.window.tick(60)

            self._handle_input()

            if not self.paused:
                self._accumulator += dt * self.speed_multiplier
                tick_duration = 1 / self.tick_rate

                while self._accumulator >= tick_duration:
                    self._update()
                    self._accumulator -= tick_duration

            self._render()

        return self._next_screen

    def _handle_input(self):
        for event in self.window.get_events():
            if event.type == EventType.QUIT:
                self.running = False
                self._next_screen = "quit"

            elif event.type == EventType.KEY_DOWN:
                if event.key == Key.ESCAPE:
                    self.running = False
                    self._next_screen = "menu"
            elif event.type == EventType.MOUSE_CLICK:
                action = self.hud.handle_click(event.mouse_pos)
                self._handle_hud_action(action)

    def _handle_hud_action(self, action: str | None):
        if action == "toggle_pause":
            self.paused = not self.paused

        elif action == "toggle_fullscreen":
            self._toggle_fullscreen()

        elif action == "food_minus":
            self.food_density = round(max(MIN_FOOD_DENSITY, self.food_density - FOOD_DENSITY_STEP), 2)

        elif action == "food_plus":
            self.food_density = round(min(MAX_FOOD_DENSITY, self.food_density + FOOD_DENSITY_STEP), 2)

        elif action == "speed_minus":
            self.speed_multiplier = max(MIN_SPEED_MULTIPLIER, self.speed_multiplier / 2)

        elif action == "speed_plus":
            self.speed_multiplier = min(MAX_SPEED_MULTIPLIER, self.speed_multiplier * 2)

        elif action == "add_ai":
            if len(self.agents) < MAX_VISIBLE_AGENTS:
                next_id = max((agent.id for agent in self.agents), default=0) + 1
                self.agents.append(AgentInfo(id=next_id))

        elif action == "back_to_menu":
            self.running = False
            self._next_screen = "menu"

    def _toggle_fullscreen(self):
        self.window.toggle_fullscreen()
        self.render.screen = self.window.screen

        panel_x = self.grid.width * self.tile_size

        self.hud.resize(
            panel_x,
            self.window.get_height(),
        )

    def _update(self):
        self.elapsed_ticks += 1
        for agent in self.agents:
            agent.play_time_ticks += 1
        self.food_manager.update()

    def _render(self):
        mouse_pos = self.window.get_mouse_pos()

        self.window.clear()
        bg_rect = Rect(0, 0, self.window.get_width(), self.window.get_height())
        self.render.draw_rect(bg_rect, BACKGROUND)
        self.render.draw_grid(self.grid)
        self.food_manager.draw_foods()
        self.hud.render_hud(
            self.speed_multiplier, self.elapsed_ticks, self.tick_rate,
            self.agents, self.food_density, self.paused, self.window.fullscreen, mouse_pos,
        )

        self.window.update()
