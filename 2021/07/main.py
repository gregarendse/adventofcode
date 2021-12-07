#!/bin/python

from typing import List


def calculat_cost(position: List[int], point: int = 0, cost: int = 9999999999) -> int:

    new_cost: int = 0

    for position in positions:
        new_cost += abs(point - position)

    if new_cost > cost:
        return cost
    else:
        return calculat_cost(positions, point+1, new_cost)


def calculate_exp_cost(position: List[int], point: int = 0, cost: int = 999999999) -> int:

    new_cost: int = 0

    for position in positions:
        new_cost += abs(position - point) * (abs(position - point) + 1) / 2

    if new_cost > cost:
        return int(cost)
    else:
        return calculate_exp_cost(positions, point + 1, new_cost)


with open('2021/07/input.txt', 'r') as file:
    positions: List[int] = [int(x) for x in file.read().split(',')]

print(calculat_cost(positions, point=min(positions)))
print(calculate_exp_cost(positions, point=min(positions)))
