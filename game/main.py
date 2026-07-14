
from game.render.menu import Menu
from game.render.game import Game
from game.parser.parser import SnakeArgs, parse_args
from game.encapsulation.window import Window

def ouroboros(args: SnakeArgs):
    running_app = True
    skip_menu_once = args.skip_menu
    window = Window(screen_width=640, screen_height=640, caption="Ouroboros")

    while running_app:

        if skip_menu_once:
            config = args.as_menu_config()
            skip_menu_once = False
        else:
            menu = Menu(window)
            menu_config = menu.run()

            if menu_config is None:
                running_app = False
                break

            config = menu_config

        tick_rate = args.tick_rate

        game = Game(window,
            grid_width=config["grid_width"],
            grid_height=config["grid_height"],
            food_density=config["food_density"],
            num_agents=config["num_agents"],
            tick_rate=tick_rate,
            fullscreen=config["fullscreen"],
        )
        next_screen = game.run()

        if next_screen == "quit":
            running_app = False

    window.quit()

if __name__ == "__main__":
    args = parse_args()
    ouroboros(args)
