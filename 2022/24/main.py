#!/usr/bin/env python
from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

PARENT = Path(__file__).parent


@dataclass
class Blizzard(object):
    x: int
    y: int
    direction: str


def read_from_file(file: Path) -> tuple[dict[tuple[int, int], list[str]], int, int]:
    with open(file) as f:
        valley_map: Dict[Tuple[int, int], List[str]] = defaultdict(list)

        lines: list[str] = f.readlines()
        for i, line in enumerate(lines):
            line = str(line).strip()
            for j, c in enumerate(line):
                if c in ["<", "^", ">", "v"]:
                    valley_map[(j, i)].append(c)
                elif str(c).isdigit():
                    for _ in range(int(c)):
                        valley_map[(j, i)].append("?")

        return valley_map, j, i


def blizzard(valley: dict[tuple[int, int], list[str]], max_x: int, max_y: int) -> dict[tuple[int, int], list[str]]:
    next_valley: dict[tuple[int, int], list[str]] = defaultdict(list)

    for position, blizzards in valley.items():
        for b in blizzards:
            x, y = position

            if ">" == b:
                if x + 1 == max_x:
                    x = 1
                else:
                    x += 1
            elif "<" == b:
                if x - 1 == 0:
                    x = max_x - 1
                else:
                    x -= 1
            elif "^" == b:
                if y - 1 == 0:
                    y = max_y - 1
                else:
                    y -= 1
            elif "v" == b:
                if y + 1 == max_y:
                    y = 1
                else:
                    y += 1

            next_valley[(x, y)].append(b)

    return next_valley


def path_finder(
        position: tuple[int, int],
        target: tuple[int, int],
        states: List[dict[tuple[int, int], list[str]]],
        max_x: int,
        max_y: int,
        minute: int = 0
) -> int:
    history: Dict[Tuple[Tuple[int, int], int], int] = defaultdict(lambda: 999999999)
    q: deque[tuple[tuple[int, int], int]] = deque([(position, minute % len(states))])

    while q:
        position, minute = q.popleft()

        if position == target:
            return minute

        # Cycle over the number of different states we have
        state_i = minute % len(states)
        minute_next: int = minute + 1

        valley = states[state_i]
        x, y = position

        for dx, dy in [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1)]:
            position_next = (x + dx, y + dy)
            if (0 < x + dx < max_x
                    and 0 < y + dy < max_y
                    and len(valley[position_next]) == 0
                    and history[(position_next, state_i)] > minute_next):
                q.append((position_next, minute_next))
                history[(position_next, state_i)] = minute_next
        if not q and len(valley[position_next]) == 0:
            q.append((position, minute_next))

    raise Exception("No path found")


def resolve_states(
        valley: dict[tuple[int, int], list[str]],
        max_x: int,
        max_y: int
) -> list[dict[tuple[int, int], list[str]]]:
    states: list[dict[tuple[int, int], list[str]]] = []
    while valley not in states:
        states.append(valley)
        valley = blizzard(valley, max_x, max_y)
    return states


def __part_one__(file: Path) -> int:
    valley: dict[tuple[int, int], list[str]]
    max_x: int
    max_y: int

    valley, max_x, max_y = read_from_file(file)
    states = resolve_states(valley, max_x, max_y)

    end: tuple[int, int] = (max_x - 1, max_y - 1)
    position: tuple[int, int] = (1, 1)

    path: int = path_finder(position, end, states, max_x, max_y)

    return path


def __part_two__(file: Path) -> int:
    valley: dict[tuple[int, int], list[str]]
    max_x: int
    max_y: int

    valley, max_x, max_y = read_from_file(file)
    states = resolve_states(valley, max_x, max_y)

    end: tuple[int, int] = (max_x - 1, max_y - 1)
    start: tuple[int, int] = (1, 1)

    goal: int = path_finder(start, end, states, max_x, max_y, minute=1)
    back: int = path_finder(end, start, states, max_x, max_y, minute=goal)
    goal_again: int = path_finder(start, end, states, max_x, max_y, minute=(goal + back))

    return sum([goal, back, goal_again])


def part_one() -> int:
    valley, x, y = read_from_file(PARENT.joinpath('state_1_1.txt'))

    for i in range(1, 6):
        expected, x, y = read_from_file(PARENT.joinpath(f'state_1_{i + 1}.txt'))
        valley = blizzard(valley, x, y)

        if i == 3:
            continue

        assert valley == expected

    example: int = __part_one__(PARENT.joinpath('example.txt'))
    assert example == 18
    answer: int = __part_one__(PARENT.joinpath('input.txt'))
    return answer


def part_two() -> int:
    example: int = __part_two__(PARENT.joinpath('example.txt'))
    assert example == 54
    answer: int = __part_two__(PARENT.joinpath('input.txt'))
    return answer


def main():
    print("Part One: {}".format(part_one()))
    print("Part Two: {}".format(part_two()))


if __name__ == '__main__':
    main()
