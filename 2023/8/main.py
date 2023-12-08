#!/usr/bin/env python
import re
from collections import deque
from pathlib import Path
from typing import Dict, List, Tuple

import numpy

PARENT = Path(__file__).parent


def read_from_file(file: Path) -> str:
    pattern = re.compile(r"(\w+) = \((\w+), (\w+)\)")
    point_map: Dict[str, Tuple[str, str]] = dict()
    with open(file) as f:
        content: str = f.read()

        instructions, points = content.split('\n\n')

        for point in points.splitlines():
            matches = pattern.findall(point)

            point_map[matches[0][0]] = (matches[0][1], matches[0][2])

    return instructions, point_map


def __part_one__(file: Path) -> int:
    instructions, point_map = read_from_file(file)

    current_point: str = 'AAA'
    q = deque(instructions[:])

    counter: int = 0

    while current_point != 'ZZZ':
        i = q.popleft()
        q.append(i)
        idx: int = 1 if i == 'R' else 0

        current_point = point_map[current_point][idx]
        counter += 1

    return counter


def path(point: str, point_map: Dict[str, Tuple[str, str]], instructions: str):
    counter: int = 0
    q = deque(instructions[:])

    while not point.endswith('Z'):
        i = q.popleft()
        q.append(i)
        idx: int = 1 if i == 'R' else 0

        point = point_map[point][idx]
        counter += 1

    return counter


def lcm(numbers: List[int]) -> int:
    mult_max: int = 1

    number_map: Dict[int, int] = dict()
    for n in numbers:
        number_map[n] = n
        mult_max *= n

    while len(set(list(number_map.values()))) != 1:

        for key, value in number_map.items():

            for other_value in number_map.values():
                while number_map[key] < other_value:
                    number_map[key] = number_map[key] + key

    return other_value


def __part_two__(file: Path) -> int:
    instructions, point_map = read_from_file(file)

    current_points: List[str] = [point for point in point_map.keys() if point.endswith('A')]
    counts: List[int] = []

    for point in current_points:
        count = path(point, point_map, instructions)
        counts.append(count)

    return numpy.lcm.reduce(counts, dtype=numpy.int64)
    return lcm(numbers=counts)

    q = deque(instructions[:])

    counter: int = 0

    while any([bool(not point.endswith('Z')) for point in current_points]):
        i = q.popleft()
        q.append(i)
        idx: int = 1 if i == 'R' else 0

        for _ in range(len(current_points)):
            point = current_points.pop(0)
            current_points.append(
                point_map[point][idx]
            )
        counter += 1

    return counter


def part_one() -> int:
    example: int = __part_one__(PARENT.joinpath('example.txt'))
    assert example == 2
    answer: int = __part_one__(PARENT.joinpath('input.txt'))
    return answer


def part_two() -> int:
    example: int = __part_two__(PARENT.joinpath('example_2.txt'))
    assert example == 6
    answer: int = __part_two__(PARENT.joinpath('input.txt'))
    return answer


def main():
    print("Part One: {}".format(part_one()))
    print("Part Two: {}".format(part_two()))


if __name__ == '__main__':
    main()
