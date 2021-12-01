#!/bin/python

from typing import List


def part_one(lines: List[str]) -> str:
    larger: int = 0
    for i in range(1, len(lines)):
        print("{} : {}".format(i, lines[i]))
        if int(lines[i]) > int(lines[i - 1]):
            larger = larger + 1
    return larger


def sliding_window(lines: List[str]) -> int:
    sum: int = 0
    for i in range(3):
        sum = sum + int(lines[i])
    return sum


def part_two(lines: List[str]) -> str:
    larger: int = 0

    for i in range(1, len(lines) - 2):

        if sliding_window(lines[i:]) > sliding_window(lines[i-1:]):
            larger = larger + 1

    return larger


with open('2021/01/input.txt', 'r') as file:
    lines = file.readlines()

    print(part_one(lines))
    print(part_two(lines))
