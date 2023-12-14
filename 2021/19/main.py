#!/use/bin/env python
from dataclasses import dataclass
from sys import argv
from typing import List, Set


@dataclass
class Position:
    x: int
    y: int
    z: int


def read_file(file: str) -> List[List[Position]]:
    with open(file, 'r') as f:
        scanners: List[List[Position]] = []
        for scanner in f.read().split('\n\n'):
            beacons: List[Position] = []
            for beacon in scanner.splitlines()[1:]:
                [x, y, z] = beacon.split(',')
                beacons.append(Position(int(x), int(y), int(z)))
            scanners.append(beacons)

        return scanners


def print_map(map: List[List[list[int]]]) -> None:
    for row in map:
        for column in row:
            print(column, end='')
        print()


def calculate_distance(one: Position, two: Position) -> int:
    return abs(abs(one.z) - abs(two.z)) + abs(abs(one.x) - abs(two.x)) + abs(abs(one.y) - abs(two.y))
    # return abs(one.x * one.x - two.x * two.x + one.y * one.y - two.y * two.y + one.z * one.z - two.z * two.z)


def part_one(file: str) -> int:
    scanners: List[List[Position]] = read_file(file)

    unique_beacons: Set[int] = set()

    for scanner in scanners:
        print(scanner)
        for beacon in scanner:
            print(beacon)
            distances: List[int] = []
            for other_beacon in scanner:
                distance: int = calculate_distance(beacon, other_beacon)
                distances.append(distance)
                unique_beacons.add(distance)
            distances.sort()
            print(distances)
            print()

    print(unique_beacons)
    print(len(unique_beacons))

    return 0


def part_two(file: str) -> int:
    pass


def main():
    print("Part One: {}".format(part_one(argv[1])))
    print("Part Two: {}".format(part_two(argv[1])))


if __name__ == '__main__':
    main()
