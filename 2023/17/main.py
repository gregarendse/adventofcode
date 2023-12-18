#!/usr/bin/env python
from collections import deque
from pathlib import Path
from typing import List, Tuple, Set

PARENT = Path(__file__).parent


def read_from_file(file: Path) -> list[list[int]]:
    heat_loss_map: List[List[int]] = []
    with open(file) as f:
        for line in f.readlines():
            heat_loss_map.append(
                [int(c) for c in line.strip()]
            )
    return heat_loss_map


def shortest_path(start: Tuple[int, int], end: Tuple[int, int], heat_loss_map: list[list[int]]) -> int:
    q: deque[Tuple[Tuple[int, int], int]] = deque([(start, 0)])
    history: Set[Tuple[int, int]] = set()

    while q:
        position, count = q.popleft()

        if position == end:
            return count

        for (dx, dy) in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            position_next: Tuple[int, int] = (position[0] + dx, position[1] + dy)

            if 0 <= position_next[1] < len(heat_loss_map) \
                    and 0 <= position_next[0] < len(heat_loss_map[position_next[1]]) \
                    and position_next not in history:
                q.append((position_next, count + 1))
                history.add(position_next)
    raise Exception("Not Found :(")


def __part_one__(file: Path) -> int:
    heat_loss_map: list[list[int]] = read_from_file(file)
    start: Tuple[int, int] = (0, 0)
    end: Tuple[int, int] = (len(heat_loss_map), len(heat_loss_map[-1]))
    count: int = shortest_path(start=start, end=end, heat_loss_map=heat_loss_map)
    return 0


def __part_two__(file: Path) -> int:
    raise Exception("Not implemented")
    content: str = read_from_file(file)
    return 0


def part_one() -> int:
    example: int = __part_one__(PARENT.joinpath('example.txt'))
    assert example == 102
    answer: int = __part_one__(PARENT.joinpath('input.txt'))
    return answer


def part_two() -> int:
    example: int = __part_two__(PARENT.joinpath('example.txt'))
    assert example == 0
    answer: int = __part_two__(PARENT.joinpath('input.txt'))
    return answer


def main():
    print("Part One: {}".format(part_one()))
    print("Part Two: {}".format(part_two()))


if __name__ == '__main__':
    main()
