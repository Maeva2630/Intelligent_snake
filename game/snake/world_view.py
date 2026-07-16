""" World View """

from game.grid.grid import Grid

class WorldView:
    def __init__(self, grid: Grid, other_agents: list, foods: list, tick: int):
        self.grid = grid
        self.other_agents = other_agents
        self.tick = tick
        self.foods = foods
