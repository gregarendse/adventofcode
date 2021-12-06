#!/bin/python

from typing import Dict, List, Set


def calculate(state: Dict[int, int], days: int) -> int:
    for i in range(days):
        zeros: int = 0

        for j in range(len(state.keys())):
            if j == 0:
                zeros = state[j]
                state[j] = state[j + 1]
            elif j == len(state.keys()) - 1:
                state[j] = 0
            else:
                state[j] = state[j + 1]

        state[6] += zeros
        state[8] += zeros

    return sum(state.values())


def part_one(state: Dict[int, int]) -> None:
    print(calculate(state, days=80))


def part_two(state: Dict[int, int]) -> None:
    print(calculate(state, days=256))


with open('2021/06/input.txt', 'r') as file:

    content: str = file.read()
    ages: List[int] = [int(x) for x in content.split(',')]

    initial_state: Dict[int, int] = {i: 0 for i in range(9)}

    for age in ages:
        initial_state[age] += 1

part_one(initial_state.copy())
part_two(initial_state.copy())
