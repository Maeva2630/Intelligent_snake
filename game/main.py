import pygame

from render.menu import Menu
from render.game import Game


def main():
    running_app = True
 
    while running_app:
        menu = Menu()
        config = menu.run()
 
        if config is None:
            running_app = False
            break
 
        game = Game(
            grid_width=config["grid_width"],
            grid_height=config["grid_height"],
            food_density=config["food_density"],
        )
        next_screen = game.run()
 
        if next_screen == "quit":
            running_app = False
 
    pygame.quit()

if __name__ == "__main__":
    main()
