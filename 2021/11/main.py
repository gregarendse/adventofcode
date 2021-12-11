#!/bin/python

from dataclasses import dataclass
from typing import Dict, List, Set
import statistics
import copy


@dataclass
class Position(object):
    i: int
    j: int

    def __hash__(self) -> int:
        return hash(self.i) + hash(self.j)


counts: List[int] = [0]


def find_adjasent(grid: List[List[int]], position: Position, history: Set[Position] = set()):
    # max(i-1,0) -> min(i+1,len(grid))
    for i in range(max(0, position.i - 1), min(len(grid), position.i + 2)):
        # max(j - 1, 0) -> min(j + 1, len(grid[i]))
        for j in range(max(position.j - 1, 0), min(position.j + 2, len(grid[i]))):
            grid[i][j] += 1

            new_position: Position = Position(i, j)
            if grid[i][j] > 9 and new_position not in history:
                history.add(new_position)
                counts[0] += 1
                find_adjasent(grid, new_position, history)


def step(grid: List[List[int]]) -> List[List[int]]:

    # increase energy level
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            grid[i][j] += 1

    flashed: Set[Position] = set()
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            new_position: Position = Position(i, j)
            if grid[i][j] > 9 and new_position not in flashed:
                flashed.add(new_position)
                counts[0] += 1
                # find adjasent & increase
                find_adjasent(grid, new_position, history=flashed)

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] > 9:
                grid[i][j] = 0


def print_grid(grid: List[List[int]]) -> None:
    print("---------")
    for row in grid:
        print(row)


def part_one(grid: List[List[int]]) -> int:

    for i in range(100):
        step(grid)

    return counts[0]


def all_flash(grid: List[List[int]]) -> bool:
    for row in grid:
        for i in row:
            if i > 0:
                return False
    return True


def part_two(grid: List[List[int]]) -> None:
    step_count: int = 0

    while (not all_flash(grid)):
        step(grid)
        step_count += 1

    return step_count


def read_input() -> List[List[int]]:
    with open('2021/11/input.txt', 'r') as file:
        return [
            [
                int(i) for i in line.strip()
            ] for line in file.readlines()
        ]


grid: List[List[int]] = read_input()


print(part_one(copy.deepcopy(grid)))
print(part_two(copy.deepcopy(grid)))
