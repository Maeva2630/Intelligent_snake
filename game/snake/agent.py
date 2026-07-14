""" Agent: contain (Snake, Memory and Brain) """

from game.snake.snake import Snake
from game.snake.direction import Direction
from game.snake.world_view import WorldView
from game.snake.agent_brain import AgentBrain
from game.snake.agent_memory import AgentMemory

class Agent:
    def __init__(self, agent_id: int, start_position: tuple[int, int],
                 direction: Direction = Direction.EAST):
        self.id = agent_id
        self.snake = Snake(start_position, direction)
        self.memory = AgentMemory()
        self.brain = AgentBrain()
        self.play_time_ticks = 0

    @property
    def alive(self) -> bool:
        return self.snake.alive
    
    @property
    def length(self) -> int:
        return self.snake.length
    
    def tick(self, world_view: WorldView) -> None:
        if not self.alive:
            return
        
        self.brain.decide(self, world_view)
        self.snake.move(world_view.grid)
        self.play_time_ticks += 1