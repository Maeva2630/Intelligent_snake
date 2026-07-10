""" Main game engine: Pygame loop """

import pygame
from game.grid.grid import Grid
from game.render.hud import Hud, AgentInfo, PANEL_WIDTH, MAX_VISIBLE_AGENTS
from game.render.menu import MIN_FOOD_DENSITY, MAX_FOOD_DENSITY, FOOD_DENSITY_STEP
from game.render.render import Render

MIN_WINDOW_HEIGHT = 480
MIN_SPEED_MULTIPLIER = 0.25
MAX_SPEED_MULTIPLIER = 8.0

class Game:
    def __init__(self, grid_width: int = 32, grid_height: int = 24,
                 tile_size: int = 35, tick_rate: int = 10,
                 num_agents: int = 2, food_density: float = 0.05):
        pygame.init()
        pygame.display.set_caption("Intelligent Snake - Game")

        self.tile_size = tile_size
        self.grid = Grid(grid_width, grid_height)
        self.food_density = food_density

        grid_pixel_width = grid_width * tile_size
        grid_pixel_height = grid_height * tile_size
        window_width = grid_pixel_width + PANEL_WIDTH
        window_height = max(grid_pixel_height, MIN_WINDOW_HEIGHT)

        self.screen = pygame.display.set_mode(
            (window_width, window_height)
        )
        self.render = Render(self.screen, tile_size)
        self.hud = Hud(self.screen, panel_x=grid_pixel_width, panel_height=window_height)
        self.clock = pygame.time.Clock()

        self.running = True
        self.paused = False

        self._next_screen = "quit"

        self.tick_rate = tick_rate
        self.speed_multiplier: float = 1.0
        self._accumulator: float = 0.0
        self.elapsed_ticks: int = 0

        self.agents: list[AgentInfo] = [
            AgentInfo(id=i + 1) for i in range(num_agents)
        ]

    def run(self) -> str:
        while self.running:
            dt = self.clock.tick(60) / 1000 # 60 fps

            self._handle_input()

            if not self.paused:
                self._accumulator += dt * self.speed_multiplier
                tick_duration = 1 / self.tick_rate

                while self._accumulator >= tick_duration:
                    self._update()
                    self._accumulator -= tick_duration

            self._render()

        return self._next_screen

    # Potentiellement revoir cette implémentation avec l'encaspulation de Maëva car
    # pour l'instant c'est **MOCHE**
    # Commentaires car c'est une idée de features et sans serpent la vitesse ne sert à rien
    # à moins que je mette un timer ? *smiley qui reflechit*
    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self._next_screen = "quit"

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    self._next_screen = "menu"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                action = self.hud.handle_click(event.pos)
                self._handle_hud_action(action)

    def _handle_hud_action(self, action: str | None):
        if action == "toggle_pause":
            self.paused = not self.paused

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

    def _update(self):
        self.elapsed_ticks += 1
        for agent in self.agents:
            agent.play_time_ticks += 1

    def _render(self):
        mouse_pos = pygame.mouse.get_pos()

        self.screen.fill((0, 0, 0))
        self.render.draw_grid(self.grid)
        self.hud.render(
            self.speed_multiplier, self.elapsed_ticks, self.tick_rate,
            self.agents, self.food_density, self.paused, mouse_pos,
        )

        pygame.display.flip()
