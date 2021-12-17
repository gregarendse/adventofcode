#!/bin/python

from typing import List, Set


def max_dist(x: int) -> int:
    distance: int = 0
    while x > 0:
        distance += x

        if x > 0:
            x -= 1
        elif x < 0:
            x += 1

    return distance


def calc_height(y: int, target_y: List[int]) -> int:
    height: int = 0

    while height > min(target_y):
        height += y


def max_height(target_y: List[int]) -> int:

    step: int = abs(min(target_y)) - 1
    y: int = 0
    max_height: int = 0

    while not (min(target_y) < y < max(target_y)) and y > min(target_y):
        y = y + step
        step -= 1

        if y > max_height:
            max_height = y

    return max_height


def y_steps(start_y: int, target_y: List[int]) -> List[int]:
    y: int = 0
    velocity: int = start_y
    steps: int = 0
    valid: List[int] = []

    while y >= min(target_y):
        if min(target_y) <= y <= max(target_y):
            valid.append(steps)
        y += velocity
        velocity -= 1
        steps += 1

    return valid


def x_steps(steps: int, target_x: List[int]) -> Set[int]:
    valid: Set[int] = set()

    for start_x in range(max(target_x) + 1):
        x: int = 0
        velocity: int = start_x

        for _ in range(steps):
            x += velocity
            velocity -= min(velocity, 1)

        if min(target_x) <= x <= max(target_x):
            valid.add(start_x)

    return valid

def find_min_x(target_x: List[int]) -> int:
        start_x: int = 0
        x: int = start_x
        while not (min(target_x) < x < max(target_x)):
            start_x += 1
            x = max_dist(start_x)
        print(f"{start_x} -> {x}")
        return start_x



with open('2021/17/input.txt', 'r') as file:
    for line in file.readlines():
        parts = line.split(':')

        x_part = parts[1].split(',')[0].strip().split('=')[1].split('..')
        y_part = parts[1].split(',')[1].strip().split('=')[1].split('..')

        target_x: List[int] = [int(x) for x in x_part]
        target_y: List[int] = [int(y) for y in y_part]

        height: int = max_height(target_y)

        print(f"{height}")

        count: int = 0

        for start_y in range(min(target_y), abs(min(target_y)) + 1):

            valid: Set[int] = set()

            for steps in y_steps(start_y, target_y):
                start_xs: Set[int] = x_steps(steps, target_x)
                valid.update(start_xs)

            count += len(valid)

        print(count)
