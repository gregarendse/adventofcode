#!/bin/python

from typing import Dict, List, Set
from statistics import mode, multimode


def part_one(lines: List[str]) -> str:

    bits = {}

    for i in range(len(lines[0]) - 1):
        bits[i] = []
    

    for line in lines:
        for i in range(len(line) - 1):
            bits[i].append(line[i])

    gamma_bin = "".join([mode(v) for k,v  in bits.items()])
    epsilon_rate_bin = "".join('1' if x == '0' else '0' for x in gamma_bin)

    return int(gamma_bin, 2) * int(epsilon_rate_bin,2 )


def part_two(lines: List[str]) -> str:
    bits = {}

    for i in range(len(lines[0]) - 1):
        bits[i] = []
    

    for line in lines:
        for i in range(len(line) - 1):
            bits[i].append(line[i])

    oxygen_rating = search(lines, bits)
    co2_rating = c02(lines, bits)

    return (int(co2_rating, 2) * int(oxygen_rating, 2))



def search(lines: List[List[str]], bits: Dict[int, List[str]], position: int = 0) -> List[str]:
    if len(lines) == 1:
        return lines[0]

    modes = multimode([line[position] for line in lines])

    if len(modes) > 1:
        common = '1'
    else:
        common = modes[0]

    return search([line for line in lines if line[position] == common], bits, position + 1)

def c02(lines: List[List[str]], bits: Dict[int, List[str]], position: int = 0) -> List[str]:
    if len(lines) == 1:
        return lines[0]

    modes = multimode([line[position] for line in lines])

    if len(modes) > 1:
        common = '0'
    else:
        common = '1' if modes[0] == '0' else '0'

    return c02([line for line in lines if line[position] == common], bits, position + 1)

with open('2021/03/input.txt', 'r') as file:
    lines = file.readlines()

    print(part_one(lines))
    print(part_two(lines))
