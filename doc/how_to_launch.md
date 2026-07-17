# How to Launch Our Game

This document explains how to set up, build, and run the **Ouroboros** application, either using the settings interface or via command-line arguments.

---

## 1. Running the Game

### Prerequisites
Make sure you have Python 3.10+ installed.

1. **Create and activate the virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. **Install requirements**:
   ```bash
   pip install -r requirement.txt
   ```
3. **Compile and run the executable**:
   We use PyInstaller to compile the source code into a standalone binary:
   ```bash
   make re
   ./ouroboros
   ```

---

## 2. Using the User Interface (Settings Menu)

When launched without arguments, the game opens the **Settings Menu**:
- **Number of AIs**: Configure the amount of competing snakes (from 2 to 4).
- **Grid Size**: Cycle through three presets:
  - **Small** (16x12 cells)
  - **Medium** (32x24 cells)
  - **Big** (48x36 cells)
- **Food Density**: Control the density of food spawns (percentage of cells containing food).
- **Fullscreen**: Toggle fullscreen mode.

Click **Start** to begin the simulation. Press **ESC** or click **Back to menu** at any time to return to the menu settings.

---

## 3. Launching via Command-Line (Skip Menu)

You can launch the game directly with customized settings and bypass the main menu completely by passing command-line arguments to the executable or script:

```bash
./ouroboros --agent 3 --food 0.08 --grid 35 25 --tick 15 --fullscreen
```

### Supported Arguments Reference

| Argument | Description | Allowed Range | Default Value |
| :--- | :--- | :--- | :--- |
| `--agent count` | Number of competing AI snakes | `2` to `4` | `2` |
| `--food density` | Density of food spawning on the grid | `0.01` to `2.00` | `0.05` |
| `--tick rate` | Speed of the simulation (ticks/second) | `1` to `60` | `10` |
| `--grid W H` | Custom grid dimensions in cell units | `4` to `200` | `32 24` |
| `--fullscreen` | Start directly in fullscreen mode | *N/A* | `False` |

*Note: Specifying any of the arguments above will automatically activate the `skip_menu` flag, sending you directly into the gameplay screen.*
