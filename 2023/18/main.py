#!/usr/bin/env python
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Dict

import matplotlib.path
import numpy
import numpy as np

PARENT = Path(__file__).parent


@dataclass
class DigPlan(object):
    direction: str
    distance: int
    colour: str

    def get_movement(self) -> Tuple[int, int]:
        """
        :return: (dx,dy)
        """
        if self.direction == 'U':
            return (0, -self.distance)
        elif self.direction == 'D':
            return (0, self.distance)
        elif self.direction == 'L':
            return (-self.distance, 0)
        elif self.direction == 'R':
            return (self.distance, 0)
        else:
            raise Exception


def read_from_file(file: Path) -> list[DigPlan]:
    dig_plans: List[DigPlan] = []
    with open(file) as f:
        for line in f.readlines():
            direction, distance, colour = line.split()
            dig_plans.append(
                DigPlan(direction=str(direction), distance=int(distance), colour=str(colour[1:-1]))
            )
    return dig_plans


def get_dimensions(
        terrain_map: Dict[Tuple[int, int], DigPlan]
) -> tuple[tuple[int, int], tuple[int, int]]:
    x_min: int = 9999999999
    x_max: int = 0
    y_min: int = 9999999999
    y_max: int = 0

    for key, value in terrain_map.items():
        x, y = key
        x_max = max(x_max, x)
        y_max = max(y_max, y)

        x_min = min(x_min, x)
        y_min = min(y_min, y)

    return (x_max, y_max), (x_min, y_min)


def add(a: Tuple[int, int], b: Tuple[int, int]) -> Tuple[int, int]:
    return (a[0] + b[0], a[1] + b[1])


def dig(dig_plans: List[DigPlan], start: Tuple[int, int] = (0, 0)) -> dict[tuple[int, int], DigPlan]:
    terrain_map: Dict[Tuple[int, int], DigPlan] = dict()
    position: Tuple[int, int] = start

    for dig_plan in dig_plans:
        terrain_map[position] = dig_plan

        movement: Tuple[int, int] = dig_plan.get_movement()
        position = add(position, movement)

    return terrain_map


def on_line(line: Tuple[Tuple[int, int], Tuple[int, int]], point: Tuple[int, int]) -> bool:
    if (
            max(line[0][0], line[1][0]) >= point[0] >= min(line[0][0], line[1][0])
            and max(line[0][1], line[1][1]) >= point[1] >= min(line[0][1], line[1][1])
    ):
        return True
    return False


def intersects(
        side: tuple[tuple[int, int], tuple[int, int]],
        ray: tuple[tuple[int, int], tuple[int, int]]
) -> int:
    """
    https://stackoverflow.com/questions/217578/how-can-i-determine-whether-a-2d-point-is-within-a-polygon
    """
    # Create linear equation A*x + B*y + C = 0
    A_1 = side[0][1] - side[1][1]
    B_1 = side[0][0] - side[1][0]
    C_1 = (side[1][0] * side[1][1]) - (side[0][0] * side[0][1])

    d1 = (A_1 * ray[0][0]) + (B_1 * ray[0][1]) + C_1
    d2 = (A_1 * ray[1][0]) + (B_1 * ray[1][1]) + C_1

    if (d1 > 0 and d2 > 0) or (d1 < 0 and d2 < 0):
        return 0

    # Create linear equation A*x + B*y + C = 0
    A_2 = ray[0][1] - ray[1][1]
    B_2 = ray[0][0] - ray[1][0]
    C_2 = (ray[1][0] * ray[1][1]) - (ray[0][0] * ray[0][1])

    d1 = (A_2 * side[0][0]) + (B_2 * side[0][1]) + C_2
    d2 = (A_2 * side[1][0]) + (B_2 * side[1][1]) + C_2

    if (d1 > 0 and d2 > 0) or (d1 < 0 and d2 < 0):
        return 0

    if (A_1 * B_2) - (A_2 * B_1) == 0:
        return 2

    return 1


def within(position: Tuple[int, int], terrain_map: Dict[Tuple[int, int], DigPlan], x_min: int = 0) -> bool:
    points = [key for key, value in terrain_map.items()]
    previous: Tuple[int, int] = points[-1]

    intersections: int = 0
    ray: tuple[tuple[int, int], tuple[int, int]] = ((position[0], position[1]), (999999, position[1]))

    for current in points:
        side: tuple[tuple[int, int], tuple[int, int]] = (previous, current)

        if on_line(side, position):
            return True

        # Does ray intersect side?
        i = intersects(side, ray)
        if i == 2:
            pass
            # intersections += 1
        elif i == 1:
            intersections += 1

        previous = current

    return (intersections & 1) == 1


