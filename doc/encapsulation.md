# Encapsulation Architecture (Pygame)

To maintain a clean and modular codebase, **Ouroboros** strictly decouples its core game logic and states from the rendering details of the **Pygame** library. 

All direct interactions with Pygame are encapsulated within specific helper classes located in `game/encapsulation/`.

---

## 1. The Window (`Window`)
File: [game/encapsulation/window.py](file:///game/encapsulation/window.py)

The `Window` class manages Pygame screen surfaces, resizing events, and event loops.
* **Initialization**: Initializes the Pygame display and scales window dimensions.
* **Clock Ticks**: Standardizes the target framerate (60 FPS) and calculates the delta time (`dt`) for simulation physics.
* **Fullscreen**: Provides clean methods to toggle fullscreen mode without polluting the main game loop logic.

---

## 2. The Renderer (`Render`)
File: [game/encapsulation/render.py](file:///game/encapsulation/render.py)

The `Render` class abstracts all drawing and image assets handling operations. The main game loop never directly calls Pygame draw APIs.
* **Drawing Primitives**: Provides wrappers like `draw_rect`, `draw_circle`, `draw_line`, and `draw_text`.
* **Grid Rendering**: `draw_grid` renders the background grid cell borders.
* **Image Caching**: `load_image` caches loaded textures (logo, apples, snake sprites) in memory to avoid redundant disk I/O.
* **Screen Dimming**: `draw_dim_overlay` applies a semi-transparent colored filter over the window screen.

---

## 3. Events (`Event` and `Key`)
File: [game/encapsulation/event.py](file:///game/encapsulation/event.py)

This layer converts raw Pygame events into application-specific custom types.
* **Advantage**: If the project moves from Pygame to another graphics library (e.g., SDL, Arcade), the game event handling code does not need to be refactored.
* **Mapped Events**: Handles `EventType.QUIT`, `EventType.KEY_DOWN`, `EventType.MOUSE_CLICK` and maps keys such as `Key.ESCAPE`.

---

## 4. Geometric Utilities (`Rect`)
File: [game/encapsulation/rect.py](file:///game/encapsulation/rect.py)

A simple, lightweight rectangle structure (`x`, `y`, `width`, `height`) used primarily to configure button positions and dimensions for the user interfaces.

---

## 5. End Game Screen (`Screen`)
File: [game/render/screen.py](file:///game/render/screen.py)

To prevent cluttering the main `Game` engine, the graphics rendering of end game results (Victory or Draw screens) is delegated to the `Screen` class. It reads status variables from `Game` and uses the `Render` class to draw the appropriate text overlays.
