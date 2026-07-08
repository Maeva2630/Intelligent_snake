import pygame
import game.grid.grid as grid

class Render:
    def __init__(self, screen, tile_size):
        self.screen = screen
        self.tile_size = tile_size
        self.grid = [[0 for _ in range(screen.get_width() // tile_size)] for _ in range(screen.get_height() // tile_size)]

    def draw_rect(self, x, y, color, size):
        pygame.draw.rect(self.screen, color, (x * size, y * size, size, size))

    def draw_circle(self, x, y, color, size):
        pygame.draw.circle(self.screen, color, (int(x * size + size / 2), int(y * size + size / 2)), int(size / 2))

    def draw_grid(self, grid):
        for x in range(grid.width):
            for y in range(grid.height):
                self.draw_rect(x, y, (255, 255, 255), self.tile_size)

    def draw_snake(self, snake):
        body = snake.get_body()
        n = len(body)
        if n == 0:
            return

        for i, segment in enumerate(body):
            t = i / (n - 1) if n > 1 else 1.0

            r = int(snake.color_tail[0] + (snake.color_head[0] - snake.color_tail[0]) * t)
            g = int(snake.color_tail[1] + (snake.color_head[1] - snake.color_tail[1]) * t)
            b = int(snake.color_tail[2] + (snake.color_head[2] - snake.color_tail[2]) * t)
            color = (r, g, b)

            factor = 0.6 + 0.4 * t
            size = int(self.tile_size * factor)

            offset = (self.tile_size - size) // 2
            x = segment.x * self.tile_size + offset
            y = segment.y * self.tile_size + offset

            center_x = x + size // 2
            center_y = y + size // 2
            radius = size // 2

            glow_color = (max(0, r - 40), max(0, g - 40), max(0, b - 40))
            pygame.draw.circle(self.screen, glow_color, (center_x, center_y), radius + 2)
            pygame.draw.circle(self.screen, color, (center_x, center_y), radius)

        head = snake.get_head()
        if head:
            hx = head.x * self.tile_size
            hy = head.y * self.tile_size
            cx = hx + self.tile_size // 2
            cy = hy + self.tile_size // 2

            eye_offset = self.tile_size // 5
            eye_radius = self.tile_size // 10
            direction = snake.direction.lower() if hasattr(snake, "direction") else "right"

            eye_map = {
                "right": ((1, -1), (1, 1)),
                "left": ((-1, -1), (-1, 1)),
                "up": ((-1, -1), (1, -1)),
                "down": ((-1, 1), (1, 1))
            }

            mult1, mult2 = eye_map.get(direction, ((1, -1), (1, 1)))
            eye1 = (cx + mult1[0] * eye_offset, cy + mult1[1] * eye_offset)
            eye2 = (cx + mult2[0] * eye_offset, cy + mult2[1] * eye_offset)

            pygame.draw.circle(self.screen, (255, 255, 255), eye1, eye_radius)
            pygame.draw.circle(self.screen, (255, 255, 255), eye2, eye_radius)

            pygame.draw.circle(self.screen, (0, 0, 0), eye1, max(1, eye_radius // 2))
            pygame.draw.circle(self.screen, (0, 0, 0), eye2, max(1, eye_radius // 2))


    def draw_food(self, food):
        self.draw_circle(food.x, food.y, food.color, 10)


    def render_scene(self, grid, foods, snakes):
        self.draw_grid(grid)

        for food in foods:
            self.draw_food(food)

        for snake in snakes:
            self.draw_snake(snake)

