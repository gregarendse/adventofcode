#!/bin/python
from sys import argv
from typing import List, Dict


def read_file(file: str) -> [List[List[str]], List[str]]:
    with open(file, 'r') as f:
        [ship, moves] = f.read().split('\n\n')

    stacks: List[List[str]] = []
    places: Dict[int, int] = dict()

    for i, value in enumerate(ship.splitlines()[-1]):
        if value == ' ':
            continue
        stacks.append([])
        places[int(i)] = int(value)

    for create in ship.splitlines()[:-1]:
        for i, stack in enumerate(create):
            if stack == '[' or stack == ' ' or stack == ']':
                continue
            stacks[places.get(i) - 1].append(str(stack))

    return stacks, moves.splitlines()


def part_one(file: str) -> str:
    [stacks, moves] = read_file(file)

    for move in moves:
        parts: list[str] = move.split(" ")
        count: int = int(parts[1])
        f: int = int(parts[3]) - 1
        t: int = int(parts[5]) - 1

        # print("move {} from {} to {}".format(count, f, t))

        part = stacks[f][:count]
        part.reverse()
        stacks[f] = stacks[f][count:]
        stacks[t] = part[:] + stacks[t]

    code: str = ""
    for stack in stacks:
        code += stack[0]

    return code


def part_two(file: str) -> str:
    [stacks, moves] = read_file(file)

    for move in moves:
        parts: list[str] = move.split(" ")
        count: int = int(parts[1])
        f: int = int(parts[3]) - 1
        t: int = int(parts[5]) - 1

        # print("move {} from {} to {}".format(count, f, t))

        part = stacks[f][:count]
        stacks[f] = stacks[f][count:]
        stacks[t] = part[:] + stacks[t]

    code: str = ""
    for stack in stacks:
        code += stack[0]

    return code


def main():
    print("Part One: {}".format(part_one(argv[1])))
    print("Part Two: {}".format(part_two(argv[1])))


if __name__ == '__main__':
    main()
