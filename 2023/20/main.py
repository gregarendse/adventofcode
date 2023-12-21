#!/usr/bin/env python
import re
from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path
from re import Pattern
from typing import Dict, List

PARENT = Path(__file__).parent


@dataclass
class Module(object):
    name: str
    connections: List[str]

    def pulse(self, i: int, source: str) -> int:
        return i


class Broadcast(Module):
    pass


class FlipFlop(Module):
    """
    Flip-flop modules (prefix %) are either on or off; they are initially off.
    If a flip-flop module receives a high pulse, it is ignored and nothing happens.
    However, if a flip-flop module receives a low pulse, it flips between on and off.
    If it was off, it turns on and sends a high pulse.
    If it was on, it turns off and sends a low pulse.
    """
    state: int = 0

    def pulse(self, i: int, source: str) -> int:
        if i == 0:
            if self.state == 0:
                self.state = 1
                return 1
            elif self.state == 1:
                self.state = 0
                return 0
        return None


class Conjunction(Module):
    """
    Conjunction modules (prefix &) remember the type of the most recent pulse received from each of their connected
    input modules; they initially default to remembering a low pulse for each input.
    When a pulse is received, the conjunction module first updates its memory for that input.
    Then, if it remembers high pulses for all inputs, it sends a low pulse; otherwise, it sends a high pulse.
    """
    state: Dict[str, int] = dict()

    def pulse(self, i: int, source: str) -> int:
        self.state[source] = i

        if all(self.state.values()):
            return 0
        else:
            return 1


def read_from_file(file: Path) -> dict[str, Module]:
    pattern: Pattern[str] = re.compile(r"([&%]?)(\w+) -> ([a-z\s,]+)")

    module_map: Dict[str, Module] = dict()
    conjunctions: List[Conjunction] = []
    modules: List[str] = []
    sources: Dict[str, List[str]] = defaultdict(list)

    with open(file) as f:

        for line in f.readlines():
            for match in pattern.findall(line.strip()):
                name: str = str(match[1])
                connections: List[str] = [str(c).strip() for c in match[2].split(',')]

                for connection in connections:
                    sources[connection].append(name)

                if match[0] == '':
                    module_map[name] = Broadcast(name=name, connections=connections)
                elif match[0] == '%':
                    module_map[name] = FlipFlop(name=name, connections=connections)
                    modules.append(name)
                elif match[0] == '&':
                    conjunction = Conjunction(name=name, connections=connections)
                    module_map[name] = conjunction
                    conjunctions.append(conjunction)
                    modules.append(name)
                else:
                    raise Exception

    for conjunction in conjunctions:
        conjunction.state = dict.fromkeys([source for source in sources[conjunction.name]], 0)
    return module_map


def press_button(module_map: dict[str, Module], pulses: Dict[int, int]) -> Dict[int, int]:
    # print('-----')
    q = deque([('button', 0, 'broadcaster')])

    while q:
        (source, pulse, connection) = q.popleft()
        pulses[pulse] += 1

        module = module_map.get(connection)

        if module is None:
            continue

        pulse = module.pulse(pulse, source)

        if pulse is None:
            continue

        for c in module.connections:
            # print(f"{connection} {pulse} -> {c}")
            q.append((connection, pulse, c))
            if pulse == 0 and c == 'rx':
                raise TypeError

    return pulses


def __part_one__(file: Path, count: int = 1000) -> int:
    module_map: dict[str, Module] = read_from_file(file)
    pulses: Dict[int, int] = defaultdict(int)

    for _ in range(count):
        pulses = press_button(module_map, pulses)

    total: int = 1
    for value in pulses.values():
        total *= value
    return total


def __part_two__(file: Path) -> int:
    module_map: dict[str, Module] = read_from_file(file)
    pulses: Dict[int, int] = defaultdict(int)

    count: int = 0

    while True:
        count += 1
        try:
            pulses = press_button(module_map, pulses)
        except TypeError:
            return count


def part_one() -> int:
    example: int = __part_one__(PARENT.joinpath('example.txt'))
    assert example == 32000000
    example: int = __part_one__(PARENT.joinpath('example_2.txt'))
    assert example == 11687500
    answer: int = __part_one__(PARENT.joinpath('input.txt'))
    return answer


def part_two() -> int:
    answer: int = __part_two__(PARENT.joinpath('input.txt'))
    return answer


def main():
    print("Part One: {}".format(part_one()))
    print("Part Two: {}".format(part_two()))


if __name__ == '__main__':
    main()
