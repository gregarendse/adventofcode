#!/bin/python
from sys import argv
from typing import List


def read_file(file: str) -> List[str]:
    with open(file, 'r') as file:
        elves = file.read().split('\n\n')
        return elves


def calculate_calories(file) -> List[int]:
    calories: List[int] = []
    for elf in read_file(file):
        calories.append(sum([int(x) for x in elf.splitlines()]))
    return calories


def part_one(file: str) -> int:
    calories: List[int] = calculate_calories(file)
    return max(calories)


def part_two(file: str) -> int:
    calories: List[int] = calculate_calories(file)
    return sum(sorted(calories)[-3:])


def main():
    print("Part One: {}".format(part_one(argv[1])))
    print("Part Two: {}".format(part_two(argv[1])))


if __name__ == '__main__':
    main()
