#!/usr/bin/env python
from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set

PARENT = Path(__file__).parent


@dataclass
class Point(object):
    x: int
    y: int

    pipe: str = None

    def __hash__(self):
        return hash(self.x) + hash(self.y)

    def __add__(self, other):
        return Point(
            x=(self.x + other.x),
            y=(self.y + other.y)
        )

    def __sub__(self, other):
        return Point(
            x=(self.x - other.x),
            y=(self.y - other.y)
        )

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


def read_from_file(file: Path) -> dict[Point, str]:
    points: List[Point] = []
    point_map: Dict[Point, str] = defaultdict(str)
    with open(file) as f:
        for y, line in enumerate(f.readlines()):
            for x, c in enumerate(line.strip()):
                point = Point(x=int(x), y=int(y), pipe=str(c))
                points.append(point)
                point_map[point] = str(c)
    return point_map


def compatible(position: Point, move: Point) -> bool:
    """
    | is a vertical pipe connecting north and south.
    - is a horizontal pipe connecting east and west.
    L is a 90-degree bend connecting north and east.
    J is a 90-degree bend connecting north and west.
    7 is a 90-degree bend connecting south and west.
    F is a 90-degree bend connecting south and east.
    . is ground; there is no pipe in this tile.
    S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
    """

    pipe_map: Dict[str, int] = {
        'S': 0b1111,
        '|': 0b1010,
        '-': 0b0101,
        'L': 0b1100,
        'J': 0b1001,
        '7': 0b0011,
        'F': 0b0110,
        '.': 0b0000
    }

    movement_map: Dict[str, bool] = {
        '--': True,
        '|\n|': True,
        'S|': False,
        '|S': False,
        'S\n|': True,
        '|\nS': True,
        'S-': True,
        '-S': True,
        'S\n-': False,
        '-\nS': False,
        'SL': False,
        'LS': True,
        'S\nL': True,
        'L\nS': False,
        'SJ': True,
        'JS': False,
        'S\nJ': True,
        'J\nS': False,
        'S7': True,
        '7S': False,
        'S\n7': True,
        '7\nS': False,
        'SF': False,
        'FS': True,
        'S\nF': False,
        'F\nS': True,
        '|-': False,
        '-|': False,
        '|\n-': False,
        '-\n|': False,
        '|L': False,
        'L|': False,
        '|\nL': True,
        'L\n|': False,
        '|J': False,
        'J|': False,
        '|\nJ': True,
        'J\n|': False,
        '|7': False,
        '7|': False,
        '|\n7': False,
        '7\n|': True,
        '|F': False,
        'F|': False,
        '|\nF': False,
        'F\n|': True,
        '-L': False,
        'L-': True,
        '-\nL': False,
        'L\n-': False,
        '-J': True,
        'J-': False,
        '-\nJ': False,
        'J\n-': False,
        '-7': True,
        '7-': False,
        '-\n7': False,
        '7\n-': False,
        '-F': False,
        'F-': True,
        '-\nF': False,
        'F\n-': False,
        'LJ': True,
        'JL': False,
        'L\nJ': True,
        'J\nL': False,
        'L7': True,
        '7L': False,
        'L\n7': False,
        '7\nL': True,
        'LF': False,
        'FL': False,
        'L\nF': False,
        'F\nL': True,
        'J7': False,
        '7J': False,
        'J\n7': False,
        '7\nJ': True,
        'JF': False,
        'FJ': True,
        'J\nF': False,
        'F\nJ': True,
        '7F': False,
        'F7': True,
        '7\nF': False,
        'F\n7': True
    }

    d: Point = move - position
    """
    (x1,y1) - (x2,y2) = (dx, dy)
    
               0,1  (0,-dy)
                N
                |
                |
(-dx,0) -1,0 W-- --E 1,0 (+dx,0)
                |
                |
                S
               0,-1 (0,+dy)
    """
    current_pipe_connections: int = pipe_map.get(position.pipe)
    next_pipe_connections: int = pipe_map.get(move.pipe)

    possible: int = 0b1111

    if d.y == -1:
        # North (0,1)
        return bool(current_pipe_connections & 0b1000) \
            and bool(next_pipe_connections & 0b0010)
    elif d.x == 1:
        # East (1,0)
        return bool(current_pipe_connections & 0b0100) \
            and bool(next_pipe_connections & 0b0001)
    elif d.y == 1:
        # South (0,-1)
        return bool(current_pipe_connections & 0b0010) \
            and bool(next_pipe_connections & 0b1000)
    elif d.x == -1:
        # West (-1,0)
        return bool(current_pipe_connections & 0b0001) \
            and bool(next_pipe_connections & 0b0100)
    else:
        raise Exception

    return bool(possible)


