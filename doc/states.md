# FSM, Vision, and Memory of Agents

This section details the internal mechanics of the agent's brain (the AI snake), its forward-facing field of view, and its local memory management.

---

## 1. The Finite State Machine (FSM)

Each agent's decision logic is governed by a Finite State Machine ([AgentBrain](file:///game/snake/agent_brain.py)), defined by the `AgentState` enum:

* **`AgentState.HUNTING`** (highest priority):
  * **Condition**: activated as soon as another alive snake occupies a cell inside the agent's vision cone, or the agent recently locked onto one (see section 4 for the commit/cooldown details). This overrides everything else.
  * **Behavior**: pursues, cuts off, or encircles the target depending on distance — full breakdown in section 4.
* **`AgentState.TARGET`**:
  * **Condition**: activated when there is no threat to hunt, and the agent has at least one food coordinate stored in its memory.
  * **Behavior**: The agent computes the direction to approach the closest known food using toric distance and executes the corresponding turn action.
* **`AgentState.DODGE`**:
  * **Condition**: activated when there is nothing to hunt or eat, and the cell directly in front of the snake's head is blocked (by another snake — the agent's own body no longer counts as blocking, see section 5.5).
  * **Behavior**: The agent turns away, picking the first available free direction (left or right).
* **`AgentState.EXPLORATION`** (default / fallback state):
  * **Condition**: activated when none of the states above apply — nothing to hunt, nothing to eat, and the path ahead is clear.
  * **Behavior**: The agent continues moving in a straight line.

---

## 2. Forward-Facing Vision Cone

Each snake has a restricted field of view pointing forward in its direction of movement.

* **Geometry**: It is a **vision cone (or triangle)**:
  * **Depth**: Configured by `vision_radius` (default: 5 cells).
  * **Width**: Grows wider as distance increases:
    * At distance 1 (directly in front): 1 cell wide (the center cell).
    * At distance 2: 3 cells wide (center cell + 1 left + 1 right).
    * At distance 3: 5 cells wide, and so on.
* **Detection**: Each tick, the agent scans these cells and classifies what it sees:
  * Food (`"food"`)
  * Other alive snakes (`"agent"`)
  * Its own body (`"self"`)
  * Empty cells (`"empty"`)
* **Visual Overlay**: This field of view is drawn on the screen as a translucent colored layer (matching the agent's color).

---

## 3. Local Memory (`AgentMemory`)

Since vision is limited, the snake uses a local memory ([AgentMemory](file:///game/snake/agent_memory.py)) to store what it has seen:

* **Remembering**: Whenever an apple enters the vision cone, its coordinate and the current game tick are saved.
* **Targeting**: The FSM's `TARGET` state queries memory to find the closest known apple.
* **Forgetting**:
  * When a snake eats a known apple, it deletes it from its memory.
  * *Note*: The memory does not store other snakes' positions because they move dynamically. Instead, they are handled as real-time obstacles during immediate collision checks.

---

## 5. Design Journey: Why `HUNTING` Looks the Way It Does

The naive version of `HUNTING` did not work, and each fix uncovered a new,
more subtle failure mode. This section documents that process, since the
project brief specifically asks for the limits and reasoning behind the
FSM, not just its final shape.

### 5.1 — Naive pursuit doesn't catch an equal-speed target

*First attempt*: move toward the target's current head position each tick.
*Result*: this only ever chases from behind. If the prey already runs
directly away from the hunter, both move at the same speed, so the gap
never closes - a mathematical property of equal-speed pursuit, not a bug.

*Fix attempt*: aim at a point a few cells **ahead** of the prey, along its
current heading, instead of its current position (`HUNTING_LOOKAHEAD`).
This helps whenever the two paths actually converge, but does nothing for
the exact "running away in a straight line" case above - the aim point
moves away exactly as fast as the hunter approaches it.

### 5.2 — Stalled pursuit: flanking around the toric world

Since the map wraps around, a stalled head-on chase can be turned into a
closing one by reversing direction: the hunter now approaches from the
*other* side of the world, so instead of matching the prey's speed, the
two close the gap **toward each other** (twice the effective closing
speed). This is `_start_flank` / `_continue_flank`, triggered by
`HUNTING_STALL_THRESHOLD`.

### 5.3 — Two identical hunters can freeze each other

Once both snakes can hunt each other, two problems appeared that pure
logic review did not catch - only running long simulations did:

* **Symmetric flank lock**: the forced U-turn always tried "right" first,
  deterministically. Two identical agents in a mirrored configuration
  reproduced the *exact* same stalemate every cycle, forever. Fixed by
  shuffling the turn order randomly per attempt (`_forced_turn`), and by
  adding the `HUNTING_GIVE_UP_TICKS` / cooldown safety net so that even an
  undiscovered deadlock pattern cannot loop indefinitely.
* **Frozen orbit**: the first version of `_encircle_point` computed the
  orbit target by rotating the hunter's *current* relative offset from the
  prey by 90°. If both snakes ended up moving in perfect parallel (offset
  never changing tick to tick), the computed target never changed either —
  the two would cruise together indefinitely instead of orbiting. Fixed by
  making the orbit angle advance by a fixed step every tick
  (`ENCIRCLE_ANGULAR_STEP`), independent of the current geometry — it can
  no longer get stuck at a fixed point.

![dance](snake/agents_dance.mp4)

### 5.4 — Priority order silently disabled hunting

For a long stretch of testing, agents seemed to "never" hunt, even with an
opponent right next to them. Cause: known food was checked *before* the
visible-threat check in `_update_state`. Since food constantly respawns,
an agent almost always had at least one apple in memory, so `TARGET`
permanently won the priority check and `HUNTING` was never reached in
practice — the code was correct, it was simply unreachable. Swapping the
order (visible threat checked first) fixed it immediately.

### Known remaining limitation

`HUNTING`, like `TARGET`, still only looks one step ahead when choosing a
direction (`_turn_towards`). It cannot plan a route the way a real
pathfinding algorithm (A\*) would, and can in principle still walk itself
into a dead end that a deeper search would have avoided. This is the main
documented limitation of the current decision system, and the natural next
step if the project continues beyond this iteration.
