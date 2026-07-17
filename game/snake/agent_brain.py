""" Agent Brain: FSM, decision logic  """

import math
import random
from game.snake.world_view import WorldView
from enum import Enum

_STRAIGHT = "straight"
_LEFT = "left"
_RIGHT = "right"

HUNTING_LOOKAHEAD = 3
HUNTING_MAX_LOOKAHEAD = 8
HUNTING_NOISE_CHANCE = 0.15
HUNTING_STALL_THRESHOLD = 3
HUNTING_COMMIT_TICKS = 15
HUNTING_FLANK_TICKS = 12
HUNTING_GIVE_UP_TICKS = 60
HUNTING_COOLDOWN_TICKS = 30
HUNTING_SIZE_TOLERANCE = 3

ENCIRCLE_TRIGGER_DISTANCE = 6
ENCIRCLE_RADIUS = 3
ENCIRCLE_ANGULAR_STEP = 0.35

class AgentState(Enum):
    EXPLORATION = "exploration"
    TARGET = "target"
    DODGE = "dodge"
    HUNTING = "hunting"

class AgentBrain:
    def __init__(self):
        self.current_state = AgentState.EXPLORATION
        self._last_hunt_distance: int | None = None
        self._hunt_stall_ticks = 0
        self._hunt_target = None
        self._hunt_target_last_seen_tick: int | None = None

        self._flank_ticks_remaining = 0
        self._flank_turns_remaining = 0

        self._hunt_engaged_since_tick: int | None = None
        self._hunt_cooldown: dict[int, int] = {}

        self._encircle_phase = 0.0

    def decide(self, agent, world_view) -> None:
        self._update_state(agent, world_view)

        if self.current_state == AgentState.TARGET:
            self._move_towards_known_food(agent, world_view)
        elif self.current_state == AgentState.HUNTING:
            self._move_towards_hunt(agent, world_view)
        else:
            self._avoid_immediate_collisiont(agent, world_view)

    def _update_state(self, agent, world_view) -> None:
        visible_threat = self._nearest_visible_threat(agent, world_view)
        if visible_threat is not None:
            if self._hunt_target is not visible_threat:
                self._hunt_engaged_since_tick = world_view.tick
            self._hunt_target = visible_threat
            self._hunt_target_last_seen_tick = world_view.tick

            if self._give_up_if_stuck(agent, world_view):
                self.current_state = AgentState.EXPLORATION
                return

            self.current_state = AgentState.HUNTING
            return

        if (self._hunt_target is not None and self._hunt_target.alive
            and world_view.tick - self._hunt_target_last_seen_tick <= HUNTING_COMMIT_TICKS):
            if self._give_up_if_stuck(agent, world_view):
                self.current_state = AgentState.EXPLORATION
                return
            self.current_state = AgentState.HUNTING
            return
        self._hunt_target = None
        self._hunt_engaged_since_tick = None

        if agent.memory.known_resources():
            self.current_state = AgentState.TARGET
            return

        straight_pos = self._next_position(agent, agent.snake.direction, world_view.grid)
        if self._is_blocked(straight_pos, world_view):
            self.current_state = AgentState.DODGE
        else:
            self.current_state = AgentState.EXPLORATION

    def _give_up_if_stuck(self, agent, world_view) -> bool:
        if self._hunt_engaged_since_tick is None:
            return False

        engaged_ticks = world_view.tick - self._hunt_engaged_since_tick
        if engaged_ticks < HUNTING_GIVE_UP_TICKS:
            return False

        if self._hunt_target is not None:
            self._hunt_cooldown[id(self._hunt_target)] = world_view.tick + HUNTING_COOLDOWN_TICKS

        self._hunt_target = None
        self._hunt_engaged_since_tick = None
        self._last_hunt_distance = None
        self._hunt_stall_ticks = 0
        self._flank_ticks_remaining = 0
        return True

    def _nearest_visible_threat(self, agent, world_view):
        visible_positions = {
            pos for pos, content in agent.last_visible_cells.items()
            if content == "agent"
        }

        if not visible_positions:
            return None

        grid = world_view.grid
        candidates = []
 
        for other in world_view.other_agents:
            if not other.alive:
                continue
 
            cooldown_until = self._hunt_cooldown.get(id(other))
            if cooldown_until is not None and world_view.tick < cooldown_until:
                continue
 
            if not any(other.snake.occupies(pos) for pos in visible_positions):
                continue
 
            candidates.append(other)
 
        if not candidates:
            return None
 
        reasonable = [c for c in candidates if c.length <= agent.length + HUNTING_SIZE_TOLERANCE]
        pool = reasonable if reasonable else candidates
 
        return min(pool, key=lambda other: grid.toric_distance(agent.snake.head, other.snake.head))

    def _move_towards_known_food(self, agent, world_view) -> None:
        target = agent.memory.closest_known_resource(agent.snake.head, world_view.grid)
        if target is None:
            self._avoid_immediate_collisiont(agent, world_view)
            return

        self._turn_towards(agent, target, world_view)

    def _encircle_point(self, agent, prey, grid) -> tuple[int, int]:
        self._encircle_phase = (self._encircle_phase + ENCIRCLE_ANGULAR_STEP) % (2 * math.pi)

        px, py = prey.snake.head
        target_ox = round(ENCIRCLE_RADIUS * math.cos(self._encircle_phase))
        target_oy = round(ENCIRCLE_RADIUS * math.sin(self._encircle_phase))

        return grid.handle_toric(px + target_ox, py + target_oy)

    def _find_cutoff_point(self, agent, prey, grid) -> tuple[int, int] | None:
        px, py = prey.snake.head
        dx, dy = prey.snake.direction.delta()
        point = (px, py)

        for prey_ticks in range(1, HUNTING_MAX_LOOKAHEAD + 1):
            point = grid.handle_toric(point[0] + dx, point[1] + dy)
            hunter_distance = grid.toric_distance(agent.snake.head, point)
            hunter_ticks_needed = -(-hunter_distance // 2)
            if hunter_ticks_needed <= prey_ticks:
                return point

        return None

    def _move_towards_hunt(self, agent, world_view) -> None:
        prey = self._hunt_target
        if prey is None or not prey.alive:
            self._avoid_immediate_collisiont(agent, world_view)
            self._last_hunt_distance = None
            self._hunt_stall_ticks = 0
            self._flank_ticks_remaining = 0
            return

        grid = world_view.grid
        current_distance = grid.toric_distance(agent.snake.head, prey.snake.head)

        if current_distance <= ENCIRCLE_TRIGGER_DISTANCE:
            self._flank_ticks_remaining = 0
            self._hunt_stall_ticks = 0
            self._last_hunt_distance = None
            encircle_target = self._encircle_point(agent, prey, grid)
            self._turn_towards(agent, encircle_target, world_view)
            return

        if self._flank_ticks_remaining > 0:
            self._continue_flank(agent, world_view)
            return

        if self._last_hunt_distance is not None and current_distance >= self._last_hunt_distance:
            self._hunt_stall_ticks += 1
        else:
            self._hunt_stall_ticks = 0
        self._last_hunt_distance = current_distance

        if self._hunt_stall_ticks >= HUNTING_STALL_THRESHOLD:
            self._start_flank(agent, world_view)
            return

        cutoff = self._find_cutoff_point(agent, prey, grid)
        if cutoff is not None:
            self._turn_towards(agent, cutoff, world_view)
        else:
            px, py = prey.snake.head
            dx, dy = prey.snake.direction.delta()
            intercept = px, py
            for _ in range(HUNTING_LOOKAHEAD):
                intercept = grid.handle_toric(intercept[0] + dx, intercept[1] + dy)
            self._turn_towards(agent, intercept, world_view)

    def _start_flank(self, agent, world_view) -> None:
        self._flank_ticks_remaining = HUNTING_FLANK_TICKS
        self._flank_turns_remaining = 2
        self._hunt_stall_ticks = 0
        self._continue_flank(agent, world_view)

    def _continue_flank(self, agent, world_view) -> None:
        self._flank_ticks_remaining -= 1

        if self._flank_turns_remaining > 0:
            if self._forced_turn(agent, world_view):
                self._flank_turns_remaining -= 1
            self._avoid_immediate_collisiont(agent, world_view)
        else:
            self._avoid_immediate_collisiont(agent, world_view)

    def _forced_turn(self, agent, world_view) -> bool:
        grid = world_view.grid
        sides = [agent.snake.direction.turn_right, agent.snake.direction.turn_left]
        random.shuffle(sides)

        for turn in sides:
            candidate_direction = turn()
            candidate_pos = self._next_position(agent, candidate_direction, grid)
            if not self._is_blocked(candidate_pos, world_view):
                agent.snake.direction = candidate_direction
                return True

        return False

    def _self_occupied(self, agent, position: tuple[int, int]) -> bool:
        if not agent.snake.occupies(position):
            return False
        if position == agent.snake.tail and agent.snake.will_vacate_tail():
            return False
        return True

    def _turn_towards(self, agent, target: tuple[int, int], world_view: WorldView, distance_fn = None) -> None:
        grid = world_view.grid
        if distance_fn is None:
            distance_fn = lambda g, a, b: g.toric_distance(a, b)

        survivable = []
        for action, direction in self._reachable_directions(agent.snake.direction):
            next_pos = self._next_position(agent, direction, grid)
            if self._is_blocked(next_pos, world_view):
                continue
            survivable.append((action, next_pos, self._self_occupied(agent, next_pos)))
 
        if not survivable:
            self._avoid_immediate_collisiont(agent, world_view)
            return

        free = [c for c in survivable if not c[2]]
        pool = free if free else survivable

        best_action = None
        best_distance = None
        for action, next_pos, _ in pool:
            distance = distance_fn(grid, next_pos, target)
            if best_distance is None or distance < best_distance:
                best_distance = distance
                best_action = action

        self._apply_action(agent, best_action)

    def _avoid_immediate_collisiont(self, agent, world_view) -> None:
        grid = world_view.grid
        survivable = []
        for action, direction in self._reachable_directions(agent.snake.direction):
            next_pos = self._next_position(agent, direction, grid)
            if self._is_blocked(next_pos, world_view):
                continue
            survivable.append((action, self._self_occupied(agent, next_pos)))
 
        if not survivable:
            agent.snake.die()
            return

        for action, self_occupied in survivable:
            if not self_occupied:
                self._apply_action(agent, action)
                return

        self._apply_action(agent, survivable[0][0])

    def _is_blocked(self, position: tuple[int, int], world_view) -> bool:
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
