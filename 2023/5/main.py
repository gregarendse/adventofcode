#!/usr/bin/env python
from pathlib import Path
from typing import Dict, List

PARENT = Path(__file__).parent


class Converter(object):

    srcs: List[int]
    dsts: List[int]
    lengths: List[int]

    def __init__(self):
        super().__init__()
        self.srcs = []
        self.dsts = []
        self.lengths = []

    def convert(self, input: int) -> int:
        for i in range(len(self.srcs)):
            if self.srcs[i] <= input <= self.srcs[i] + self.lengths[i]:
                return self.dsts[i] + (input - self.srcs[i])
        return input


def read_from_file(file: Path) -> str:
    with open(file) as f:
        content = f.read()

        parts = content.split('\n\n')
        seeds = [int(s) for s in parts[0].split(':')[1].split()]

        maps: List[Converter] = []

        for map in parts[1:]:
            converter: Converter = Converter()

            for convert in map.splitlines()[1:]:
                dst, src, length = convert.split()
                converter.srcs.append(int(src))
                converter.dsts.append(int(dst))
                converter.lengths.append(int(length))

            maps.append(converter)

        return seeds, maps


def __part_one__(file: Path) -> int:
    seeds, maps = read_from_file(file)

    lowest_location: int = 999999999999999999

    for seed in seeds:
        for converter in maps:
            seed = converter.convert(seed)
        print(f"{seed}")
        lowest_location = min(lowest_location, seed)

    return lowest_location


def process(seed: int, converts: List[Converter]) -> int:
    for converter in converts:
        seed = converter.convert(seed)
    return seed


def __part_two__(file: Path) -> int:
    seeds, maps = read_from_file(file)

    lowest_location: int = 999999999999999999
    idx: int = None
    seed_location_map: Dict[int, List[int]] = dict()
    state = None

    for i in range(0, len(seeds), 2):

        location_low: int = 99999999999999999999
        seed_low = None

        for seed in range(seeds[i], seeds[i] + seeds[i + 1], int(seeds[i + 1] ** 0.5)):
            location = process(seed, maps)

            if location < location_low:
                seed_low = seed
                location_low = location

        if location_low < lowest_location:
            state = (i, seed_low, location_low)
            lowest_location = location_low

    (i, seed_low, location_low) = state

    aaaa = int(seeds[i + 1] ** 0.5)

    for seed in range(seed_low - aaaa, seed_low + aaaa):
        lowest_location = min(lowest_location, process(seed, maps))

    return lowest_location


def part_one() -> int:
    example: int = __part_one__(PARENT.joinpath('example.txt'))
    assert example == 35
    answer: int = __part_one__(PARENT.joinpath('input.txt'))
    return answer


def part_two() -> int:
    example: int = __part_two__(PARENT.joinpath('example.txt'))
    assert example == 46
    answer: int = __part_two__(PARENT.joinpath('input.txt'))
    return answer


def main():
    print("Part One: {}".format(part_one()))
    print("Part Two: {}".format(part_two()))


if __name__ == '__main__':
    main()
