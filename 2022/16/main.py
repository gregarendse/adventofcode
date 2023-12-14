#!/use/bin/env python
import functools
from dataclasses import dataclass
from sys import argv
from typing import List, Dict


@dataclass
class Valve(object):
    name: str
    rate: int
    next: List[str]

    def __hash__(self):
        return hash(self.name)


def read_from_file(file: str) -> Dict[str, Valve]:
    valves: Dict[str, Valve] = dict()
    with open(file) as f:
        for line in f.readlines():
            # 0     1  2   3    4       5       6    7  8      9+
            # Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
            parts = line.split()
            name = parts[1]
            rate = int(parts[4].split('=')[1][:-1])
            next = " ".join(parts[9:]).split(', ')
            valves[name] = Valve(name=name, rate=rate, next=next)

    return valves


def display(valves: List[Valve]) -> None:
    for v in valves:
        print(v)


valves: Dict[str, Valve]


@functools.lru_cache(maxsize=None)
def find_next(
        valve: Valve,
        opened,
        minutes: int = 30
) -> int:
    if minutes <= 0:
        return 0

    max_rate: int = 0

    if valve.name not in opened:

        for possible in valve.next:

            if valve.rate != 0:
                rate: int = valve.rate * (minutes - 1)
                current_opened = tuple(sorted(opened + (valve.name,)))

                max_rate = max(
                    max_rate,
                    rate + find_next(valve=valves[possible], opened=current_opened, minutes=minutes - 2)
                )
            else:
                max_rate = max(
                    max_rate,
                    find_next(valve=valves[possible], opened=opened, minutes=minutes - 1)
                )
    return max_rate


def part_one(file: str) -> int:
    global valves
    valves = read_from_file(file)
    position: str = 'AA'
    path: List[str] = []

    value = find_next(valve=valves[position], opened=tuple([]))
    print(path)
    return value


def part_two(file: str) -> int:
    return None


def main(file: str):
    if file is None:
        file = argv[1]
    print("Part One: {}".format(part_one(file)))
    print("Part Two: {}".format(part_two(file)))


if __name__ == '__main__':
    main(file='input.txt')
