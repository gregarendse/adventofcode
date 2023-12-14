#!/usr/bin/env python
from pathlib import Path
from typing import List, Tuple

PARENT = Path(__file__).parent


def read_from_file(file: Path) -> list[tuple[str, list[int]]]:
    lines: List[Tuple[str, List[int]]] = []
    with open(file) as f:
        for line in f.readlines():
            pattern, numbers = line.split()
            numbers = [int(n) for n in numbers.split(',')]
            lines.append((pattern, numbers))
    return lines


def matches(possibility: str, numbers: List[int]) -> bool:
    possibility = possibility.strip('.')
    parts = possibility.split('.')
    parts = list(filter(lambda p: len(p), parts))

    if len(parts) != len(numbers):
        return False

    for idx, part in enumerate(parts):
        if len(part) != numbers[idx]:
            return False
    return True


def parse(pattern: str, numbers: List[int]) -> int:
    fixed_characters: int = 0
    idxs: List[int] = []
    for idx, s in enumerate(pattern):
        if s == '?':
            idxs.append(idx)
        elif s == '#':
            fixed_characters += 1
    possibilities: int = 2 ** sum(numbers)

    patterns: List[str] = []
    n_sum: int = sum(numbers) - fixed_characters

    for p in range(possibilities):
        bin_str: str = bin(p)[2:].zfill(len(pattern))
        if bin_str.count('1') != n_sum:
            continue

        possible_pattern = str(pattern)

        for i, idx in enumerate(idxs):
            s: str = '#' if bin_str[len(pattern) - i - 1] == '1' else '.'
            possible_pattern = possible_pattern[:idx] + s + possible_pattern[idx + 1:]
        if matches(possible_pattern, numbers):
            patterns.append(possible_pattern)

    return len(patterns)


def __part_one__(file: Path) -> int:
    lines: list[tuple[str, list[int]]] = read_from_file(file)

    totals: List[int] = []

    for line in lines:
        totals.append(
            parse(line[0], line[1])
        )

    return sum(totals)


def expanded_parse(pattern: str, numbers: List[int], expand: int = 5) -> int:
    extended_pattern: str = ""
    extended_numbers: List[int] = []
    for _ in range(expand):
        extended_pattern += pattern
        extended_numbers.extend(numbers)

    return parse(extended_pattern, extended_numbers)


def __part_two__(file: Path) -> int:
    lines: list[tuple[str, list[int]]] = read_from_file(file)

    totals: List[int] = []

    for line in lines:
        possibilities: int = expanded_parse(line[0], line[1])
        print(f"{line} -> {possibilities}")
        totals.append(possibilities)

    return sum(totals)


def part_one() -> int:
    test: int = parse("?###????????", [3, 2, 1])
    assert test == 10

    assert parse("???.###", [1, 1, 3]) == 1
    assert parse(".??..??...?##.", [1, 1, 3]) == 4
    assert parse("?#?#?#?#?#?#?#?", [1, 3, 1, 6]) == 1
    assert parse("????.#...#...", [4, 1, 1]) == 1
    assert parse("????.######..#####.", [1, 6, 5]) == 4
    assert parse("?###????????", [3, 2, 1]) == 10

    example: int = __part_one__(PARENT.joinpath('example.txt'))
    assert example == 21
    answer: int = __part_one__(PARENT.joinpath('input.txt'))
    return answer


def part_two() -> int:
    """

    ???.### 1,1,3 - 1 -> 1
    .??..??...?##. 1,1,3 - 4 -> 16384 (4^(5+2))
    ?#?#?#?#?#?#?#? 1,3,1,6 - 1 -> 1
    ????.#...#... 4,1,1 - 1 -> 16
    ????.######..#####. 1,6,5 - 4 -> 2500
    ?###???????? 3,2,1 - 10 -> 506250


    :return:
    """
    assert parse("???.###", [1, 1, 3]) == 1
    assert expanded_parse("???.###", [1, 1, 3]) == 1
    assert expanded_parse(".??..??...?##.", [1, 1, 3]) == 16384
    assert expanded_parse("?#?#?#?#?#?#?#?", [1, 3, 1, 6]) == 1
    assert expanded_parse("????.#...#...", [4, 1, 1]) == 16
    assert expanded_parse("????.######..#####.", [1, 6, 5]) == 2500
    assert expanded_parse("?###????????", [3, 2, 1]) == 506250

    example: int = __part_two__(PARENT.joinpath('example.txt'))
    assert example == 525152
    answer: int = __part_two__(PARENT.joinpath('input.txt'))
    return answer


def main():
    # print("Part One: {}".format(part_one()))
    print("Part Two: {}".format(part_two()))


if __name__ == '__main__':
    main()
