""" Agent Brain: FSM, decision logic  """

from enum import Enum
from game.snake.direction import Direction

LOW_ERNGY = 30

class AgentState(Enum):
    EXPLORATION = "exploration"
    TARGET = "target"
    SURVIVAL = "survival"
    DODGE = "dodge"

class AgentBrain:
    def __init__(self):
        self.current_state = AgentState.EXPLORATION

    def decide(self, agent, world_view) -> None:
        self._update_state(agent)

        if self.current_state == AgentState.SURVIVAL:
            self._move_towards_known_food(agent, world_view)
        else:
            self._avoid_immediate_collisiont(agent, world_view)
    
    def _update_state(self, agent) -> None:
        if agent.snake.energy <= LOW_ERNGY:
            self.current_state = AgentState.SURVIVAL
        elif agent.memory.known_resources():
            self.current_state = AgentState.TARGET
        else:
            self.current_state = AgentState.EXPLORATION

    def _move_towards_known_food(self, agent, world_view) -> None:
        target = agent.memory.closest_known_resource(agent.snake.head, world_view.grid)
        if target is None:
            self._avoid_immediate_collisiont(agent, world_view)
            return
        
        direction = self._greedy_direction_towards(agent, target, world_view.grid)
        agent.snake.set_direction(direction)

    def _avoid_immediate_collisiont(self, agent, world_view) -> None:
        grid = world_view.grid
        for direction in self._candidate_directions(agent.snake.direction):
            dx, dy = direction.delta()
            next_pos = grid.handle_toric(agent.snake.head[0] + dx, agent.snake.head[1] + dy)
            if not agent.snake.occupies(next_pos):
                agent.snake.set_direction(direction)
                return

    def _greedy_direction_towards(self, agent, target: tuple[int, int], grid) -> Direction:
        head_x, head_y = agent.snake.head
        best_direction = agent.snake.direction
        best_distance = grid.toric_distance(agent.snake.head, target)

        for direction in Direction:
            dx, dy = direction.delta()
            next_pos = grid.handle_toric(head_x + dx, head_y + dy)
            if agent.snake.occupies(next_pos):
                continue
            distance = grid.toric_distance(next_pos, target)
            if distance < best_distance:
                best_distance = distance
                best_direction = direction

        return best_direction

    def _candidate_directions(self, current: Direction) -> list[Direction]:
        return [current, current.turn_left(), current.turn_right()]
