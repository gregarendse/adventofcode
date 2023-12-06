#!/usr/bin/env python
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set, Tuple

PARENT = Path(__file__).parent


def read_from_file(file: Path):
    with open(file) as f:
        return [line.strip() for line in f.readlines()]
        symbols = []
        numbers = defaultdict(int)

        for y, line in enumerate(f.readlines()):
            for x, c in enumerate(line):
                if not c.isnumeric() and c != '.':
                    symbols.append((x, y))

            x: int = 0
            while x < len(line):
                dx = 1
                while str(line[x:x + dx + 1]).isnumeric() and x + dx < len(line):
                    dx += 1

                if str(line[x:x + dx]).isnumeric():
                    n = int(line[x:x + dx])
                    for ddx in range(dx):
                        numbers[(x + ddx, y)] = n
                x += dx

        return symbols, numbers


def get_points(i: int = 0) -> List[Tuple[int, int]]:
    points: Set[Tuple[int, int]] = set()

    # Left
    points.add((-1, 1))
    points.add((-1, 0))
    points.add((-1, -1))

    # Right
    points.add((i, 1))
    points.add((i, 0))
    points.add((i, -1))

    # Top & Bottom
    for dx in range(i):
        for (ddx, ddy) in [(0, 1), (0, -1)]:
            points.add((ddx + dx, ddy))
    return sorted(list(points))


def __part_one__(file: Path) -> int:
    lines = read_from_file(file)
    part_numbers = []

    for y, line in enumerate(lines):
        x: int = 0
        while x < len(line):
            dx: int = 0
            while x + dx + 1 <= len(line) and str(line[x:x + dx + 1]).isnumeric():
                dx += 1

            if dx == 0:
                x += 1
                continue

            if str(line[x:x + dx]).isnumeric():
                n = int(line[x:x + dx])

                points = get_points(dx)

                around = []

                for (ddx, ddy) in points:
                    print(f"{x + ddx},{y + ddy}")
                    if 0 <= y + ddy < len(lines) and 0 <= x + ddx < len(lines[y + ddy]):
                        pass
                    else:
                        continue

                    c: str = str(lines[y + ddy][x + ddx])

                    around.append(c)

                    if c == '.' or c.isnumeric():
                        continue

                if len(list(filter(lambda x: str(x) != '.' and not str(x).isnumeric(), around))) > 0:
                    part_numbers.append(n)
                print(f"{n} -> {around}")

            x += dx

    return sum(part_numbers)


def __part_two__(file: Path) -> int:
    lines = read_from_file(file)
    gears: Dict[Tuple[int, int], List[int]] = defaultdict(list)

    for y, line in enumerate(lines):
        x: int = 0
        while x < len(line):
            dx: int = 0
            while x + dx + 1 <= len(line) and str(line[x:x + dx + 1]).isnumeric():
                dx += 1

            if dx == 0:
                x += 1
                continue

            if str(line[x:x + dx]).isnumeric():
                n = int(line[x:x + dx])

                points = get_points(dx)

                around = []

                for (ddx, ddy) in points:
                    if 0 <= y + ddy < len(lines) and 0 <= x + ddx < len(lines[y + ddy]):
                        pass
                    else:
                        continue

                    c: str = str(lines[y + ddy][x + ddx])

                    if c == '*':
                        gears[(x + ddx, y + ddy)].append(n)
                        break

            x += dx

    total: int = 0

    for part_numbers in gears.values():
        if len(part_numbers) != 2:
            continue
        ans: int = 1
        for part_number in part_numbers:
            ans *= part_number
        total += ans

    return total


def part_one() -> int:
    example: int = __part_one__(PARENT.joinpath('example.txt'))
    assert example == 4361
    example: int = __part_one__(PARENT.joinpath('example_2.txt'))
    assert example == 9 + 633 + 63
    answer: int = __part_one__(PARENT.joinpath('input.txt'))
    return answer


def part_two() -> int:
    example: int = __part_two__(PARENT.joinpath('example.txt'))
    assert example == 467835
    answer: int = __part_two__(PARENT.joinpath('input.txt'))
    return answer


def main():
    print("Part One: {}".format(part_one()))
    print("Part Two: {}".format(part_two()))


if __name__ == '__main__':
    main()
