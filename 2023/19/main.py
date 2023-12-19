#!/usr/bin/env python
import re
from dataclasses import dataclass
from pathlib import Path
from re import Pattern
from typing import List, Dict, Optional

PARENT = Path(__file__).parent


@dataclass
class Rule(object):
    category: str
    operator: str
    condition: int
    destination: str

    def apply(self, part: Dict[str, int]) -> Optional[str]:
        if self.operator == '<':
            if part[self.category] < self.condition:
                return self.destination
        elif self.operator == '>':
            if part[self.category] > self.condition:
                return self.destination
        return None


@dataclass
class Workflow(object):
    rules: List[Rule]
    destination: str

    def process(self, part: Dict[str, int]) -> str:
        for rule in self.rules:
            dest: Optional[str] = rule.apply(part)
            if dest is not None:
                return dest
        return self.destination


def read_from_file(file: Path) -> tuple[list[dict[str, int]], dict[str, Workflow]]:
    with open(file) as f:
        workflows_raw, ratings_raw = f.read().split('\n\n')

    pattern: Pattern[str] = re.compile(r"(\w+){(.*)}")
    parts: List[Dict[str, int]] = []

    for line in ratings_raw.splitlines():
        part_map: Dict[str, int] = dict()
        for part in line[1:-1].split(','):
            t, n = part.split('=')
            part_map[str(t)] = int(n)
        parts.append(part_map)

    workflows_map: Dict[str, Workflow] = dict()

    for line in workflows_raw.splitlines():
        matches = pattern.findall(line)[0]
        name: str = matches[0]
        rules_raw: List[str] = matches[1].split(',')
        dst: str = rules_raw[-1]

        rules: List[Rule] = []
        for rule in rules_raw[:-1]:
            sub_pattern = re.compile(r"(\w)([<>])(\d+):(\w+)")
            sub_matches = sub_pattern.findall(rule)[0]
            rules.append(
                Rule(
                    category=str(sub_matches[0]),
                    operator=str(sub_matches[1]),
                    condition=int(sub_matches[2]),
                    destination=str(sub_matches[3])
                )
            )

        workflow: Workflow = Workflow(
            rules=rules,
            destination=str(dst)
        )

        workflows_map[str(name)] = workflow

    return parts, workflows_map


def __part_one__(file: Path) -> int:
    parts, workflows_map = read_from_file(file)
    start: str = 'in'
    accepted_parts: List[Dict[str, int]] = []
    count: int = 0

    for part in parts:
        n = start
        while n != 'R' and n != 'A':
            n = workflows_map[n].process(part)
        if n == 'A':
            accepted_parts.append(part)
            for value in part.values():
                count += value
    return count


def __part_two__(file: Path) -> int:
    raise Exception("Not implemented")
    content: str = read_from_file(file)
    return 0


def part_one() -> int:
    example: int = __part_one__(PARENT.joinpath('example.txt'))
    assert example == 19114
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
