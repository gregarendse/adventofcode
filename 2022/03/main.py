#!/bin/python
from sys import argv
from typing import List


def read_file(file: str) -> List[str]:
    with open(file, 'r') as f:
        return f.readlines()


def part_one(file: str) -> int:
    lines: List[str] = read_file(file)

    ans: List[int] = []
    for line in lines:
        line = line.strip()
        length = int(len(line) / 2)

        first = set([str(x) for x in line[:length]])
        second = set([str(x) for x in line[length:]])

        both = first & second

        value: str = str(both.pop())

        if value.upper() == value:
            # upper case
            s = ord(value) - ord('A') + 27
            ans.append(s)
        else:
            # lower case
            s = ord(value) - ord('a') + 1
            ans.append(s)
    return sum(ans)


def part_two(file: str) -> int:
    lines: List[str] = read_file(file)

    ans: List[int] = []

    for i in range(0, len(lines), 3):

        first = set([str(x) for x in lines[i].strip()])
        second = set([str(x) for x in lines[i + 1].strip()])
        third = set([str(x) for x in lines[i + 2].strip()])

        both = first & second & third
        value: str = str(both.pop())

        if value.upper() == value:
            # upper case
            s = ord(value) - ord('A') + 27
            ans.append(s)
        else:
            # lower case
            s = ord(value) - ord('a') + 1
            ans.append(s)
    return sum(ans)


def main():
    print("Part One: {}".format(part_one(argv[1])))
    print("Part Two: {}".format(part_two(argv[1])))


if __name__ == '__main__':
    main()
