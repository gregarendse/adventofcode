#!/usr/bin/env python
from collections import deque, defaultdict
from copy import copy
from pathlib import Path
from typing import List, Tuple, Dict

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
    q: deque[Tuple[Tuple[int, int], List[int], List[Tuple[int, int]], List[Tuple[int, int]]]] = deque(
        [(start, [], [], [])])
    min_map: Dict[Tuple[int, int], int] = defaultdict(lambda: 999999999)

    while q:
        (x, y), heat_losses, moves, history = q.popleft()

        heat_loss = sum(heat_losses)
        if heat_loss > min_map[(x, y)]:
            continue
        else:
            min_map[(x, y)] = heat_loss
            final_state = heat_losses

        for (dx, dy) in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            (x_next, y_next) = (x + dx, y + dy)

            momentum: list[tuple[int, int]] = moves[max(len(moves) - 3, 0):]

            if 0 <= y_next < len(heat_loss_map) \
                    and 0 <= x_next < len(heat_loss_map[y_next]) \
                    and (x_next, y_next) not in history \
                    and ((len(momentum) < 3) or (len(set(momentum)) > 1) or (dx, dy) not in momentum):
                moves.append((dx, dy))
                history.append((x, y))
                heat_losses.append(heat_loss_map[y_next][x_next])
                q.append(
                    (
                        (x_next, y_next),
                        copy(heat_losses),
                        copy(moves),
                        copy(history)
                    )
                )

    return min_map[end]


def __part_one__(file: Path) -> int:
    heat_loss_map: list[list[int]] = read_from_file(file)
    start: Tuple[int, int] = (0, 0)
    end: Tuple[int, int] = (len(heat_loss_map) - 1, len(heat_loss_map[-1]) - 1)
    count: int = shortest_path(start=start, end=end, heat_loss_map=heat_loss_map)
    return count


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
