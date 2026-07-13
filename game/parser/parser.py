
import argparse
from dataclasses import dataclass

from game.render.menu import MIN_AGENTS, MAX_AGENTS, MIN_FOOD_DENSITY, MAX_FOOD_DENSITY

_MIN_TICK_RATE = 1
_MAX_TICK_RATE = 60
_MIN_GRID_DIM = 4
_MAX_GRID_DIM = 200

_DEFAULT_FOOD_DENSITY = 0.05
_DEFAULT_NUM_AGENTS = MIN_AGENTS
_DEFAULT_TICK_RATE = 10
_DEFAULT_GRID = (32, 24)
_DEFAULT_FULLSCREEN = False

@dataclass
class SnakeArgs:
    food_density: float
    num_agents: int
    tick_rate: int
    grid_width: int
    grid_height: int
    fullscreen: bool
    skip_menu: bool

    @classmethod
    def from_argv(cls, argv: list[str] | None = None) -> "SnakeArgs":
        parser = cls._build_parser()
        namespace = parser.parse_args(argv)
        return cls._from_namespace(namespace, parser)

    @classmethod
    def _from_namespace(
        cls,
        args: argparse.Namespace,
        parser: argparse.ArgumentParser,
    ) -> "SnakeArgs":
        skip_menu = any(
            value is not None
            for value in (args.food, args.agent, args.tick, args.grid, args.fullscreen)
        )

        errors: list[str] = []

        food_density = args.food if args.food is not None else _DEFAULT_FOOD_DENSITY
        if not (MIN_FOOD_DENSITY <= food_density <= MAX_FOOD_DENSITY):
            errors.append(
                f"Invalid --food '{food_density}': must be between "
                f"{MIN_FOOD_DENSITY} and {MAX_FOOD_DENSITY}."
            )

        num_agents = args.agent if args.agent is not None else _DEFAULT_NUM_AGENTS
        if not (MIN_AGENTS <= num_agents <= MAX_AGENTS):
            errors.append(
                f"Invalid --agent '{num_agents}': must be between "
                f"{MIN_AGENTS} and {MAX_AGENTS}."
            )

        tick_rate = args.tick if args.tick is not None else _DEFAULT_TICK_RATE
        if not (_MIN_TICK_RATE <= tick_rate <= _MAX_TICK_RATE):
            errors.append(
                f"Invalid --tick '{tick_rate}': must be between "
                f"{_MIN_TICK_RATE} and {_MAX_TICK_RATE}."
            )

        if args.grid is not None:
            grid_width, grid_height = args.grid
        else:
            grid_width, grid_height = _DEFAULT_GRID
 
        for dim_name, dim_value in (("width", grid_width), ("height", grid_height)):
            if not (_MIN_GRID_DIM <= dim_value <= _MAX_GRID_DIM):
                errors.append(
                    f"Invalid --grid {dim_name} '{dim_value}': must be between "
                    f"{_MIN_GRID_DIM} and {_MAX_GRID_DIM}."
                )

        fullscreen = args.fullscreen if args.fullscreen is not None else _DEFAULT_FULLSCREEN

        if errors:
            parser.error("\n  ".join(errors))

        return cls(
            food_density=food_density,
            num_agents=num_agents,
            tick_rate=tick_rate,
            grid_width=grid_width,
            grid_height=grid_height,
            fullscreen=fullscreen,
            skip_menu=skip_menu,
        )

    # --- Factory --- #

    @staticmethod
    def _build_parser() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            prog="snake",
            description="Intelligent Snake - Edition Multi-Agents Competitive",
        )
        parser.add_argument(
            "--food",
            dest="food",
            type=float,
            default=None,
            metavar="density",
            help=f"Food spawn density, between {MIN_FOOD_DENSITY} and "
                 f"{MAX_FOOD_DENSITY} (default: {_DEFAULT_FOOD_DENSITY})",
        )
        parser.add_argument(
            "--agent",
            dest="agent",
            type=int,
            default=None,
            metavar="count",
            help=f"Number of competing AI snakes, between {MIN_AGENTS} and "
                 f"{MAX_AGENTS} (default: {_DEFAULT_NUM_AGENTS})",
        )
        parser.add_argument(
            "--tick",
            dest="tick",
            type=int,
            default=None,
            metavar="rate",
            help=f"Simulation ticks per second, between {_MIN_TICK_RATE} and "
                 f"{_MAX_TICK_RATE} (default: {_DEFAULT_TICK_RATE})",
        )
        parser.add_argument(
            "--grid",
            dest="grid",
            type=int,
            nargs=2,
            default=None,
            metavar=("width", "height"),
            help=f"Grid dimensions in cells, e.g. --grid 35 70 "
                 f"(default: {_DEFAULT_GRID[0]} {_DEFAULT_GRID[1]})",
        )
        parser.add_argument(
            "--fullscreen",
            dest="fullscreen",
            action="store_true",
            default=None,
            help="Launch directly in fullscreen mode",
        )
        return parser

    # --- Helpers --- #

    def as_menu_config(self) -> dict:
        return {
            "num_agents": self.num_agents,
            "grid_width": self.grid_width,
            "grid_height": self.grid_height,
            "food_density": self.food_density,
            "fullscreen": self.fullscreen,
        }

    def __str__(self) -> str:
        return (
            f"SnakeArgs(food_density={self.food_density}, "
            f"num_agents={self.num_agents}, tick_rate={self.tick_rate}, "
            f"grid={self.grid_width}x{self.grid_height}, fullscreen={self.fullscreen})"
        )

def parse_args(argv: list[str] | None = None) -> SnakeArgs:
    return SnakeArgs.from_argv(argv)
