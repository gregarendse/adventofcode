#!/usr/bin/env python
import re
from pathlib import Path
from typing import Dict, List

PARENT = Path(__file__).parent


def read_from_file(file: Path) -> list[str]:
    with open(file) as f:
        return [s.strip() for s in f.read().split(',')]


def character_hash(c: str, current_value: int = 0) -> int:

    current_value += ord(c)
    current_value = current_value * 17
    current_value = current_value % 256

    return current_value


def str_hash(s: str) -> int:
    current_value: int = 0
    for c in s:
        current_value = character_hash(c, current_value=current_value)
    return current_value


def __part_one__(file: Path) -> int:
    sequence: list[str] = read_from_file(file)

    totals: List[int] = []

    for s in sequence:
        totals.append(
            str_hash(s)
        )

    return sum(totals)


def __part_two__(file: Path) -> int:
    sequence: list[str] = read_from_file(file)
    pattern = re.compile(r"(\w+)([-=])(\d?)")

    boxes: List[List[str]] = [[] for _ in range(256)]
    lense_map: Dict[str, int] = dict()

    for s in sequence:
        matches = pattern.findall(s)
        label, operation, focal_length = matches.pop()

        box_idx: int = str_hash(label)

        idx: int = None
        for i, existing_label in enumerate(boxes[box_idx]):
            if existing_label == label:
                idx = i
                break

        if operation == '=':
            if idx is not None:
                lense_map[label] = int(focal_length)
            else:
                boxes[box_idx].append(label)
                lense_map[label] = int(focal_length)
        elif operation == '-':
            if idx is not None:
                boxes[box_idx].pop(idx)
        else:
            raise Exception(operation)

    total: List[int] = []
    for box_idx, box in enumerate(boxes):
        sub_total: List[int] = []

        for idx, l in enumerate(box):
            sub_total.append(
                (box_idx + 1) * (idx + 1) * lense_map[l]
            )

        total.append(sum(sub_total))
    return sum(total)


def part_one() -> int:
    assert str_hash("HASH") == 52

    example: int = __part_one__(PARENT.joinpath('example.txt'))
    assert example == 1320
    answer: int = __part_one__(PARENT.joinpath('input.txt'))
    return answer


def part_two() -> int:
    example: int = __part_two__(PARENT.joinpath('example.txt'))
    assert example == 145
    answer: int = __part_two__(PARENT.joinpath('input.txt'))
    return answer


def main():
    print("Part One: {}".format(part_one()))
    print("Part Two: {}".format(part_two()))


if __name__ == '__main__':
    main()
