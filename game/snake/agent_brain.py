""" Agent Brain: FSM, decision logic  """

from enum import Enum

LOW_ERNGY = 30

_STRAIGHT = "straight"
_LEFT = "left"
_RIGHT = "right"

class AgentState(Enum):
    EXPLORATION = "exploration"
    TARGET = "target"
    DODGE = "dodge"

class AgentBrain:
    def __init__(self):
        self.current_state = AgentState.EXPLORATION

    def decide(self, agent, world_view) -> None:
        self._update_state(agent, world_view)

        if self.current_state == AgentState.TARGET:
            self._move_towards_known_food(agent, world_view)
        else:
            self._avoid_immediate_collisiont(agent, world_view)

    def _update_state(self, agent, world_view) -> None:
        if agent.memory.known_resources():
            self.current_state = AgentState.TARGET_ACQUIRED
            return

        straight_pos = self._next_position(agent, agent.snake.direction, world_view.grid)
        if self._is_blocked(agent, straight_pos, world_view):
            self.current_state = AgentState.DODGE
        else:
            self.current_state = AgentState.EXPLORATION

    def _move_towards_known_food(self, agent, world_view) -> None:
        target = agent.memory.closest_known_resource(agent.snake.head, world_view.grid)
        if target is None:
            self._avoid_immediate_collisiont(agent, world_view)
            return
        
        self._turn_towards(agent, target, world_view.grid)

    def _turn_towards(self, agent, target: tuple[int, int], grid) -> None:
        best_action = None
        best_distance = None

        for action, direction in self._reachable_directions(agent.snake.direction):
            dx, dy = direction.delta()
            next_pos = grid.handle_toric(agent.snake.head[0] + dx, agent.snake.head[1] + dy)
            if agent.snake.occupies(next_pos):
                continue

            distance = grid.toric_distance(next_pos, target)
            if best_distance is None or distance < best_distance:
                best_distance = distance
                best_action = action

        self._apply_action(agent, best_action)

    def _avoid_immediate_collisiont(self, agent, world_view) -> None:
        for action, direction in self._reachable_directions(agent.snake.direction):
            next_pos = self._next_position(agent, direction, world_view.grid)
            if not self._is_blocked(agent, next_pos, world_view):
                self._apply_action(agent, action)
                return

    def _is_blocked(self, agent, position: tuple[int, int], world_view) -> bool:
        if agent.snake.occupies(position):
            return True

        return any(
            other.alive and other.snake.occupies(position)
            for other in world_view.other_agents
        )

    def _next_position(self, agent, direction, grid) -> tuple[int, int]:
        dx, dy = direction.delta()
        return grid.handle_toric(agent.snake.head[0] + dx, agent.snake.head[1] + dy)

    def _reachable_directions(self, current):
        return [
            (_STRAIGHT, current),
            (_LEFT, current.turn_left()),
            (_RIGHT, current.turn_right()),
        ]

    def _apply_action(self, agent, action: str | None) -> None:
        if action == _LEFT:
            agent.snake.turn_left()
        elif action == _RIGHT:
            agent.snake.turn_right()
