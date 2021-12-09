#!/bin/python

from dataclasses import dataclass
from typing import Dict, List, Set


@dataclass
class Point(object):
    x: int
    y: int
    value: int

    def is_next_to(self, point) -> bool:
        if abs(self.x - point.x) <= 1 and abs(self.y - point.y) <= 1:
            return True
        else:
            return False


def find_low_points(lines: List[List[int]]) -> List[Point]:
    low_points: List[Point] = []

    for i in range(len(lines)):
        for j in range(len(lines[i])):
            current_height: int = lines[i][j]

            if (i - 1 < 0 or lines[i - 1][j] > current_height) \
                    and (j - 1 < 0 or lines[i][j - 1] > current_height) \
                    and (i + 1 >= len(lines) or lines[i + 1][j] > current_height) \
                    and (j + 1 >= len(lines[i]) or lines[i][j + 1] > current_height):
                low_points.append(Point(x=j, y=i, value=current_height))

    return low_points


def part_one(lines: List[List[int]]) -> int:
    low_points = find_low_points(lines)
    return sum(
        [x.value + 1 for x in low_points]
        )


def find_next_points(heigh_map: List[List[int]], point: Point, been_points: List[Point] = []) -> List[Point]:
    if point in been_points:
        return []

    been_points.append(point)

    points: List[Point] = [point]

    #   Up
    if point.y + 1 < len(heigh_map) and heigh_map[point.y + 1][point.x] < 9:
        points.extend(
            find_next_points(
                heigh_map,
                point=Point(x=point.x, y=point.y + 1, value=point.value),
                been_points=been_points
            )
        )
    #   Down
    if point.y - 1 >= 0 and heigh_map[point.y - 1][point.x] < 9:
        points.extend(
            find_next_points(
                heigh_map,
                point=Point(x=point.x, y=point.y - 1, value=point.value),
                been_points=been_points
            )
        )
    #   Left
    if point.x - 1 >= 0 and heigh_map[point.y][point.x - 1] < 9:
        points.extend(
            find_next_points(
                heigh_map,
                point=Point(x=point.x - 1, y=point.y, value=point.value),
                been_points=been_points
            )
        )
    #   Right
    if point.x + 1 < len(heigh_map[point.y]) and heigh_map[point.y][point.x + 1] < 9:
        points.extend(
            find_next_points(
                heigh_map,
                point=Point(x=point.x + 1, y=point.y, value=point.value),
                been_points=been_points
            )
        )

    return points


def part_two(lines: List[List[int]]) -> None:

    low_points: List[Point] = find_low_points(lines)

    basins: List[List[Point]] = []
    for low_point in low_points:
        basin: List[Point] = find_next_points(height_map, low_point)
        basins.append(basin)

    basin_sizes: List[int] = sorted([len(x) for x in basins])

    return basin_sizes[-1] * basin_sizes[-2] * basin_sizes[-3]


with open('2021/09/input.txt', 'r') as file:
    lines: List[str] = file.readlines()

height_map: List[List[int]] = [
    [int(height) for height in line.strip()] for line in lines
]

print(part_one(height_map))
print(part_two(height_map))