def pnpoly(vertices: List[Tuple[int, int]], point: Tuple[int, int]) -> bool:
    """
    https://wrfranklin.org/Research/Short_Notes/pnpoly.html
    ```
    int pnpoly(int nvert, float *vertx, float *verty, float testx, float testy)
{
  int i, j, c = 0;
  for (i = 0, j = nvert-1; i < nvert; j = i++) {
    if ( ((verty[i]>testy) != (verty[j]>testy)) &&
	 (testx < (vertx[j]-vertx[i]) * (testy-verty[i]) / (verty[j]-verty[i]) + vertx[i]) )
       c = !c;
  }
  return c;
}
    ```
    """

    previous: Tuple[int, int] = vertices[-1]
    c: bool = False

    for current in vertices:
        if on_line((previous, current), point):
            return True
        if ((current[1] > point[1]) != (previous[1] > point[1])) and \
                (point[0] < (previous[0] - current[0]) * (point[1] - current[1]) / (previous[1] - current[1]) + current[
                    0]):
            c = not c
        previous = current

    return c


def display(points: List[Tuple[int, int]], x_max, y_max, x_min, y_min):
    print('---------')
    for y in range(y_min, y_max + 1):
        for x in range(x_min, x_max + 1):
            sym: str = "#" if (x, y) in points else "."
            print(f"{sym}", end="")
        print()


def __part_one__(file: Path) -> int:
    dig_plans: List[DigPlan] = read_from_file(file)
    terrain_map: dict[tuple[int, int], DigPlan] = dig(dig_plans)
    (x_max, y_max), (x_min, y_min) = get_dimensions(terrain_map)
    vertices: list[tuple[int, int]] = [key for key, value in terrain_map.items()]
    # display(vertices, x_max, y_max, x_min, y_min)

    count: List[Tuple[int, int]] = []

    for y in range(y_min, y_max + 1):
        for x in range(x_min, x_max + 1):
            # if (x, y) in count:
            #     continue
            # if within((x, y), terrain_map, x_min=x_min):
            #     count.append((x, y))
            if pnpoly(vertices, (x, y)):
                count.append((x, y))

    # display(count, x_max, y_max, x_min, y_min)
    return len(count)


def transform(dig_plans: List[DigPlan]) -> List[DigPlan]:
    for dig_plan in dig_plans:
        dig_plan.distance = int(dig_plan.colour[1:6], 16)
        # 0 means R, 1 means D, 2 means L, and 3 means U.
        direction: int = int(dig_plan.colour[6:7], 16)
        if direction == 0:
            dig_plan.direction = 'R'
        elif direction == 1:
            dig_plan.direction = 'D'
        elif direction == 2:
            dig_plan.direction = 'L'
        elif direction == 3:
            dig_plan.direction = 'U'
        else:
            raise Exception
    return dig_plans


def __part_two__(file: Path) -> int:
    dig_plans: List[DigPlan] = read_from_file(file)
    dig_plans = transform(dig_plans)
    terrain_map: dict[tuple[int, int], DigPlan] = dig(dig_plans)
    (x_max, y_max), (x_min, y_min) = get_dimensions(terrain_map)
    vertices: list[tuple[int, int]] = [key for key, value in terrain_map.items()]
    # display(vertices, x_max, y_max, x_min, y_min)

    x, y = np.meshgrid(np.arange(x_max), np.arange(y_max), sparse=True)
    x, y = x.flatten(), y.flatten()
    points = np.vstack((x, y)).T

    p = matplotlib.path.Path(vertices)
    grid = p.contains_points(points)
    unique, counts = numpy.unique(grid, return_counts=True)

    count: int = 0
    for item in grid:
        if item:
            count += 1
    return count

    mask = grid.reshape(x_max, y_max)

    count: List[Tuple[int, int]] = []

    for y in range(y_min, y_max + 1):
        for x in range(x_min, x_max + 1):
            # if (x, y) in count:
            #     continue
            # if within((x, y), terrain_map, x_min=x_min):
            #     count.append((x, y))
            if pnpoly(vertices, (x, y)):
                count.append((x, y))

    # display(count, x_max, y_max, x_min, y_min)
    return len(count)


def part_one() -> int:
    example: int = __part_one__(PARENT.joinpath('example.txt'))
    assert example == 62
    answer: int = __part_one__(PARENT.joinpath('input.txt'))
    return answer


def part_two() -> int:
    example: int = __part_two__(PARENT.joinpath('example.txt'))
    assert example == 952408144115
    answer: int = __part_two__(PARENT.joinpath('input.txt'))
    return answer


def main():
    print("Part One: {}".format(part_one()))
    # print("Part Two: {}".format(part_two()))


if __name__ == '__main__':
    main()
