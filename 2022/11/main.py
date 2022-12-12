#!/use/bin/env python
from dataclasses import dataclass
from sys import argv
from typing import List


@dataclass
class Monkey(object):
    items: List[int]
    operand: str
    value: str
    test: int
    positive: int
    negative: int
    count: int = 0

    def operation(self, item: int, worry: int = 3, lcm: int = 1) -> int:
        try:
            value: int = int(self.value)
        except ValueError:
            value: int = item

        ret: int = 0

        if self.operand == '+':
            ret = item + value
        elif self.operand == '-':
            ret = item - value
        elif self.operand == '*':
            ret = item * value
        elif self.operand == '/':
            ret = item // value
        else:
            print("PROBLEM")

        return (ret // worry) % lcm

    def divisible(self, operation: int) -> int:
        # print("{} divisible by {} -> {}".format(operation, self.test, operation % self.test))
        if operation % self.test == 0:
            return self.positive
        else:
            return self.negative


def read_file(file: str) -> List[Monkey]:
    with open(file, 'r') as f:
        monkeys: List[Monkey] = []
        for monkey_line in f.read().split("\n\n"):
            parts: List[str] = monkey_line.splitlines()
            items: List[int] = [int(x) for x in parts[1].split(':')[1].split(',')]
            [operand, value] = parts[2].split(':')[1].split()[-2:]
            test = int(parts[3].split()[-1])
            positive: int = int(parts[4].split()[-1])
            negative: int = int(parts[5].split()[-1])

            monkeys.append(
                Monkey(items=items, operand=operand, value=value, test=test, positive=positive, negative=negative))
        return monkeys


def output(monkeys: List[Monkey]):
    for monkey in monkeys:
        print(monkey)


def round(monkeys: List[Monkey], rounds: int = 20, worry=3, mod=1) -> List[Monkey]:
    for _ in range(rounds):
        for _, monkey in enumerate(monkeys):
            for item in monkey.items:
                monkey.count += 1
                worry_level: int = monkey.operation(item, worry=worry, lcm=mod)
                to = monkey.divisible(worry_level)
                monkeys[to].items.append(worry_level)

            monkey.items = []
    return monkeys


def part_one(file: str) -> int:
    monkeys: List[Monkey] = read_file(file)
    lcm: int = 1
    for monkey in monkeys:
        lcm = (lcm * monkey.test)
    monkeys = round(monkeys, worry=3, mod=lcm)
    counts: List[int] = [x.count for x in monkeys]
    counts.sort()
    return counts[-1] * counts[-2]


def part_two(file: str) -> int:
    monkeys: List[Monkey] = read_file(file)

    lcm: int = 1

    for monkey in monkeys:
        lcm = (lcm * monkey.test)

    monkeys = round(monkeys, 10000, worry=1, mod=lcm)
    counts: List[int] = [x.count for x in monkeys]
    counts.sort()
    return counts[-1] * counts[-2]


def main():
    print("Part One: {}".format(part_one(argv[1])))
    print("Part Two: {}".format(part_two(argv[1])))


if __name__ == '__main__':
    main()
