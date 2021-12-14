#!/bin/python

from dataclasses import dataclass
from typing import Dict, List, Set
import statistics
import copy


def step(polymer_template: str, rules: Dict[str, str]) -> str:
    s: str = ""

    for i in range(len(polymer_template) - 1):
        s += polymer_template[i] + rules.get(polymer_template[i:i+2])

    s += polymer_template[-1]

    return s


def part_one(polymer_template: str, rules: List[str]) -> int:
    rule_map: Dict[str, str] = {}
    for rule in rules:
        pair, element = rule.split(' -> ')
        rule_map[pair.strip()] = element.strip()

    polymer: str = polymer_template
    for i in range(10):
        polymer = step(polymer, rule_map)

    occur_map: Dict[str, int] = {}
    for p in polymer:
        if occur_map.get(p) is None:
            occur_map[p] = 0
        occur_map[p] += 1

    return max(occur_map.values()) - min(occur_map.values())


def part_two(polymer_template: str, rules: List[str]) -> int:
    # Only keep track of the count of pairs

    rule_map: Dict[str, str] = {}
    for rule in rules:
        pair, element = rule.split(' -> ')
        rule_map[pair.strip()] = element.strip()

    # Init pair counter
    counter: Dict[str, int] = {k: 0 for k in rule_map}

    # Count initial string
    for i in range(len(polymer_template) - 1):
        counter[polymer_template[i:i+2]] += 1

    for i in range(40):
        # Init this step's count of pairs
        new_counter: Dict[str, int] = {k: 0 for k in rule_map}

        # Calculate new pairs and count
        for key in counter:
            # e.g. NN -> C
            # Pair NN maps to two pairs NC & CN
            new_counter[key[0]+rule_map[key]] += counter[key]
            new_counter[rule_map[key]+key[1]] += counter[key]

        counter = new_counter

    # Counter keeps track of pairs.
    occur_map: Dict[str, int] = {k[0]: 0 for k in counter}
    for key in counter:
        # NNCB -> (NN), (NC), (CB)
        # Counting only the first letter of the pair N,N,C
        occur_map[key[0]] += counter[key]
    # The last letter will always be the last letter of the original input B
    occur_map[polymer_template[-1]] += 1

    return max(occur_map.values()) - min(occur_map.values())


with open('2021/14/input.txt', 'r') as file:
    polymer_template, rules = file.read().split('\n\n')

rules: List[str] = rules.splitlines()


print(part_one(copy.deepcopy(polymer_template), rules))
print(part_two(copy.deepcopy(polymer_template), rules))
