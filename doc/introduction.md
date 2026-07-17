# Ouroboros - Intelligent Snake

Welcome to the documentation of **Ouroboros**, a real-time competitive multi-agent simulation of autonomous intelligent snakes.

## General Game Concept

**Ouroboros** is an advanced, competitive evolution of the classic Snake game. Instead of a human player controlling a single snake, the game simulates autonomous intelligent agents (AIs) driven by Finite State Machines (FSM) moving on a toric grid.

### Toric Grid (Pac-man Effect)
The game board is a **toric** grid: exiting from one side of the screen instantly teleports the snake to the opposite side (similar to Pac-man). This toric geometry applies to snake movement, shortest-path calculations to reach food, and collision risk assessments.

---

## Competitive Mode (Battle Royale)

The game operates as a survival tournament:
* **Number of AIs**: 2 to 4 snakes compete simultaneously in the arena.
* **Objective**: Be the last surviving snake.
* **Loss Conditions**:
  * If a snake collides with its own body, it dies.
  * If a snake's head collides with another snake's body, it dies.
* **Victory**: As soon as only one surviving snake remains, the game pauses and displays a victory overlay celebrating the winning AI (rendered in its color). If the last two snakes crash at the exact same tick, a "No Winner" game over screen is shown.

---

## Food System

* **Spawn**: Managed by the `FoodManager` class in `game/entity/food.py`. Apples spawn randomly across the map based on a configured density.
* **Lifespan**: Each apple has a limited lifespan (`live_length`). If not eaten after a certain number of ticks, it disappears and a new apple spawns elsewhere.
* **Consumption and Growth**: When a snake passes its head over an apple, the apple is removed from the grid, the snake grows by one segment (`agent.snake.grow()`), and the resource coordinate is cleared from the agent's memory.
