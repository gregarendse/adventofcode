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
        # for (ddx, ddy) in [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]:
        for (ddx, ddy) in [(0, 1), (0, -1)]:
            points.add((ddx + dx, ddy))
    return sorted(list(points))


def __part_one__(file: Path) -> int:
    lines = read_from_file(file)
    characters: Dict[str, int] = defaultdict(int)

    part_numbers = []

    for y, line in enumerate(lines):
        x: int = 0
        while x < len(line):
            characters[line[x]] += 1

            dx: int = 1
            while x + dx + 1 < len(line) and str(line[x:x + dx + 1]).isnumeric():
                dx += 1

            if str(line[x:x + dx]).isnumeric():
                n = int(line[x:x + dx])

                points = get_points(dx)
                print(f"{n} -> {points}")

                for (ddx, ddy) in points:
                    if 0 <= y + ddy < len(lines):
                        pass
                    else:
                        continue

                    if 0 <= x + ddx < len(lines[y + ddy]):
                        pass
                    else:
                        continue

                    c = lines[y + ddy][x + ddx]

                    if str(c).isnumeric():
                        continue

                    if c != '.':
                        part_numbers.append(n)
                        break

            x += dx

    for k, v in characters.items():
        print(f"{k} {v}")
    return sum(part_numbers)


def __part_two__(file: Path) -> int:
    raise Exception("Not implemented")
    content: str = read_from_file(file)
    return 0


def part_one() -> int:
    example: int = __part_one__(PARENT.joinpath('example.txt'))
    assert example == 4361
    answer: int = __part_one__(PARENT.joinpath('input.txt'))
    return answer


def part_two() -> int:
    # example: int = __part_two__(PARENT.joinpath('example.txt'))
    # assert example == 0
    # answer: int = __part_two__(PARENT.joinpath('input.txt'))
    return None


def main():
    print("Part One: {}".format(part_one()))
    print("Part Two: {}".format(part_two()))


if __name__ == '__main__':
    main()
