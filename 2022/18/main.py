#!/use/bin/env python
from dataclasses import dataclass
from sys import argv
from typing import List, Dict, Set


@dataclass
class Cube(object):
    x: int
    y: int
    z: int

    exposed: Dict[str, int]

    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z
        self.exposed = {
            'X+': 1,
            'X-': 1,
            'Y+': 1,
            'Y-': 1,
            'Z+': 1,
            'Z-': 1
        }

    def __str__(self):
        return "{}, {}, {}".format(self.x, self.y, self.z)

    def __hash__(self):
        return hash(self.x) + hash(self.y) + hash(self.z)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def count_exposed(self) -> int:
        return sum(self.exposed.values())

    def is_adjacent(self, cube) -> bool:
        x: int = self.x - cube.x
        y: int = self.y - cube.y
        z: int = self.z - cube.z
        test: bool = sum([abs(x), abs(y), abs(z)]) == 1
        return test

    def set_adjacent(self, cube) -> None:
        x: int = self.x - cube.x
        y: int = self.y - cube.y
        z: int = self.z - cube.z

        if x != 0:
            if self.x < cube.x:
                self.exposed['X-'] = 0
                cube.exposed['X+'] = 0
            else:
                self.exposed['X+'] = 0
                cube.exposed['X-'] = 0
        if y != 0:
            if self.y < cube.y:
                self.exposed['Y-'] = 0
                cube.exposed['Y+'] = 0
            else:
                self.exposed['Y+'] = 0
                cube.exposed['Y-'] = 0
        if z != 0:
            if self.z < cube.z:
                self.exposed['Z-'] = 0
                cube.exposed['Z+'] = 0
            else:
                self.exposed['Z+'] = 0
                cube.exposed['Z-'] = 0


def read_from_file(file: str) -> List[Cube]:
    with open(file) as f:
        cubes: List[Cube] = []
        for line in f.readlines():
            x, y, z = line.split(',')
            cubes.append(
                Cube(int(x), int(y), int(z))
            )
    return cubes


def part_one(file: str) -> int:
    cubes: List[Cube] = read_from_file(file)
    for i in range(len(cubes)):
        for j in range(i):
            test: bool = cubes[i].is_adjacent(cubes[j])
            if test:
                cubes[i].set_adjacent(cubes[j])
            # print("{} : {} -> {}".format(cubes[i], cubes[j], test))

    return sum([cube.count_exposed() for cube in cubes])


def get_neighbours(cube: Cube) -> List[Cube]:
    neighbours: List[Cube] = []
    for delta in [Cube(1, 0, 0), Cube(-1, 0, 0), Cube(0, 1, 0), Cube(0, -1, 0), Cube(0, 0, 1), Cube(0, 0, -1)]:
        neighbours.append(Cube(cube.x + delta.x, cube.y + delta.y, cube.z + delta.z))
    return neighbours


def part_two(file: str) -> int:
    cubes: List[Cube] = read_from_file(file)

    max_x: int = max([cube.x for cube in cubes]) + 1
    min_x: int = min([cube.x for cube in cubes]) - 1
    max_y: int = max([cube.y for cube in cubes]) + 1
    min_y: int = min([cube.y for cube in cubes]) - 1
    max_z: int = max([cube.z for cube in cubes]) + 1
    min_z: int = min([cube.z for cube in cubes]) - 1

    seen: Set[Cube] = set()
    queue: List[Cube] = [Cube(max_x, max_y, max_z)]  # Starting point
    exposed: int = 0

    while queue:
        current: Cube = queue.pop()

        if current in cubes:
            exposed += 1
            continue

        if current not in seen:
            seen.add(current)

            for neighbour in get_neighbours(current):
                if min_x <= neighbour.x <= max_x \
                        and min_y <= neighbour.y <= max_y \
                        and min_z <= neighbour.z <= max_z:
                    queue.append(neighbour)

    return exposed


def main(file: str):
    if file is None:
        file = argv[1]

    example_2: int = part_one('example_2.txt')
    assert example_2 == 10
    example: int = part_one('example.txt')
    assert example == 64
    p1 = part_one('input.txt')
    print("Part One: {}".format(p1))

    p2: int = part_two('example.txt')
    assert p2 == 58
    p2 = part_two('input.txt')
    print("Part Two: {}".format(p2))


if __name__ == '__main__':
    main(file='example.txt')
