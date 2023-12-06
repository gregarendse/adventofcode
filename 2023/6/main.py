#!/usr/bin/env python
from pathlib import Path
from typing import List, Tuple

PARENT = Path(__file__).parent


def read_from_file(file: Path) -> list[tuple[int, int]]:
    time_distances: List[Tuple[int, int]] = []
    with open(file) as f:
        times, distances = f.readlines()

        times = times.split(':')[1].split()
        distances = distances.split(':')[1].split()

        for i in range(len(times)):
            time_distances.append(
                (int(times[i]), int(distances[i]))
            )
    return time_distances


def __part_one__(file: Path) -> int:
    time_distances = read_from_file(file)

    counts: List[int] = []
    total = 1

    for time, distance in time_distances:
        hold_durations: List[int] = []
        for i in range(time):
            if i * (time - i) > distance:
                hold_durations.append(i)
        counts.append(len(hold_durations))
        total *= len(hold_durations)

    return total


def __part_two__(file: Path) -> int:
    time_distances = read_from_file(file)

    s_time: str = ""
    s_distance: str = ""

    for time, distance in time_distances:
        s_time += str(time)
        s_distance += str(distance)

    time = int(s_time)
    distance = int(s_distance)

    hold_durations: List[int] = []
    for i in range(time):
        if i * (time - i) > distance:
            hold_durations.append(i)

    return len(hold_durations)


def part_one() -> int:
    example: int = __part_one__(PARENT.joinpath('example.txt'))
    assert example == 288
    answer: int = __part_one__(PARENT.joinpath('input.txt'))
    return answer


def part_two() -> int:
    example: int = __part_two__(PARENT.joinpath('example.txt'))
    assert example == 71503
    answer: int = __part_two__(PARENT.joinpath('input.txt'))
    return answer


def main():
    print("Part One: {}".format(part_one()))
    print("Part Two: {}".format(part_two()))


if __name__ == '__main__':
    main()
