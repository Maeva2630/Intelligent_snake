import pygame

from parser.parser import SnakeArgs, parse_args
from render.menu import Menu
from render.game import Game

def ouroboros(args: SnakeArgs):
    running_app = True
    skip_menu_once = args.skip_menu

    while running_app:

        if skip_menu_once:
            config = args.as_menu_config()
            skip_menu_once = False
        else:
            menu = Menu()
            menu_config = menu.run()

            if menu_config is None:
                running_app = False
                break

            config = menu_config

        tick_rate = args.tick_rate

        game = Game(
            grid_width=config["grid_width"],
            grid_height=config["grid_height"],
            food_density=config["food_density"],
            tick_rate=tick_rate
        )
        next_screen = game.run()

        if next_screen == "quit":
            running_app = False

    pygame.quit()

if __name__ == "__main__":
    args = parse_args()
    ouroboros(args)
