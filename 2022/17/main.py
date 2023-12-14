#!/usr/bin/env python
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

PARENT = Path(__file__).parent


@dataclass
class Point(object):
    x: int
    y: int

    def __hash__(self):
        return hash(self.x) + hash(self.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)


# Point in reference to bottom-left corner
ROCKS: List[List[Point]] = [
    [  # ----
        Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0)
    ],
    [  # +
        Point(1, 2),
        Point(0, 1), Point(1, 1), Point(2, 1),
        Point(1, 0)
    ],
    [  # _|
        Point(2, 2),
        Point(2, 1),
        Point(0, 0), Point(1, 0), Point(2, 0),
    ],
    [  # |
        Point(0, 3),
        Point(0, 2),
        Point(0, 1),
        Point(0, 0)
    ],
    [  # square
        Point(0, 1), Point(1, 1),
        Point(0, 0), Point(1, 0),
    ]
]

GAS_DIRECTION = {
    '<': Point(-1, 0),
    '>': Point(1, 0)
}


def read_from_file(file: Path) -> str:
    with open(file) as f:
        return f.read().strip()


def fits(position: Point, rock: List[Point], chamber: List[List[int]]) -> bool:
    for point in rock:
        position_next = position + point

        if 0 <= position_next.x < 7 and position_next.y >= 0:
            pass
        else:
            return False

        if chamber[position_next.y][position_next.x] != 0:
            if chamber[position_next.y][position_next.x] > 1:
                raise Exception()
            return False
    return True


def fall(rock: List[Point], chamber: List[List[int]], direction: deque[str], height: int = 0, bottom: int = 0) -> int:
    position = Point(2, height - bottom + 3)
    position_next = position

    max_height: int = 15

    while True:

        while len(chamber) < height - bottom + 3 + 4:
            chamber.append([0, 0, 0, 0, 0, 0, 0])
        # if len(chamber) > height - bottom + 3 + 4:
        #     raise Exception

        # Gas direction
        d = direction[0]
        direction.rotate(-1)

        position_next = position + GAS_DIRECTION[d]

        if fits(position_next, rock, chamber):
            position = position_next

        # Fall
        position_next = position + Point(0, -1)

        if fits(position_next, rock, chamber):
            position = position_next
        else:
            break

    new_height: int = height
    for point in rock:
        p = position + point
        new_height = max(bottom + p.y + 1, new_height)
        if chamber[p.y][p.x]:
            raise Exception
        chamber[p.y][p.x] += 1

    bottoms: List[int] = [0 for _ in range(7)]

    for x in range(7):
        for y in reversed(range(len(chamber))):
            if chamber[y][x] > 0:
                bottoms[x] = y
                break

    bottom += min(bottoms)
    for y in range(min(bottoms)):
        chamber.pop(0)

    dt = new_height - height
    db = min(bottoms)

    return dt, db, chamber


def display(chamber: List[List[int]], height: int):
    output: str = ""
    for y in reversed(chamber):
        line: str = "|"
        for x in y:
            if x:
                line += "#"
            else:
                line += '.'
        output += line
        output += "|\n"
    output += "+-------+\n"
    print(output)


def state(chamber: List[List[int]]) -> int:
    h: int = 0
    for i, y in enumerate(chamber):
        for j, x in enumerate(y):
            h += (i + 1) * (j + 1) * x

    return h


def __part_one__(file: Path, stop: int = 2022) -> int:
    jet_directions = deque(read_from_file(file))
    height: int = 0
    bottom: int = 0
    chamber: List[List[int]] = []
    seen: Dict[Tuple[int, int], Tuple[int, int, List[List[int]]]] = dict()

    for i in range(stop):
        rock_iter: int = i % len(ROCKS)
        key: int = state(chamber)

        s = seen.get((key, rock_iter))

        if s is None:
            rock = ROCKS[rock_iter]
            dh, db, new_chamber = fall(rock, chamber, jet_directions, height, bottom)
            seen[(key, rock_iter)] = (dh, db, new_chamber)
        else:
            dh, db, new_chamber = s

        height += dh
        bottom += db
        chamber = new_chamber

    return height


def __part_two__(file: Path) -> int:
    raise Exception("Not implemented")
    content: str = read_from_file(file)
    return 0


def part_one() -> int:
    assert __part_one__(PARENT.joinpath('example.txt'), stop=1) == 1
    assert __part_one__(PARENT.joinpath('example.txt'), stop=2) == 4
    assert __part_one__(PARENT.joinpath('example.txt'), stop=3) == 6
    assert __part_one__(PARENT.joinpath('example.txt'), stop=4) == 7
    assert __part_one__(PARENT.joinpath('example.txt'), stop=5) == 9
    assert __part_one__(PARENT.joinpath('example.txt'), stop=6) == 10
    assert __part_one__(PARENT.joinpath('example.txt'), stop=7) == 13
    assert __part_one__(PARENT.joinpath('example.txt'), stop=8) == 15
    assert __part_one__(PARENT.joinpath('example.txt'), stop=9) == 17
    assert __part_one__(PARENT.joinpath('example.txt'), stop=10) == 17

    example: int = __part_one__(PARENT.joinpath('example.txt'))
    assert example == 3068
    answer: int = __part_one__(PARENT.joinpath('input.txt'))
    return answer


def part_two() -> int:
    example: int = __part_one__(PARENT.joinpath('example.txt'), stop=1000000000000)
    assert example == 1514285714288
    answer: int = __part_one__(PARENT.joinpath('input.txt'), stop=1000000000000)
    return answer


def main():
    print("Part One: {}".format(part_one()))
    print("Part Two: {}".format(part_two()))


if __name__ == '__main__':
    main()
