#!/bin/python

from dataclasses import dataclass
from typing import Dict, List, Set
import statistics
import copy


@dataclass
class Path(object):
    start: str
    end: str


def traverse(paths: List[Path], position: str = 'end', history=None, route: List[Path] = [], twice: bool = True) -> int:

    if position == 'start':
        return 1

    route.append(position)
    count: int = 0

    if history is None:
        history = set()

    if position in history:
        if position != 'end' and not twice:
            twice = True
        else:
            return 0

    if position.islower():
        history.add(position)

    for path in paths:
        if path.start == position:
            count += traverse(paths, path.end, copy.deepcopy(history),
                              copy.deepcopy(route), twice=twice)
        if path.end == position:
            count += traverse(paths, path.start, copy.deepcopy(history),
                              copy.deepcopy(route), twice=twice)

    return count


def part_one(paths: List[Path]) -> int:
    count: int = traverse(paths=paths, position='end', history=set())
    return count


def part_two(paths: List[Path]) -> None:
    count: int = traverse(paths=paths, position='end',
                          history=set(), twice=False)
    return count


def read_input() -> List[List[int]]:

    with open('2021/12/input.txt', 'r') as file:
        paths: List[Path] = []
        for line in file.readlines():
            paths.append(Path(line.strip().split(
                '-')[0], line.strip().split('-')[1]))
        return paths


paths: List[Path] = read_input()


print(part_one(copy.deepcopy(paths)))
print(part_two(copy.deepcopy(paths)))
