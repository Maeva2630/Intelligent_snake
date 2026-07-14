from game.encapsulation.render import Render
import random

class Food:
    def __init__(self, x: int, y: int, render: Render):
        self.x = x
        self.y = y
        self.live_length = 50

    def draw(self, render: Render):
        render.draw_circle(self.x, self.y, (255, 0, 0), render.tile_size)

    
class FoodManager:
    def __init__(self, render: Render, grid_size: tuple[int, int], food_density: float = 0.05):
        self.render = render
        self.foods = []
        self.grid_size = grid_size
        self.nb_foods = int(grid_size[0] * grid_size[1] * food_density)
        self.generate_food()
    
    def generate_food(self):
        existing_positions = {(food.x, food.y) for food in self.foods}
        while len(self.foods) < self.nb_foods:
            x = random.randint(0, self.grid_size[0] - 1)
            y = random.randint(0, self.grid_size[1] - 1)
            if (x, y) not in existing_positions:
                self.foods.append(Food(x, y, self.render))
                existing_positions.add((x, y))

    def draw_foods(self):
        for food in self.foods:
            food.draw(self.render)

    def update(self):
        for food in self.foods:
            food.live_length -= 1
        
        self.foods = [food for food in self.foods if food.live_length > 0]
        self.generate_food()

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

