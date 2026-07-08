"""Grid units test
Launch with: python -m pytest tests/grid/test_grid.py
"""

import pytest
from game.grid.grid import Grid


# Grids use for the tests
@pytest.fixture
def square_grid():
    return Grid(10, 10)

@pytest.fixture
def rect_grid():
    return Grid(32, 24)


def test_grid_initial_state_is_all_zero(square_grid):
    for x in range(square_grid.width):
        for y in range(square_grid.height):
            assert square_grid.get(x, y) == 0

def test_grid_dimensions_are_stored(rect_grid):
    assert rect_grid.width == 32
    assert rect_grid.height == 24

class TestHandleToric:
    def test_in_bounds_coordinates_are_unchanged(self, square_grid):
        assert square_grid.handle_toric(5, 5) == (5, 5)
        assert square_grid.handle_toric(0, 0) == (0, 0)

    def test_negative_x_wraps_to_right_edge(self, square_grid):
        assert square_grid.handle_toric(-1, 0) == (square_grid.width - 1, 0)

    def test_negative_y_wraps_to_bottom_edge(self, square_grid):
        assert square_grid.handle_toric(0, -1) == (0, square_grid.height - 1)

    def test_x_past_right_edge_wraps_to_left(self, square_grid):
        assert square_grid.handle_toric(square_grid.width, 0) == (0, 0)

    def test_y_past_bottom_edge_wraps_to_top(self, square_grid):
        assert square_grid.handle_toric(0, square_grid.height) == (0, 0)

    def test_wrap_on_rectangular_grid_uses_correct_axis(self, rect_grid):
        assert rect_grid.handle_toric(-1, 0) == (rect_grid.width - 1, 0)
        assert rect_grid.handle_toric(0, -1) == (0, rect_grid.height - 1)

class TestGetSet:
    def test_set_then_get_in_bounds(self, square_grid):
        square_grid.set(3, 4, 7)
        assert square_grid.get(3, 4) == 7

    def test_set_out_of_bounds_wraps_before_writing(self, square_grid):
        square_grid.set(-1, 0, 42)
        assert square_grid.get(square_grid.width - 1, 0) == 42

    def test_get_out_of_bounds_wraps_before_reading(self, square_grid):
        square_grid.set(0, 0, 99)
        assert square_grid.get(square_grid.width, square_grid.height) == 99

    def test_set_does_not_affect_neighboring_cells(self, square_grid):
        square_grid.set(2, 2, 1)
        assert square_grid.get(2, 3) == 0
        assert square_grid.get(3, 2) == 0

class TestToricDistance:
    def test_distance_to_self_is_zero(self, square_grid):
        assert square_grid.toric_distance((5, 5), (5, 5)) == 0

    def test_direct_distance_when_no_wrap_is_shorter(self, square_grid):
        assert square_grid.toric_distance((2, 2), (4, 2)) == 2

    def test_distance_wraps_around_x_edge_on_square_grid(self, square_grid):
        assert square_grid.toric_distance((0, 0), (9, 0)) == 1

    def test_distance_wraps_around_y_edge_on_square_grid(self, square_grid):
        assert square_grid.toric_distance((0, 0), (0, 9)) == 1

    def test_distance_is_symmetric(self, square_grid):
        a, b = (1, 2), (7, 8)
        assert square_grid.toric_distance(a, b) == square_grid.toric_distance(b, a)

    def test_distance_wraps_around_y_edge_on_rectangular_grid(self, rect_grid):
        assert rect_grid.toric_distance((0, 0), (0, 23)) == 1

    def test_vertical_wrap_uses_height_not_width(self, rect_grid):
        far_y = rect_grid.height // 2
        assert rect_grid.toric_distance((0, 0), (0, far_y)) == far_y
