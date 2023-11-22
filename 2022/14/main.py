#!/usr/bin/env python
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

PARENT = Path(__file__).parent


def read_from_file(file: Path) -> List[List[Tuple[int, int]]]:
    with open(file) as f:
        rocks: List[List[Tuple[int, int]]] = []
        for line in f.readlines():
            coordstr = line.split(' -> ')
            rock: List[Tuple[int, int]] = []
            for coord in coordstr:
                x, y = coord.split(',')
                rock.append((int(x), int(y)))
            rocks.append(rock)

        return rocks


def get_points(start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:

    if start[0] == end[0]:
        min_y = min(start[1], end[1])
        max_y = max(start[1], end[1])
        return [(start[0], min_y + i) for i in range(max_y - min_y + 1)]
    elif start[1] == end[1]:
        min_x = min(start[0], end[0])
        max_x = max(start[0], end[0])

        return [(min_x + i, start[1]) for i in range(max_x - min_x + 1)]
    else:
        raise Exception()


def populate_map(rocks: List[List[Tuple[int, int]]]) -> Dict[Tuple[int, int], int]:
    rock_map: Dict[Tuple[int, int]] = defaultdict(int)

    for rock in rocks:
        for i in range(1, len(rock)):
            start = rock[i - 1]
            end = rock[i]
            for point in get_points(start, end):
                rock_map[point] = 8

    return rock_map


def is_between(start: Tuple[int, int], end: Tuple[int, int], point: Tuple[int, int]) -> bool:
    dxc = point[0] - start[0]
    dyc = point[1] - start[1]

    dxl = end[0] - start[0]
    dyl = end[1] - start[1]

    if (dxc * dyl - dyc * dxl) != 0:
        return False

    if abs(dxl) >= abs(dyl):
        return dxl > 0 if start[0] <= point[0] <= end[0] else end[0] <= point[0] <= start[0]
    else:
        return dyl > 0 if start[1] <= point[1] <= end[1] else end[1] <= point[1] <= start[1]


def can_move(position: Tuple[int, int], rocks: List[List[Tuple[int, int]]]) -> bool:
    for rock in rocks:
        for i in range(1, len(rock)):
            starting_point = rock[i - 1]
            ending_point = rock[i]
            if is_between(starting_point, ending_point, position):
                return False

    return True


def fall(rocks: List[List[Tuple[int, int]]], start: Tuple[int, int] = (500, 0), max_y: int = 0) -> Optional[
    Tuple[int, int]]:
    position: Tuple[int, int] = start
    next_position: Tuple[int, int] = start

    while position == next_position:
        for move in [(0, 1), (-1, 1), (1, 1)]:
            next_position = (position[0] + move[0], position[1] + move[1])
            if can_move(next_position, rocks):
                position = next_position
                break
        if position[1] > max_y:
            return None

    return position


def __part_one__(file: Path) -> int:
    rocks: list[list[tuple[int, int]]] = read_from_file(file)
    max_y: int = 0
    for rock in rocks:
        for position in rock:
            max_y = max(max_y, position[1])

    counter: int = 0
    position: Tuple[int, int] = (0, 0)
    while position:
        position = fall(rocks, start=(500, 0), max_y=max_y)
        if position is None:
            return counter
        counter += 1
        rocks.append([(position[0], position[1]), (position[0], position[1] + 1)])
    raise Exception("Nope...")


def fall_2(cave: Dict[Tuple[int, int], int], start: Tuple[int, int] = (500, 0), max_y: int = 0) -> Optional[
    Tuple[int, int]]:

    position: Tuple[int, int] = start
    next_position: Tuple[int, int] = start

    while position == next_position:
        for move in [(0, 1), (-1, 1), (1, 1)]:
            next_position = (position[0] + move[0], position[1] + move[1])

            if next_position[1] < max_y and cave[next_position] == 0:
                position = next_position
                break

    return position


def display(cave: Dict[Tuple[int, int], int]):
    min_x: int = 999999999
    max_x: int = 0
    min_y: int = 999999999
    max_y: int = 0

    for position, value in cave.items():
        min_x = min(min_x, position[0])
        max_x = max(max_x, position[0])
        min_y = min(min_y, position[1])
        max_y = max(max_y, position[1])

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            value = cave[(x, y)]
            if value == 0:
                print('.', end='')
            elif value == 8:
                print('#', end='')
            elif value == 1:
                print('o', end='')
            else:
                raise Exception()
        print()


def __part_two__(file: Path) -> int:
    rocks: list[list[tuple[int, int]]] = read_from_file(file)
    cave: Dict[Tuple[int, int]] = populate_map(rocks)

    max_y: int = 0
    for rock in rocks:
        for position in rock:
            max_y = max(max_y, position[1])
    max_y += 2

    counter: int = 0
    position: Tuple[int, int] = (0, 0)

    while position:
        counter += 1
        position = fall_2(cave, start=(500, 0), max_y=max_y)
        if position == (500, 0):
            break
        cave[position] = 1

    return counter


def part_one() -> int:
    example: int = __part_one__(PARENT.joinpath('example.txt'))
    assert example == 24
    answer: int = __part_one__(PARENT.joinpath('input.txt'))
    return answer


def part_two() -> int:
    example: int = __part_two__(PARENT.joinpath('example.txt'))
    assert example == 93
    answer: int = __part_two__(PARENT.joinpath('input.txt'))
    return answer


def main():
    print("Part One: {}".format(part_one()))
    print("Part Two: {}".format(part_two()))


if __name__ == '__main__':
    main()