def find_path(start: Point, point_map: Dict[Point, str]) -> Optional[int]:
    seen: Set[Point] = set()
    q: deque[tuple[Point, int]] = deque([(start, 0)])
    max_distance: int = 0

    while q:

        position, distance = q.popleft()
        seen.add(position)
        max_distance = max(max_distance, distance)

        for move in [Point(x=1, y=0), Point(x=0, y=1), Point(x=-1, y=0), Point(x=0, y=-1)]:
            position_next = position + move
            if position_next not in seen and position_next in point_map:
                pipe_next: str = point_map.get(position_next)
                position_next.pipe = pipe_next

                if position_next.pipe == '.':
                    pass
                elif compatible(position, position_next):
                    q.append((position_next, distance + 1))
                    seen.add(position_next)

    return max_distance


def follow(start: Point, point_map: Dict[Point, str]) -> list[Point]:
    seen: Set[Point] = set()
    q: deque[tuple[Point, int]] = deque([(start, 0)])
    max_distance: int = 0
    path: List[Point] = []

    while q:

        position, distance = q.popleft()
        seen.add(position)
        max_distance = max(max_distance, distance)

        for move in [Point(x=0, y=-1), Point(x=1, y=0), Point(x=0, y=1), Point(x=-1, y=0)]:
            position_next = position + move
            if position_next not in seen and position_next in point_map:
                pipe_next: str = point_map.get(position_next)
                position_next.pipe = pipe_next

                if position_next.pipe == '.':
                    pass
                elif compatible(position, position_next):
                    path.append(position)
                    q.append((position_next, distance + 1))
                    seen.add(position_next)
                    break

    return path


def __part_one__(file: Path) -> int:
    point_map: dict[Point, str] = read_from_file(file)
    start: Point
    for key, value in point_map.items():
        if key.pipe == 'S':
            start = key
            break
    distance: int = find_path(start=start, point_map=point_map)
    return distance


def __part_two__(file: Path) -> int:
    point_map: dict[Point, str] = read_from_file(file)
    start: Optional[Point] = None
    for key, value in point_map.items():
        if key.pipe == 'S':
            start = key
            break
    path: list[Point] = follow(start=start, point_map=point_map)
    return None


def part_one() -> int:
    # example: int = __part_one__(PARENT.joinpath('example.txt'))
    # assert example == 4

    example: int = __part_one__(PARENT.joinpath('example_2.txt'))
    assert example == 8

    answer: int = __part_one__(PARENT.joinpath('input.txt'))
    return answer


def part_two() -> int:
    example: int = __part_two__(PARENT.joinpath('example.txt'))
    assert example == 1

    example: int = __part_two__(PARENT.joinpath('example_3.txt'))
    assert example == 4

    example: int = __part_two__(PARENT.joinpath('example_4.txt'))
    assert example == 8

    example: int = __part_two__(PARENT.joinpath('example_5.txt'))
    assert example == 10

    answer: int = __part_two__(PARENT.joinpath('input.txt'))
    return answer


def main():
    # print("Part One: {}".format(part_one()))
    print("Part Two: {}".format(part_two()))


if __name__ == '__main__':
    main()
