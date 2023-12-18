from typing import List
from unittest import TestCase

from main import DigPlan, read_from_file, get_dimensions, PARENT, dig, within


class Test(TestCase):

    def setUp(self):
        self.dig_plans: List[DigPlan] = read_from_file(PARENT.joinpath('example.txt'))
        self.terrain_map: dict[tuple[int, int], DigPlan] = dig(self.dig_plans)
        (x_max, y_max), (x_min, y_min) = get_dimensions(self.terrain_map)
        self.x_max = x_max
        self.y_max = y_max
        self.x_min = x_min
        self.y_min = y_min

    def test_within(self):
        self.assertTrue(
            within((0, 0), self.terrain_map, x_min=self.x_min),
            "(0,0)"
        )
        self.assertFalse(
            within((0, -9), self.terrain_map, x_min=self.x_min),
            "(0,-9)"
        )
        self.assertTrue(
            within((6, 0), self.terrain_map, x_min=self.x_min),
            "(6,0)"
        )
        self.assertTrue(
            within((6, -9), self.terrain_map, x_min=self.x_min),
            "(6,-9)"
        )

        self.assertFalse(
            within((0, -9), self.terrain_map, x_min=self.x_min),
            "(0,-9)"
        )

        self.assertTrue(
            within((2, -9), self.terrain_map, x_min=self.x_min),
            "(2,-8)"
        )
        self.assertTrue(
            within((5, -1), self.terrain_map, x_min=self.x_min),
            "(5,-1)"
        )
