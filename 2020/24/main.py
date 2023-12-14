#!/use/bin/env python
from dataclasses import dataclass
from enum import Enum
from sys import argv
from typing import List, Dict


def read_file(file: str) -> List[str]:
    with open(file, 'r') as f:
        return f.readlines()


class Direction(Enum):
    EAST = 'e'
    SOUTH_EAST = 'se'
    SOUTH_WEST = 'sw'
    WEST = 'w'
    NORTH_WEST = 'nw'
    NORTH_EAST = 'ne'


@dataclass
class Position(object):
    q: int = 0
    r: int = 0
    s: int = 0

    def distance(self):
        return (abs(self.q) + abs(self.r) + abs(self.s)) / 2

    def __hash__(self):
        return self.q.__hash__() + self.r.__hash__() + self.s.__hash__()


def get_directions(input_string: str) -> Position:
    position: int = 0

    pos: Position = Position()

    for i in range(1, len(input_string)):
        direction = input_string[position:i]

        if len(direction) > 2:
            print(direction)
            break

        if direction == Direction.EAST.value:
            position += len(direction)
            pos.q += 1
            pos.s -= 1
        elif direction == Direction.SOUTH_EAST.value:
            position += len(direction)
            pos.r += 1
            pos.s -= 1
        elif direction == Direction.SOUTH_WEST.value:
            position += len(direction)
            pos.r += 1
            pos.q -= 1
        elif direction == Direction.WEST.value:
            position += len(direction)
            pos.q -= 1
            pos.s += 1
        elif direction == Direction.NORTH_WEST.value:
            position += len(direction)
            pos.r -= 1
            pos.s += 1
        elif direction == Direction.NORTH_EAST.value:
            position += len(direction)
            pos.r -= 1
            pos.q += 1

    return pos


def part_one(file: str) -> int:
    directions: List[Position] = []
    for line in read_file(file):
        line = line.strip()
        directions.append(
            get_directions(line)
        )

    print(len(directions))
    print(len(set(directions)))
    print()

    tiles: Dict[Position, int] = dict()

    for d in directions:
        if tiles.get(d) is None:
            tiles[d] = 1
        else:
            tiles[d] += 1

    black_count: int = 0
    for k, v in tiles.items():
        print("{} {}".format(v, k))
        if v % 2 == 1:
            black_count += 1

    return black_count


def part_two(file: str) -> int:
    pass


def main():
    print("Part One: {}".format(part_one(argv[1])))
    print("Part Two: {}".format(part_two(argv[1])))


if __name__ == '__main__':
    main()
