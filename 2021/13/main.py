#!/bin/python

from dataclasses import dataclass
from typing import Dict, List, Set
import statistics
import copy


def place_dots(dots: List) -> List[List[int]]:
    paper_size: int = 2046
    paper: List[List[int]] = [
        [0 for j in range(paper_size)] for i in range(paper_size)
    ]

    for dot in dots:
        x, y = dot.split(',')
        paper[int(y)][int(x)] = 1

    return paper


def fold(paper: List[List[int]], x: int = None, y: int = None) -> List[List[int]]:

    if y is not None:

        for i in range(y, len(paper)):
            for j in range(len(paper[i])):
                paper[i - y][j] += paper[(3 * y) - i][j]

        paper = paper[:y]

    if x is not None:

        for i in range(len(paper)):
            for j in range(x):
                paper[i][j] += paper[i][(2 * x) - j]
            paper[i] = paper[i][:x]

    return paper


def print_paper(paper: List[List[int]]) -> None:
    print("".join(['-' for i in paper[0]]))
    for row in paper:
        for item in row:
            print(('#' if item > 0 else '.'), end='')
        print()


def part_one(paper: List[List[int]], folds: List[str]) -> int:
    for line in folds:
        angle, value = line.split('=')
        if angle == 'y':
            paper = fold(paper, x=None, y=int(value))
        elif angle == 'x':
            paper = fold(paper, x=int(value), y=None)
        break

    count: int = 0
    for line in paper:
        for item in line:
            if item > 0:
                count += 1
    return count


def part_two(paper: List[List[int]], folds: List[str]) -> int:
    for line in folds:
        # print(line)
        angle, value = line.split('=')
        if angle == 'y':
            paper = fold(paper, x=None, y=int(value))
        elif angle == 'x':
            paper = fold(paper, x=int(value), y=None)

    print_paper(paper)


with open('2021/13/input.txt', 'r') as file:
    dots_coords, fold_lines = file.read().split('\n\n')

paper: List[List[int]] = place_dots(dots_coords.splitlines())
folds: List[str] = [x.split('fold along ')[1] for x in fold_lines.splitlines()]


print(part_one(copy.deepcopy(paper), folds))
print(part_two(copy.deepcopy(paper), folds))
