#!/usr/bin/env python
from collections import deque
from pathlib import Path
from typing import List, Set, Tuple

PARENT = Path(__file__).parent


def expand_image_idx_y(image: List[List[str]]) -> List[int]:
    expanded_image: list[list[str]] = []
    ys: List[int] = []

    for i, y in enumerate(image):
        expanded_image.append(list(y))
        if len(set(y)) == 1:
            ys.append(i)
    return ys


def expand_image_idx_x(image: List[List[str]]) -> List[int]:
    xs: List[int] = []

    for i in reversed(range(len(image[0]))):
        expand: bool = True
        for j in range(len(image)):
            if image[j][i] != '.':
                expand = False
                break

        if expand:
            xs.append(i)

    return xs


def expand_image(image: List[List[str]]):
    expanded_image: list[list[str]] = []

    for y in image:
        expanded_image.append(list(y))
        if len(set(y)) == 1:
            expanded_image.append(list(y))

    for i in reversed(range(len(image[0]))):

        expand: bool = True
        for j in range(len(image)):
            if image[j][i] != '.':
                expand = False
                break

        if expand:
            for j in range(len(expanded_image)):
                expanded_image[j].insert(i, '.')

    return expanded_image


def read_from_file(file: Path) -> list[list[str]]:
    image: List[List[str]] = []

    with open(file) as f:
        for y, line in enumerate(f.readlines()):
            image.append([])
            for x, c in enumerate(line.strip()):
                image[y].append(c)

    return image


def find_path(start: Tuple[int, int], image: List[List[str]]):
    q = deque([start])
    seen: Set[Tuple[int, int]] = set()
    distance: int = 0
    end = None

    while q:

        position: Tuple[int, int] = q.popleft()

        if image[position[1]][position[0]] == '#' and position != start:
            end = position
            break

        # Next moves...
        for move in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            position_next = (position[0] + move[0], position[1] + move[1])
            if position_next not in seen \
                    and 0 <= position_next[0] < len(image[1]) \
                    and 0 <= position_next[1] < len(image):
                q.append(position_next)
                seen.add(position_next)

    return end


def calculate_distance(start, end) -> int:
    return abs(start[0] - end[0]) + abs(start[1] - end[1])


def __part_one__(file: Path) -> int:
    image = read_from_file(file)
    image = expand_image(image)

    galaxy_points: List[Tuple[int, int]] = []
    for y, line in enumerate(image):
        for x, c in enumerate(line):
            if c == '#':
                galaxy_points.append((x, y))

    distances: List[int] = []
    for i in range(len(galaxy_points)):
        for j in range(i, len(galaxy_points)):
            distances.append(calculate_distance(galaxy_points[i], galaxy_points[j]))
    return sum(distances)


def __part_two__(file: Path, expand: int = 1000000) -> int:
    image = read_from_file(file)
    galaxy_points: List[Tuple[int, int]] = []
    for y, line in enumerate(image):
        for x, c in enumerate(line):
            if c == '#':
                galaxy_points.append((x, y))
    expand_y = expand_image_idx_y(image)
    expand_x = expand_image_idx_x(image)

    expanded_points: List[Tuple[int, int]] = []

    for _ in range(len(galaxy_points)):
        point = galaxy_points.pop(0)
        y_sum: int = len([y for y in expand_y if y < point[1]])
        if y_sum > 0:
            new_y: int = point[1] + (expand * y_sum) - y_sum
        else:
            new_y = point[1]

        x_sum: int = len([x for x in expand_x if x < point[0]])
        if x_sum > 0:
            new_x: int = point[0] + (expand * x_sum) - x_sum
        else:
            new_x = point[0]

        expanded_points.append(
            (new_x, new_y)
        )

    distances: List[int] = []
    for i in range(len(expanded_points)):
        for j in range(i + 1, len(expanded_points)):
            start = expanded_points[i]
            end = expanded_points[j]
            distances.append(calculate_distance(start, end))
    return sum(distances)


def part_one() -> int:
    example: int = __part_one__(PARENT.joinpath('example.txt'))
    assert example == 374
    answer: int = __part_one__(PARENT.joinpath('input.txt'))
    return answer


def part_two() -> int:
    example: int = __part_two__(PARENT.joinpath('example.txt'), 2)
    assert example == 374

    # 10 -> 1030
    example: int = __part_two__(PARENT.joinpath('example.txt'), 10)
    assert example == 1030

    # 100 -> 8410
    example: int = __part_two__(PARENT.joinpath('example.txt'), 100)
    assert example == 8410

    answer: int = __part_two__(PARENT.joinpath('input.txt'))
    return answer


def main():
    print("Part One: {}".format(part_one()))
    print("Part Two: {}".format(part_two()))


if __name__ == '__main__':
    main()
