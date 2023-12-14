#!/usr/bin/env python
from pathlib import Path
from typing import Dict, List, Set, Tuple

PARENT = Path(__file__).parent


def read_from_file(file: Path) -> list[list[str]]:
    patterns: List[List[str]] = []
    with open(file) as f:
        for pattern in f.read().split('\n\n'):
            patterns.append(
                [line.strip() for line in pattern.splitlines()]
            )
        return patterns


def difference(left: str, right: str) -> list[int]:
    diff: int = 0
    diff_list: List[int] = []
    for i in range(min(len(left), len(right))):
        if left[i] != right[i]:
            diff += 1
            diff_list.append(i)
    return diff_list


def difference_list(left: List[str], right: List[str]) -> list[tuple[int, int]]:
    diff: int = 0
    diff_list: List[Tuple[int, int]] = []
    for i in range(min(len(left), len(right))):
        for d in difference(left[i], right[i]):
            diff_list.append((d, i))
    return diff_list


def find_vertical(pattern: List[str], threshold: int = 0) -> int:
    vertical_lines: List[List[int]] = []
    differnece_map: Dict[int, List[int]] = dict()
    for line in pattern:
        l = len(line)
        local_vertical_lines: List[int] = []
        for i in range(1, l):
            left: str = line[max((i - l // 2) * 2 - 1, 0):i]
            right: str = line[i:min(i + i, l)]
            difference1 = difference(left, "".join(reversed(right)))
            if len(difference1) == threshold:
                local_vertical_lines.append(i)
                differnece_map[i] = difference1
        vertical_lines.append(local_vertical_lines)

    vertical_set: Set[int] = set(vertical_lines[0])
    for local_vertical_lines in vertical_lines:
        vertical_set = vertical_set.intersection(local_vertical_lines)

    if len(vertical_set):
        pop = vertical_set.pop()
        return pop, differnece_map.get(pop)
    else:
        return 0, []


def find_horizontal(pattern: List[str], threshold: int = 0) -> int:
    horizontal_lines: List[int] = []
    differnece_map: Dict[int, List[Tuple[int, int]]] = dict()
    l: int = len(pattern)
    for i in range(1, l):
        # max(((i+1) - l // 2) * 2, 0)
        left: List[str] = pattern[max((i - l // 2) * 2 - 1, 0):i]
        # min(i + i, l)
        right: List[str] = pattern[i:min(i + i, l)]

        difference_list1 = difference_list(left, list(reversed(right)))
        if len(difference_list1) == threshold:
            horizontal_lines.append(i)
            differnece_map[i] = difference_list1
    if len(horizontal_lines):
        pop = horizontal_lines.pop()
        return pop, differnece_map.get(pop)
    else:
        return 0, []


def find_reflection_point(pattern: List[str], threshold: int = 0) -> int:

    vertical_line: int = find_vertical(pattern, threshold)
    horizontal_line: int = find_horizontal(pattern, threshold)

    return vertical_line + horizontal_line * 100


def __part_one__(file: Path) -> int:
    patterns: list[list[str]] = read_from_file(file)

    summaries: List[int] = []
    for pattern in patterns:
        summaries.append(
            find_reflection_point(pattern)
        )

    return sum(summaries)


def __part_two__(file: Path) -> int:
    patterns: list[list[str]] = read_from_file(file)

    summaries: List[int] = []
    for pattern in patterns:

        horizontal_point, horizontal_changes = find_horizontal(pattern, 1)
        if horizontal_point:
            x, y = horizontal_changes.pop()
            c: str = '.' if pattern[y][x] == '#' else '#'
            pattern[y] = pattern[y][:x] + c + pattern[y][x:]
            vertical_point, vertical_changes = find_vertical(pattern)
            summaries.append(vertical_point + horizontal_point * 100)
            continue

        vertical_point, vertical_changes = find_vertical(pattern, 1)
        if vertical_point:
            y = vertical_point
            x = vertical_changes.pop()
            c: str = '.' if pattern[y][x] == '#' else '#'
            pattern[y] = pattern[y][:x] + c + pattern[y][x:]
            horizontal_point, horizontal_changes = find_horizontal(pattern)
            summaries.append(vertical_point + horizontal_point * 100)
            continue

    return sum(summaries)


def part_one() -> int:
    example: int = __part_one__(PARENT.joinpath('example.txt'))
    assert example == 405
    answer: int = __part_one__(PARENT.joinpath('input.txt'))
    return answer


def part_two() -> int:
    example: int = __part_two__(PARENT.joinpath('example.txt'))
    assert example == 400
    answer: int = __part_two__(PARENT.joinpath('input.txt'))
    return answer


def main():
    print("Part One: {}".format(part_one()))
    print("Part Two: {}".format(part_two()))


if __name__ == '__main__':
    main()
