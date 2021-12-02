#!/bin/python

from typing import List


def part_one(lines: List[str]) -> str:
    horizontal_pos: int = 0
    depth_pos: int = 0

    for line in lines:
        [direction, length] = line.split(' ')
        if 'forward' == direction:
            horizontal_pos = horizontal_pos + int(length)
        elif 'down' == direction:
            depth_pos = depth_pos + int(length)
        elif 'up' == direction:
            depth_pos = depth_pos - int(length)
        else:
            raise Exception(line)

    return horizontal_pos * depth_pos


def part_two(lines: List[str]) -> str:
    horizontal_pos: int = 0
    depth_pos: int = 0
    aim: int = 0

    for line in lines:
        [direction, length] = line.split(' ')
        if 'forward' == direction:
            horizontal_pos = horizontal_pos + int(length)
            depth_pos = depth_pos + (aim * int(length))
        elif 'down' == direction:
            aim = aim + int(length)
        elif 'up' == direction:
            aim = aim - int(length)
        else:
            raise Exception(line)

    return horizontal_pos * depth_pos


with open('2021/02/input.txt', 'r') as file:
    lines: List[str] = file.readlines()

    print(part_one(lines))
    print(part_two(lines))
