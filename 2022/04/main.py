#!/bin/python
from sys import argv
from typing import List


def read_file(file: str) -> List[str]:
    with open(file, 'r') as f:
        return f.readlines()


def part_one(file: str) -> int:
    lines: List[str] = read_file(file)

    sections: List[List[List[int]]] = []
    for line in lines:
        parts: List[str] = line.split(',')

        section_ids: List[int] = []
        sections.append(section_ids)

        for part in parts:
            section: List[str] = part.split('-')
            section_ids.append(
                [x for x in range(int(section[0]), int(section[1]) + 1)]
            )

    overlap = 0
    for section in sections:
        if len(set(section[0]) - set(section[1])) == 0 or len(set(section[1]) - set(section[0])) == 0:
            overlap += 1
    return overlap

def part_two(file: str) -> int:
    lines: List[str] = read_file(file)

    sections: List[List[List[int]]] = []
    for line in lines:
        parts: List[str] = line.split(',')

        section_ids: List[int] = []
        sections.append(section_ids)

        for part in parts:
            section: List[str] = part.split('-')
            section_ids.append(
                [x for x in range(int(section[0]), int(section[1]) + 1)]
            )

    overlap = 0
    for section in sections:
        if len(set(section[0]) & set(section[1])) > 0 or len(set(section[1]) & set(section[0])) > 0:
            overlap += 1
    return overlap

def main():
    print("Part One: {}".format(part_one(argv[1])))
    print("Part Two: {}".format(part_two(argv[1])))


if __name__ == '__main__':
    main()
