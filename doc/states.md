# FSM, Vision, and Memory of Agents

This section details the internal mechanics of the agent's brain (the AI snake), its forward-facing field of view, and its local memory management.

---

## 1. The Finite State Machine (FSM)

Each agent's decision logic is governed by a Finite State Machine ([AgentBrain](file:///game/snake/agent_brain.py)), defined by the `AgentState` enum:

* **`AgentState.EXPLORATION`** (Default State):
  * **Condition**: Activated when the agent has no known food locations saved in its memory.
  * **Behavior**: The agent attempts to move in a straight line. If the path directly ahead is clear, it continues forward.
* **`AgentState.DODGE`**:
  * **Condition**: Activated when the cell directly in front of the snake's head is blocked (by its own body or another snake), and it has no food targets in memory.
  * **Behavior**: The agent turns away, picking the first available free direction (left or right).
* **`AgentState.TARGET`**:
  * **Condition**: Activated as soon as the agent has at least one food coordinate stored in its memory.
  * **Behavior**: The agent computes the direction to approach the closest known food using toric distance and executes the corresponding turn action.

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
