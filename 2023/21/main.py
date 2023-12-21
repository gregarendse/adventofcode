#!/usr/bin/env python
from collections import defaultdict, deque
from copy import copy
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Set

PARENT = Path(__file__).parent


class Comparable:
    def __cmp__(self, other):
        raise NotImplementedError

    def __eq__(self, other):
        return self.__cmp__(other) == 0

    def __ne__(self, other):
        return self.__cmp__(other) != 0

    def __gt__(self, other):
        return self.__cmp__(other) > 0

    def __lt__(self, other):
        return self.__cmp__(other) < 0

    def __ge__(self, other):
        return self.__cmp__(other) >= 0

    def __le__(self, other):
        return self.__cmp__(other) <= 0


@dataclass(unsafe_hash=True)
class Point():
    x: int
    y: int

    def __add__(self, other):
        return Point(x=self.x + other.x, y=self.y + other.y)


def read_from_file(file: Path) -> tuple[Point, list[list[str]], dict[Point, str]]:
    garden: List[List[str]] = []
    garden_map: Dict[Point, str] = defaultdict(lambda: '.')
    start: Point = None

    with open(file) as f:
        for y, line in enumerate(f.readlines()):
            ys: List[str] = []
            for x, c in enumerate(line.strip()):
                if c == 'S':
                    start = point
                    c = '.'

                point: Point = Point(x=x, y=y)
                garden_map[point] = c
                ys.append(c)

            garden.append(ys)

    return start, garden, garden_map


def walk(start: Point, garden: List[List[str]], steps: int = 64) -> int:
    q = deque([(start, steps, [start])])
    history: Set[Point] = set()
    visited: Set[Point] = set()

    max_point: Point = Point(y=len(garden), x=len(garden[0]))
    min_point: Point = Point(x=0, y=0)

    while q:
        (position, remaining_steps, path) = q.popleft()

        if remaining_steps == 0:
            for i in reversed(range(0, len(path), 2)):
                visited.add(path[i])
            continue

        for step in [Point(0, 1), Point(1, 0), Point(0, -1), Point(-1, 0)]:
            position_next = position + step

            if min_point.x <= position_next.x <= max_point.x \
                    and min_point.y <= position_next.y <= max_point.y:
                if garden[position_next.y][position_next.x] != '.':
                    continue

                if position_next not in path:
                    path.append(position_next)
                    q.append((position_next, remaining_steps - 1, copy(path)))

    return len(visited)


def __part_one__(file: Path, steps=64) -> int:
    start, garden, garden_map = read_from_file(file)

    total = walk(start, garden, steps=steps)
    return total


def __part_two__(file: Path) -> int:
    raise Exception("Not implemented")
    content: str = read_from_file(file)
    return 0


def part_one() -> int:
    example: int = __part_one__(PARENT.joinpath('example.txt'), steps=6)
    assert example == 16
    answer: int = __part_one__(PARENT.joinpath('input.txt'))
    return answer


def part_two() -> int:
    example: int = __part_two__(PARENT.joinpath('example.txt'))
    assert example == 0
    answer: int = __part_two__(PARENT.joinpath('input.txt'))
    return answer


def main():
    print("Part One: {}".format(part_one()))
    print("Part Two: {}".format(part_two()))


if __name__ == '__main__':
    main()
