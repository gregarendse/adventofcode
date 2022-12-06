#!/use/bin/env python

from sys import argv
from typing import List, Tuple


def read_file(file: str) -> List[List[str]]:
    with open(file, 'r') as f:
        map: List[List[str]] = []
        for line in f.readlines():
            line = line.strip()
            row: List[str] = []
            for l in line:
                row.append(l)
            map.append(row)
        return map


def print_map(map: List[List[str]]) -> None:
    for row in map:
        for column in row:
            print(column, end='')
        print()


def move(map: List[List[str]], direction: str) -> List[List[str]]:
    movable: List[Tuple[int, int]] = []

    height: int = len(map)
    for row in range(len(map)):
        width: int = len(map[row])
        for column in range(width):
            if direction == 'east':
                if map[row][column] == '>':
                    if map[row][(column + 1) % width] == '.':
                        movable.append((row, column))
            if direction == 'south':
                if map[row][column] == 'v':
                    if map[(row + 1) % height][column] == '.':
                        movable.append((row, column))

    for m in movable:
        if direction == 'east':
            map[m[0]][(m[1] + 1) % width] = map[m[0]][m[1]]
            map[m[0]][m[1]] = '.'
        elif direction == 'south':
            map[(m[0] + 1) % height][m[1]] = map[m[0]][m[1]]
            map[m[0]][m[1]] = '.'

    return len(movable)


def move_east(map: List[List[str]]) -> List[List[str]]:
    return move(map, 'east')


def move_south(map: List[List[str]]) -> List[List[str]]:
    return move(map, 'south')


def part_one(file: str) -> int:
    map: List[List[str]] = read_file(file)

    counter: int = 0
    moves: int = 1
    while moves != 0:
        counter += 1
        moves = 0
        moves += move_east(map)
        moves += move_south(map)

    return counter


def part_two(file: str) -> int:
    pass


def main():
    print("Part One: {}".format(part_one(argv[1])))
    print("Part Two: {}".format(part_two(argv[1])))


if __name__ == '__main__':
    main()
