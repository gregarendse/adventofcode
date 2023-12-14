#!/bin/python
from dataclasses import dataclass
from sys import argv
from typing import List


@dataclass
class Number(object):
    left = None
    right = None
    parent = None

    def explode(self):
        pass


def split(number: int) -> [int, int]:
    return [round((number / 2) - 0.5), round((number / 2) + 0.5)]


def read_file(file: str) -> List[str]:
    pass


def parse(input: str, stack) -> [int, int]:
    print('-----')
    print(input)
    if input[0] == '[':
        return parse(input[1:], None)
    left, right = input.split(',', 1)
    print(left)
    print(right)
    if left[0] == '[':
        left = parse(left[1:], None)
    if right[0] == '[':
        right = parse(right[1:], None)
    return [left, right]

def part_one(file: str) -> int:
    lines: List[str] = \
        """[1,2]
    [[1,2],3]
    [9,[8,7]]
    [[1,9],[8,5]]
    [[[[1,2],[3,4]],[[5,6],[7,8]]],9]
    [[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]
    [[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]""".splitlines()

    for line in lines:
        line = line.strip()
        print(line)
        left, right = parse(line, None)
        print("{} {}".format(left,right))




def part_two(file: str) -> int:
    pass


def main():
    print("Part One: {}".format(part_one(argv[1])))
    print("Part Two: {}".format(part_two(argv[1])))


if __name__ == '__main__':
    main()
