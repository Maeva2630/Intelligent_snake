""" Agent: contain (Snake, Memory and Brain) """

from game.snake.snake import Snake
from game.snake.direction import Direction
from game.snake.world_view import WorldView
from game.snake.agent_brain import AgentBrain
from game.snake.agent_memory import AgentMemory

class Agent:
    def __init__(self, agent_id: int, start_position: tuple[int, int],
                 color: tuple[int, int, int], direction: Direction = Direction.EAST, vision_radius: int = 5):
        self.id = agent_id
        self.vision_radius = vision_radius
        self.snake = Snake(start_position, direction, initial_length=3)
        self.color = color
        self.memory = AgentMemory()
        self.brain = AgentBrain()
        self.play_time_ticks = 0
        self.last_visible_cells: dict[tuple[int, int], str] = {}

    @property
    def alive(self) -> bool:
        return self.snake.alive
    
    @property
    def length(self) -> int:
        return self.snake.length
    
    def tick(self, world_view: WorldView) -> None:
        if not self.alive:
            return
        self.last_visible_cells = self.get_visible_cells(world_view)
        self.memory.update_from_vision(self.last_visible_cells, world_view.tick)
        
        self.brain.decide(self, world_view)
        self.snake.move(world_view.grid)
        self.play_time_ticks += 1

    def get_visible_cells(self, world_view: WorldView) -> dict[tuple[int, int], str]:
        head_x, head_y = self.snake.head
        visible_cells = {}
        food_positions = {(food.x, food.y) for food in world_view.foods}

        fx, fy = self.snake.direction.delta()
        rx, ry = self.snake.direction.turn_right().delta()

        visible_cells[(head_x, head_y)] = "self"

        for i in range(1, self.vision_radius + 1):
            lateral_span = i - 1
            for j in range(-lateral_span, lateral_span + 1):
                dx = i * fx + j * rx
                dy = i * fy + j * ry
                x, y = world_view.grid.handle_toric(head_x + dx, head_y + dy)
                
                if (x, y) in food_positions:
                    visible_cells[(x, y)] = "food"
                elif any(other.alive and other.snake.occupies((x, y)) for other in world_view.other_agents):
                    visible_cells[(x, y)] = "agent"
                elif self.snake.occupies((x, y)):
                    visible_cells[(x, y)] = "self"
                else:
                    visible_cells[(x, y)] = "empty"
        # debug
        with open("visible_cells.txt", "a") as f:
            f.write(f"{visible_cells}\n")
        return visible_cells

def resolve_collisions(agents: list[Agent]) -> None:
    alive_agents = [agent for agent in agents if agent.alive]

    for agent in alive_agents:
        if agent.snake.collides_with_self():
            agent.snake.die()
            continue

        for other in alive_agents:
            if other is agent:
                continue
            if agent.snake.head in other.snake.body:
                agent.snake.die()
                break


