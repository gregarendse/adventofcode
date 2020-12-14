from typing import List

import math


def part_one(earliest: int, bus_ids: List[int]) -> int:
    earliest_departure_time: int = None
    earliest_bus_id: int = None

    for bus_id in bus_ids:
        departure_time: int = 0

        while departure_time < earliest:
            departure_time += bus_id

        if earliest_departure_time is None or earliest_departure_time > departure_time:
            earliest_departure_time = departure_time
            earliest_bus_id = bus_id

    return (earliest_departure_time - earliest) * earliest_bus_id


def chinese_remainder_theorem(moduluses: List[int], remainders: List[int]) -> int:
    product: int = math.prod(moduluses)
    sum: int = 0

    for modulus, remainder in zip(moduluses, remainders):
        p: int = product // modulus
        sum += remainder * p * multiple_inverse(modulus, p)

    return sum % product


def multiple_inverse(a: int, b: int) -> int:
    for inverse in range(a):
        if b * inverse % a == 1:
            return inverse
    raise Exception


def part_two(bus_ids: List[str]) -> int:
    return chinese_remainder_theorem(
        [int(bus_id) for bus_id in bus_ids if bus_id != 'x'],
        [int(bus_id) - i for i, bus_id in enumerate(bus_ids) if bus_id != 'x']
    )


with open('input.txt', 'r') as file:
    [earliest, buss_ids] = file.readlines()
    print(part_one(int(earliest), [int(x) for x in buss_ids.split(',') if x != 'x']))
    print(part_two(buss_ids.split(',')))
