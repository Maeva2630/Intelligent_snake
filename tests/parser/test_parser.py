"""Parser units test
Launch with: python -m pytest tests/parser/test_parser.py
"""

import pytest

from game.parser.parser import parse_args
from game.render.menu import MIN_AGENTS, MAX_AGENTS, MIN_FOOD_DENSITY, MAX_FOOD_DENSITY

class TestDefaults:
    def test_no_args_uses_defaults(self):
        args = parse_args([])
        assert args.food_density == 0.05
        assert args.num_agents == MIN_AGENTS
        assert args.tick_rate == 10
        assert (args.grid_width, args.grid_height) == (32, 24)

    def test_no_args_does_not_skip_menu(self):
        args = parse_args([])
        assert args.skip_menu is False

class TestParsingValidValues:
    def test_food_is_parsed_as_float(self):
        args = parse_args(["--food", "0.03"])
        assert args.food_density == pytest.approx(0.03)

    def test_agent_is_parsed_as_int(self):
        args = parse_args(["--agent", "3"])
        assert args.num_agents == 3

    def test_tick_is_parsed_as_int(self):
        args = parse_args(["--tick", "20"])
        assert args.tick_rate == 20

    def test_grid_is_parsed_as_two_ints(self):
        args = parse_args(["--grid", "35", "70"])
        assert (args.grid_width, args.grid_height) == (35, 70)

    def test_all_args_combined(self):
        args = parse_args(
            ["--food", "0.03", "--agent", "3", "--tick", "20", "--grid", "35", "70"]
        )
        assert args.food_density == pytest.approx(0.03)
        assert args.num_agents == 3
        assert args.tick_rate == 20
        assert (args.grid_width, args.grid_height) == (35, 70)
        assert args.skip_menu is True

class TestSkipMenuDetection:
    @pytest.mark.parametrize(
        "argv",
        [
            ["--food", "0.05"],
            ["--agent", "2"],
            ["--tick", "10"],
            ["--grid", "32", "24"],
        ],
    )
    def test_any_single_arg_triggers_skip_menu(self, argv):
        args = parse_args(argv)
        assert args.skip_menu is True

    def test_no_arg_does_not_trigger_skip_menu(self):
        args = parse_args([])
        assert args.skip_menu is False

class TestFoodValidation:
    def test_food_at_lower_bound_is_valid(self):
        args = parse_args(["--food", str(MIN_FOOD_DENSITY)])
        assert args.food_density == pytest.approx(MIN_FOOD_DENSITY)

    def test_food_at_upper_bound_is_valid(self):
        args = parse_args(["--food", str(MAX_FOOD_DENSITY)])
        assert args.food_density == pytest.approx(MAX_FOOD_DENSITY)

    def test_food_below_lower_bound_raises(self, capsys):
        with pytest.raises(SystemExit):
            parse_args(["--food", "0.0"])
        assert "--food" in capsys.readouterr().err

    def test_food_above_upper_bound_raises(self, capsys):
        with pytest.raises(SystemExit):
            parse_args(["--food", "2.01"])
        assert "--food" in capsys.readouterr().err

class TestAgentValidation:
    def test_agent_at_lower_bound_is_valid(self):
        args = parse_args(["--agent", str(MIN_AGENTS)])
        assert args.num_agents == MIN_AGENTS

    def test_agent_at_upper_bound_is_valid(self):
        args = parse_args(["--agent", str(MAX_AGENTS)])
        assert args.num_agents == MAX_AGENTS

    def test_agent_below_lower_bound_raises(self, capsys):
        with pytest.raises(SystemExit):
            parse_args(["--agent", "1"])
        assert "--agent" in capsys.readouterr().err

    def test_agent_above_upper_bound_raises(self, capsys):
        with pytest.raises(SystemExit):
            parse_args(["--agent", "999"])
        assert "--agent" in capsys.readouterr().err

class TestTickValidation:
    def test_tick_at_lower_bound_is_valid(self):
        args = parse_args(["--tick", "1"])
        assert args.tick_rate == 1

    def test_tick_at_upper_bound_is_valid(self):
        args = parse_args(["--tick", "60"])
        assert args.tick_rate == 60

    def test_tick_below_lower_bound_raises(self, capsys):
        with pytest.raises(SystemExit):
            parse_args(["--tick", "0"])
        assert "--tick" in capsys.readouterr().err

    def test_tick_above_upper_bound_raises(self, capsys):
        with pytest.raises(SystemExit):
            parse_args(["--tick", "61"])
        assert "--tick" in capsys.readouterr().err

class TestGridValidation:
    def test_grid_within_bounds_is_valid(self):
        args = parse_args(["--grid", "10", "10"])
        assert (args.grid_width, args.grid_height) == (10, 10)

    def test_grid_width_too_small_raises(self, capsys):
        with pytest.raises(SystemExit):
            parse_args(["--grid", "1", "24"])
        assert "--grid" in capsys.readouterr().err

    def test_grid_height_too_large_raises(self, capsys):
        with pytest.raises(SystemExit):
            parse_args(["--grid", "32", "1000"])
        assert "--grid" in capsys.readouterr().err

    def test_grid_requires_exactly_two_values(self):
        with pytest.raises(SystemExit):
            parse_args(["--grid", "32"])

class TestMultipleErrors:
    def test_multiple_invalid_args_are_all_reported(self, capsys):
        with pytest.raises(SystemExit):
            parse_args(["--food", "0.99", "--agent", "999"])
        err = capsys.readouterr().err
        assert "--food" in err
        assert "--agent" in err

class TestInvalidTypes:
    def test_non_numeric_food_raises(self):
        with pytest.raises(SystemExit):
            parse_args(["--food", "beaucoup"])

    def test_non_numeric_grid_raises(self):
        with pytest.raises(SystemExit):
            parse_args(["--grid", "large", "24"])

class TestAsMenuConfig:
    def test_as_menu_config_has_expected_keys(self):
        args = parse_args(["--food", "0.1", "--agent", "3", "--grid", "20", "15"])
        config = args.as_menu_config()
        assert set(config.keys()) == {
            "num_agents", "grid_width", "grid_height", "food_density"
        }

    def test_as_menu_config_values_match_args(self):
        args = parse_args(["--food", "0.1", "--agent", "3", "--grid", "20", "15"])
        config = args.as_menu_config()
        assert config["num_agents"] == 3
        assert config["grid_width"] == 20
        assert config["grid_height"] == 15
        assert config["food_density"] == pytest.approx(0.1)

def test_str_representation_contains_values():
    args = parse_args(["--agent", "3"])
    text = str(args)
    assert "num_agents=3" in text
