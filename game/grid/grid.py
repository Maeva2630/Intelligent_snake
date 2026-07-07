""" Handle the grid of the game (cells, state, positions)"""

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]

    def get(self, x, y):
        return self.grid[y][x]

    def set(self, x, y, value):
        self.grid[y][x] = value

