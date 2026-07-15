from game.encapsulation.render import Render
import random

class Food:
    def __init__(self, x: int, y: int, render: Render):
        self.x = x
        self.y = y
        self.live_length = random.randint(60, 120)

    def draw(self, render: Render):
        apple_image = render.load_image("assets/entity/apple.png", (render.tile_size, render.tile_size))
        render.draw_image(apple_image, self.x * render.tile_size, self.y * render.tile_size)

    
class FoodManager:
    def __init__(self, render: Render, grid_size: tuple[int, int], food_density: float = 0.05):
        self.render = render
        self.foods = []
        self.grid_size = grid_size
        self.nb_foods = int(grid_size[0] * grid_size[1] * food_density)
        self.generate_food(initial=True)
    
    def generate_food(self, initial: bool = False):
        existing_positions = {(food.x, food.y) for food in self.foods}
        
        if initial:
            initial_target = max(1, self.nb_foods // 5)
            while len(self.foods) < initial_target:
                x = random.randint(0, self.grid_size[0] - 1)
                y = random.randint(0, self.grid_size[1] - 1)
                if (x, y) not in existing_positions:
                    self.foods.append(Food(x, y, self.render))
                    existing_positions.add((x, y))
        else:
            if len(self.foods) < self.nb_foods:
                if random.random() < 0.20:
                    x = random.randint(0, self.grid_size[0] - 1)
                    y = random.randint(0, self.grid_size[1] - 1)
                    if (x, y) not in existing_positions:
                        self.foods.append(Food(x, y, self.render))

    def draw_foods(self):
        for food in self.foods:
            food.draw(self.render)

    def update(self, food_density: float):
        self.nb_foods = int(self.grid_size[0] * self.grid_size[1] * food_density)
        for food in self.foods:
            food.live_length -= 1
        
        self.foods = [food for food in self.foods if food.live_length > 0]
        self.generate_food(initial=False)

    def eat_food(self, x: int, y: int):
        for food in self.foods:
            if food.x == x and food.y == y:
                self.foods.remove(food)
                return True
        return False

    def is_food_at(self, x: int, y: int):
        for food in self.foods:
            if food.x == x and food.y == y:
                return True
        return False
