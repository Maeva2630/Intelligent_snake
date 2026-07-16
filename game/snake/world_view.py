""" World View """

from game.grid.grid import Grid

class WorldView:
    def __init__(self, grid: Grid, other_agents: list, foods: list, tick: int):
        self.grid = grid
        self.other_agents = other_agents
        self.tick = tick
        self.foods = foods

    # def visible_cells(self, agent, vision_radius: int):
    #     visible: dict[tuple[int, int], str] = {}
    #     for offset in range(1, vision_radius + 1):
    #         for dx, dy in [(offset, 0), (-offset, 0), (0, offset), (0, -offset)]:
    #             nx, ny = agent.snake.handle_toric(agent.snake.head[0] + dx, agent.snake.head[1] + dy)
    #             content = self.grid.get(nx, ny)
    #             if content is not None:
    #                 visible[(nx, ny)] = content
    #     return visible
