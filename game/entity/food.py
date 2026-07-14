from game.encapsulation.render import Render

class Food:
    def __init__(self, x: int, y: int, render: Render):
        self.x = x
        self.y = y
        self.live_length = 20

    def draw(self, render: Render):
        render.draw_circle(self.x, self.y, (255, 0, 0), render.tile_size // 2)

    
class FoodManager:
    def __init__(self, render: Render):
        self.render = render
        self.foods = []
        self.generate_food()
    
    def generate_food(self):
        self.foods.append(Food(self.render.screen_width // 2, self.render.screen_height // 2, self.render))

    def draw_foods(self):
        for food in self.foods:
            food.draw(self.render)

    def update(self, dt: float):
        for food in self.foods:
            food.live_length -= dt
            if food.live_length <= 0:
                self.foods.remove(food)
