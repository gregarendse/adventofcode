#!/usr/bin/env python
import re
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Monkey(object):
    name: str
    left: str = None
    right: str = None
    operand: str = None
    value: int = None


def read_from_file(file: str) -> Dict[str, Monkey]:
    pattern = re.compile("(\w+): ([a-z0-9]+)( ([+-/*]) (\w+))?")
    with open(file) as f:
        monkeys: List[Monkey] = []
        monkey_map: Dict[str, Monkey] = dict()

        for line in f.readlines():
            matches = pattern.match(line)
            monkey = Monkey(name=matches[1])

            if matches[5] is not None:
                monkey.left = matches[2]
                monkey.operand = matches[4]
                monkey.right = matches[5]
            else:
                monkey.value = int(matches[2])
            monkeys.append(monkey)
            monkey_map[monkey.name] = monkey

        return monkey_map


def calculate(monkey_map: Dict[str, Monkey], name: str = 'root') -> int:
    monkey: Monkey = monkey_map[name]

    if monkey.value is not None:
        return monkey.value

    left: int = calculate(monkey_map, name=monkey.left)
    right: int = calculate(monkey_map, name=monkey.right)

    if '+' == monkey.operand:
        return left + right
    elif '-' == monkey.operand:
        return left - right
    elif '/' == monkey.operand:
        return left // right
    elif '*' == monkey.operand:
        return left * right
    else:
        raise Exception("Unknown operand: " + monkey.operand)


def part_one(file: str) -> int:
    monkey_map: Dict[str, Monkey] = read_from_file(file)

    return calculate(monkey_map)


def next_guess(guess: int = 0, previous_guess: int = 0, result: int = 0, previous_result: int = 0) -> int:
    try:
        gradient = (guess - previous_guess) / (result - previous_result)
    except:
        gradient = 1 if result < previous_result else -1
    return gradient


def part_two(file: str) -> int:
    monkey_map: Dict[str, Monkey] = read_from_file(file)

    # Find diff
    monkey_map['root'].operand = '-'

    previous_diff: int = abs(calculate(monkey_map))
    previous_guess: int = monkey_map['humn'].value

    monkey_map['humn'].value = 0
    diff: int = abs(calculate(monkey_map))

    rate = 0.01

    while diff > rate:
        gradient: int = next_guess(
            guess=monkey_map['humn'].value,
            previous_guess=previous_guess,
            result=diff,
            previous_result=previous_diff
        )

        previous_guess = monkey_map['humn'].value
        previous_diff = diff

        monkey_map['humn'].value = monkey_map['humn'].value - (rate * diff * gradient)

        diff = abs(calculate(monkey_map))

    return round(monkey_map['humn'].value)


def main():
    p1_example: int = part_one('example.txt')
    assert p1_example == 152
    p1: int = part_one('input.txt')
    print("Part One: {}".format(p1))

    p2_example: int = part_two('example.txt')
    assert p2_example == 301
    p2: int = part_two('input.txt')
    print("Part Two: {}".format(p2))


if __name__ == '__main__':
    main()
