#!/use/bin/env python

from sys import argv
from typing import List, Dict


def read_file(file: str) -> [List[str]]:
    with open(file, 'r') as f:
        return f.readlines()


def part_one(file: str) -> int:
    lines: List[str] = read_file(file)

    message_counter: List[Dict[str, int]] = [dict() for x in lines[0].strip()]

    for i, line in enumerate(lines):
        line = line.strip()
        for j, c in enumerate(line):
            if message_counter[j].get(c) is None:
                message_counter[j][c] = 1
            else:
                message_counter[j][c] += 1

    word: str = ""
    for c in message_counter:
        max: int = 0
        letter: str = None
        for k, v in c.items():
            if v > max:
                max = v
                letter = k
        word += letter

    return word


def part_two(file: str) -> int:
    lines: List[str] = read_file(file)

    message_counter: List[Dict[str, int]] = [dict() for x in lines[0].strip()]

    for i, line in enumerate(lines):
        line = line.strip()
        for j, c in enumerate(line):
            if message_counter[j].get(c) is None:
                message_counter[j][c] = 1
            else:
                message_counter[j][c] += 1

    word: str = ""
    for c in message_counter:
        max: int = 99999999
        letter: str = None
        for k, v in c.items():
            if v < max:
                max = v
                letter = k
        word += letter

    return word


def main():
    print("Part One: {}".format(part_one(argv[1])))
    print("Part Two: {}".format(part_two(argv[1])))


if __name__ == '__main__':
    main()
