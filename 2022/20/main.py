#!/usr/bin/env python
from collections import deque
from typing import List


def read_from_file(file: str) -> List[int]:
    with open(file) as f:
        return [int(line) for line in f.readlines()]


def mix(enumerated: deque):
    for idx_start in range(len(enumerated)):

        while enumerated[0][0] != idx_start:
            enumerated.rotate(-1)

        item = enumerated.popleft()
        shift = item[1] % len(enumerated)
        enumerated.rotate(-shift)
        enumerated.append(item)

    return enumerated


def part_one(file: str) -> int:
    numbers: List[int] = read_from_file(file)

    mixed = mix(deque(enumerate(numbers)))
    values = [value[1] for value in mixed]
    ans: int = 0

    for n in [1000, 2000, 3000]:
        position = (values.index(0) + n) % len(values)
        ans += values[position]
    return ans

    original_numbers: List[int] = numbers.copy()
    length: int = len(numbers) - 1

    print(numbers)
    for number in original_numbers:
        idx_old: int = numbers.index(number)
        numbers.remove(number)
        # n: int = numbers.pop(idx_old)
        idx_new: int = (idx_old + number) % length

        numbers.insert(idx_new, number)

        # print("{}: {}".format(number, numbers))

    idx_zero: int = numbers.index(0)
    _1000th: int = numbers[(idx_zero + 1000) % len(numbers)]
    _2000th: int = numbers[(idx_zero + 2000) % len(numbers)]
    _3000th: int = numbers[(idx_zero + 3000) % len(numbers)]
    return sum([_1000th, _2000th, _3000th])


def part_two(file: str) -> int:
    decryption_key: int = 811589153
    numbers: List[int] = read_from_file(file)

    enumerated = deque([(i, v * decryption_key) for i, v in enumerate(numbers)])
    for _ in range(10):
        enumerated = mix(enumerated)

    values = [value[1] for value in enumerated]
    ans: int = 0

    for n in [1000, 2000, 3000]:
        position = (values.index(0) + n) % len(values)
        ans += values[position]
    return ans


def main():
    p1_example: int = part_one('example.txt')
    assert p1_example == 3
    p1: int = part_one('input.txt')
    print("Part One: {}".format(p1))

    p2_example: int = part_two('example.txt')
    assert p2_example == 1623178306
    p2: int = part_two('input.txt')
    print("Part Two: {}".format(p2))


if __name__ == '__main__':
    main()
