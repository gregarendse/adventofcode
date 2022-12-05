#!/bin/python
from sys import argv
from typing import List


def read_file(file: str) -> List[str]:
    with open(file, 'r') as f:
        return f.readlines()


points = {
    'X': 1,
    'Y': 2,
    'Z': 3,
    'A': 1,
    'B': 2,
    'C': 3
}


# A/X - Rock        1
# B/Y - Paper       2
# C/Z - Scissors    3


def calculat_points(left: int, right: int) -> int:
    print(points.get(left))
    print(points.get(right))
    if points.get(left) == points.get(right):
        return points.get(right) + 3  # Draw
    if (points.get(left) - points.get(right)) % 3 > 1:
        return points.get(right) + 6
    else:
        return points.get(right)


def part_one(file: str) -> int:
    lines: List[str] = read_file(file)
    points: List[int] = []
    for line in lines:
        [left, right] = line.split(' ')
        point = calculat_points((left.strip()), (right.strip()))
        print(point)
        points.append(point)
    return sum(points)


def part_two(file: str) -> int:
    lines: List[str] = read_file(file)
    _points: List[int] = []
    for line in lines:
        [left, right] = line.split(' ')

        play: int = (points.get(left.strip()) + points.get(right.strip())) % 3 + 1
        score: int = 0

        if points.get(left.strip()) == play:
            score = play + 3  # Draw
        elif (points.get(left.strip()) - play) % 3 == 2:
            score = play + 6
        else:
            score = play

        print(play)
        print(score)
        print()
        _points.append(score)
    return sum(_points)


def main():
    print("Part One: {}".format(part_one(argv[1])))
    print("Part Two: {}".format(part_two(argv[1])))


if __name__ == '__main__':
    main()
