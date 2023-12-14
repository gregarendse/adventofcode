#!/usr/bin/env python
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

PARENT = Path(__file__).parent


def read_from_file(file: Path) -> list[list[str]]:
    dish: List[List[str]] = []

    with open(file) as f:
        for y, line in enumerate(f.readlines()):
            xs: List[str] = []
            for x, c in enumerate(line.strip()):
                xs.append(c)
            dish.append(xs)

        return dish


def hash_list(l: List[List[str]]) -> int:
    t: Tuple[Tuple[str]] = ()
    for line in l:
        _t = tuple([c for c in line])
        t += _t
    return hash(t)


def tilt_north(dish: List[List[str]]) -> List[List[str]]:
    l: int = len(dish)
    for y in range(l):
        ys = dish[y]
        for x in range(len(ys)):

            if dish[y][x] != '.':
                continue

            for dy in range(y + 1, l):
                if dish[dy][x] == '#':
                    break
                if dish[dy][x] == 'O':
                    dish[y][x] = dish[dy][x]
                    dish[dy][x] = '.'
                    break

    return dish


def tilt_south(dish: List[List[str]]) -> List[List[str]]:
    for y in reversed(range(len(dish))):
        ys = dish[y]
        for x in range(len(ys)):

            if dish[y][x] != '.':
                continue

            for dy in reversed(range(y)):
                if dish[dy][x] == '#':
                    break
                if dish[dy][x] == 'O':
                    dish[y][x] = dish[dy][x]
                    dish[dy][x] = '.'
                    break

    return dish


def tilt_west(dish: List[List[str]]) -> List[List[str]]:
    l: int = len(dish)
    for y in range(l):
        ys = dish[y]
        for x in range(len(ys)):

            if dish[y][x] != '.':
                continue

            for dx in range(x + 1, len(ys)):
                if dish[y][dx] == '#':
                    break
                if dish[y][dx] == 'O':
                    dish[y][x] = dish[y][dx]
                    dish[y][dx] = '.'
                    break

    return dish


def tilt_east(dish: List[List[str]]) -> List[List[str]]:
    l: int = len(dish)
    for y in range(l):
        ys = dish[y]
        for x in reversed(range(len(ys))):

            if dish[y][x] != '.':
                continue

            for dx in reversed(range(x)):
                if dish[y][dx] == '#':
                    break
                if dish[y][dx] == 'O':
                    dish[y][x] = dish[y][dx]
                    dish[y][dx] = '.'
                    break

    return dish


def calculate_load(dish: List[List[str]]) -> int:
    totals: List[int] = []
    l: int = len(dish)
    for y, line in enumerate(dish):
        for x, c in enumerate(line):
            if c == 'O':
                totals.append(l - y)
    return sum(totals)


def __part_one__(file: Path) -> int:
    dish = read_from_file(file)
    dish = tilt_north(dish)
    total = calculate_load(dish)
    return total


def cycle(dish: List[List[str]], count: int = 1000000000) -> List[List[str]]:
    history: Dict[int, List[List[str]]] = dict()
    i_map: Dict[int, List[List[str]]] = dict()
    h_map: Dict[int, int] = defaultdict(int)

    steps_to_cycle: int = 0
    cycle_length: int = 0
    cycle_history: List[int] = []

    for i in range(count):
        # h: int = hash_list(dish)
        #
        # if h in history:
        #     if steps_to_cycle == 0:
        #         steps_to_cycle = i
        #     if h not in cycle_history:
        #         cycle_history.append(h)
        #     else:
        #         cycle_length = i - steps_to_cycle
        #
        #         idx = (count - steps_to_cycle + cycle_length) % cycle_length
        #
        #         for key, value in history.items():
        #             load = calculate_load(value)
        #             print(f"{key} : {load}")
        #
        #         return history[cycle_history[idx]]
        #
        #     # return i_map[(count - 1) % (i)]
        #     dish = history[h]
        #     h_map[h] += 1
        #     # break
        # else:
        dish = tilt_north(dish)
        dish = tilt_west(dish)
        dish = tilt_south(dish)
        dish = tilt_east(dish)
        # dish = deepcopy(dish)

        # history[h] = dish
        # i_map[i] = dish

    return dish


def __part_two__(file: Path, count: int = 1000000000) -> int:
    # north, then west, then south, then east
    dish = read_from_file(file)

    dish = cycle(dish, count)

    total = calculate_load(dish)
    return total


def part_one() -> int:
    example: int = __part_one__(PARENT.joinpath('example.txt'))
    assert example == 136
    answer: int = __part_one__(PARENT.joinpath('input.txt'))
    return answer


def part_two() -> int:
    path = PARENT.joinpath('example.txt')

    answer: List[List[str]] = read_from_file(PARENT.joinpath('cycle_1.txt'))
    hash_1 = hash_list(answer)
    dish = read_from_file(path)
    dish = cycle(dish, 1)
    assert dish == answer

    answer = read_from_file(PARENT.joinpath('cycle_2.txt'))
    hash_2 = hash_list(answer)
    assert hash_1 != hash_2
    dish = read_from_file(path)
    dish = cycle(dish, 2)
    assert dish == answer

    answer = read_from_file(PARENT.joinpath('cycle_3.txt'))
    hash_3 = hash_list(answer)
    assert hash_2 != hash_3 != hash_1
    dish = read_from_file(path)
    dish = cycle(dish, 3)
    assert dish == answer

    example: int = __part_two__(path, count=1000)
    assert example == 64
    answer: int = __part_two__(PARENT.joinpath('input.txt'), count=1000)
    return answer


def main():
    print("Part One: {}".format(part_one()))
    print("Part Two: {}".format(part_two()))


if __name__ == '__main__':
    main()
