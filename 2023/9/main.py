#!/usr/bin/env python
from pathlib import Path
from typing import List, Set

PARENT = Path(__file__).parent


def read_from_file(file: Path) -> list[list[int]]:
    with open(file) as f:
        return [
            [
                int(n) for n in line.split()
            ] for line in f.readlines()
        ]


def build_pattern(numbers: list[int], diffs: List[int] = None) -> List[List[int]]:
    if diffs is None:
        diffs = [numbers]

    local_diffs: List[int] = []
    for i in range(len(numbers) - 1):
        diff: int = numbers[i + 1] - numbers[i]
        local_diffs.append(diff)

    diffs.append(local_diffs)
    diff_set: Set[int] = set(local_diffs)
    if len(diff_set) == 1 and diff_set.pop() == 0:
        return diffs
    else:
        return build_pattern(local_diffs, diffs)


def __part_one__(file: Path) -> int:
    lines: list[list[int]] = read_from_file(file)

    totals: List[int] = []

    for line in lines:
        pattern: list[list[int]] = build_pattern(line)

        previous_value: int = 0
        for values in reversed(pattern):
            previous_value += values[-1]
        totals.append(previous_value)

    return sum(totals)


def __part_two__(file: Path) -> int:
    lines: list[list[int]] = read_from_file(file)

    totals: List[int] = []

    for line in lines:
        pattern: list[list[int]] = build_pattern(line)

        previous_value: int = 0
        for values in reversed(pattern):
            previous_value = values[0] - previous_value
        totals.append(previous_value)

    return sum(totals)


def part_one() -> int:
    example: int = __part_one__(PARENT.joinpath('example.txt'))
    assert example == 114
    answer: int = __part_one__(PARENT.joinpath('input.txt'))
    return answer


def part_two() -> int:
    example: int = __part_two__(PARENT.joinpath('example.txt'))
    assert example == 2
    answer: int = __part_two__(PARENT.joinpath('input.txt'))
    return answer


def main():
    print("Part One: {}".format(part_one()))
    print("Part Two: {}".format(part_two()))


if __name__ == '__main__':
    main()
