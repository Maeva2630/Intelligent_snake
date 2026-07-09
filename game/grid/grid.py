""" Handle the toric (exiting via one edge causes an appearance on the other side)
    grid of the game (cells, state, positions) """

class Grid:
    def __init__(self, width: int, height: int):
        if width < 0 or height < 0:
            raise Exception(f"Grid dimensions can't be negatives: width={width}, height={height}.")

        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]

    def handle_toric(self, x: int, y: int) -> tuple[int, int]:
        return x % self.width, y % self.height

    def get(self, x: int, y: int) -> list[list[int]]:
        if x < 0 or y < 0:
            raise Exception(f"Grid coordinates can't be negatives: (x={x}, y={y}).")

        x, y = self.handle_toric(x, y)
        return self.grid[y][x]

    def set(self, x: int, y: int, value: int):
        x, y = self.handle_toric(x, y)
        self.grid[y][x] = value

    def toric_distance(self, p1: tuple[int, int], p2: tuple[int, int]) -> int:
        x1, y1 = p1
        x2, y2 = p2

        dx = abs(x1 - x2)
        dx = min(dx, self.width - dx)

        dy = abs(y1 - y2)
        dy = min(dy, self.height - dy)

        return dx + dy
