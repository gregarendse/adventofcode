#!/use/bin/env python

from sys import argv
from typing import List


def read_file(file: str) -> [List[str]]:
    with open(file, 'r') as f:
        return f.readlines()


def part_one(file: str) -> int:
    lines: List[str] = read_file(file)

    for line in lines:
        for i in range(len(line) - 4):
            part: str = line[i:i + 4]
            if len(part) == len(set(part)):
                return i + 4


def part_two(file: str) -> int:
    lines: List[str] = read_file(file)

    for line in lines:
        for i in range(len(line) - 14):
            part: str = line[i:i + 14]
            if len(part) == len(set(part)):
                return i + 14


def main():
    print("Part One: {}".format(part_one(argv[1])))
    print("Part Two: {}".format(part_two(argv[1])))


if __name__ == '__main__':
    main()
