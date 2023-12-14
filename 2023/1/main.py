#!/usr/bin/env python
import re
from pathlib import Path
from typing import List

PARENT = Path(__file__).parent


def read_from_file(file: Path) -> List[str]:
    with open(file) as f:
        return f.readlines()


def __part_one__(file: Path) -> int:
    lines: List[str] = read_from_file(file)

    calibrations: List[int] = []

    for line in lines:
        numbers: List[int] = []
        for c in line:
            if c.isnumeric():
                numbers.append(int(c))

        calibrations.append(
            int(
                str(numbers[0]) + str(numbers[-1])

            )
        )

        # calibrations.append(int("".join([numbers[0], numbers[-1]])))

    return sum(calibrations)


def __part_two__(file: Path) -> int:
    lines: List[str] = read_from_file(file)

    calibrations: List[int] = []

    pattern = re.compile("(([0-9])(one)|(two)|(three)|(four)|(five)|(six)|(seven)|(eight)|(nine))")

    matches = pattern.findall(lines[0])

    for line in lines:
        numbers: List[int] = []

        for i in range(len(line)):
            for j in range(i, len(line)):
                n = line[i:j]

                if n.isnumeric():
                    numbers.append(int(n))
                    break
                elif "one" == n:
                    numbers.append(1)
                    break
                elif "two" == n:
                    numbers.append(2)
                    break
                elif "three" == n:
                    numbers.append(3)
                    break
                elif "four" == n:
                    numbers.append(4)
                    break
                elif "five" == n:
                    numbers.append(5)
                    break
                elif "six" == n:
                    numbers.append(6)
                    break
                elif "seven" == n:
                    numbers.append(7)
                    break
                elif "eight" == n:
                    numbers.append(8)
                    break
                elif "nine" == n:
                    numbers.append(9)
                    break

        print(f"{line.strip()} : {str(numbers[0]) + str(numbers[-1])}")
        calibrations.append(
            int(
                str(numbers[0]) + str(numbers[-1])

            )
        )

    return sum(calibrations)


def part_one() -> int:
    example: int = __part_one__(PARENT.joinpath('example.txt'))
    assert example == 142
    answer: int = __part_one__(PARENT.joinpath('input.txt'))
    return answer


def part_two() -> int:
    # example: int = __part_two__(PARENT.joinpath('example_2.txt'))
    # assert example == 281
    answer: int = __part_two__(PARENT.joinpath('matt_input.txt'))
    return answer


def main():
    print("Part One: {}".format(part_one()))
    print("Part Two: {}".format(part_two()))


if __name__ == '__main__':
    main()
