#!/use/bin/env python

from dataclasses import dataclass
from sys import argv
from typing import List, Set


def read_file(file: str) -> List[List[int]]:
    with open(file, 'r') as f:
        elevation_map: List[List[int]] = []
        for line in f.readlines():
            line = line.strip()
            row: List[int] = []
            for l in line:
                row.append(ord(l))
            elevation_map.append(row)
        return elevation_map


def print_map(elevation_map: List[List[int]]):
    for row in elevation_map:
        for column in row:
            print(chr(column), end="")
        print()


@dataclass
class Position(object):
    x: int
    y: int
    height: int
    previous: object

    def __str__(self):
        return "x={},y={} {}".format(self.x, self.y, chr(self.height))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.x) + hash(self.y)


def find(elevation_map: List[List[int]], thing: str) -> Position:
    for y in range(len(elevation_map)):
        for x in range(len(elevation_map[y])):
            if chr(elevation_map[y][x]) == thing:
                return Position(x, y, elevation_map[y][x], None)
    print("not found: " + thing)


def path(elevation_map: List[List[int]], start: Position, dest: Position) -> Position:
    visited: Set[Position] = set()
    next: List[Position] = []

    visited.add(start)
    next.append(start)

    while len(next) > 0:
        p: Position = next.pop(0)
        max_height: int = (p.height + 1)

        up_y: int = p.y - 1
        # up_y: int = (p.y - 1) % len(elevation_map)

        if len(elevation_map) > up_y >= 0:
            if max_height >= elevation_map[up_y][p.x]:
                down = Position(
                    y=up_y,
                    x=p.x,
                    height=elevation_map[up_y][p.x],
                    previous=p
                )

                if down == dest:
                    return down

                if down not in visited:
                    visited.add(down)
                    next.append(down)

        left_x = p.x - 1  # (p.x - 1) % len(elevation_map[0])
        if len(elevation_map[p.y]) > left_x >= 0:
            if max_height >= elevation_map[p.y][left_x]:
                # Left
                left = Position(
                    y=p.y,
                    x=left_x,
                    height=elevation_map[p.y][left_x],
                    previous=p
                )

                if left == dest:
                    return left

                if left not in visited:
                    visited.add(left)
                    next.append(left)

        # down_y = (p.y + 1) % len(elevation_map)
        down_y = p.y + 1
        if len(elevation_map) > down_y >= 0:
            if max_height >= elevation_map[down_y][p.x]:
                # Up
                up = Position(
                    y=down_y,
                    x=p.x,
                    height=elevation_map[down_y][p.x],
                    previous=p
                )

                if up == dest:
                    return up

                if up not in visited:
                    visited.add(up)
                    next.append(up)

        # right_x = (p.x + 1) % len(elevation_map[0])
        right_x = p.x + 1
        if len(elevation_map[p.y]) > right_x >= 0:
            if max_height >= elevation_map[p.y][right_x]:
                # Right
                right = Position(
                    y=p.y,
                    x=right_x,
                    height=elevation_map[p.y][right_x],
                    previous=p
                )

                if right == dest:
                    return right

                if right not in visited:
                    visited.add(right)
                    next.append(right)


def part_one(file: str) -> int:
    elevation_map: List[List[int]] = read_file(file)
    start: Position = find(elevation_map, "S")
    elevation_map[start.y][start.x] = ord("a")
    start.height = ord("a")

    dest: Position = find(elevation_map, "E")
    elevation_map[dest.y][dest.x] = ord("z")

    d: Position = path(elevation_map, start, dest)

    length: int = 0
    previous: Position = d.previous
    while previous is not None:
        previous = previous.previous
        length += 1

    return length


def part_two(file: str) -> int:
    elevation_map: List[List[int]] = read_file(file)

    dest: Position = find(elevation_map, "E")
    elevation_map[dest.y][dest.x] = ord("z")

    S: Position = find(elevation_map, "S")
    elevation_map[S.y][S.x] = ord("a")

    start_points: List[Position] = []
    for y in range(len(elevation_map)):
        for x in range(len(elevation_map[y])):
            if chr(elevation_map[y][x]) == "a":
                start_points.append(Position(x, y, elevation_map[y][x], None))

    distances: List[int] = []
    for start in start_points:
        d: Position = path(elevation_map, start, dest)
        if d is None:
            continue
        length: int = 0
        previous: Position = d.previous
        while previous is not None:
            previous = previous.previous
            length += 1
        distances.append(length)

    return min(distances)


def main():
    print("Part One: {}".format(part_one(argv[1])))
    print("Part Two: {}".format(part_two(argv[1])))


if __name__ == '__main__':
    main()
