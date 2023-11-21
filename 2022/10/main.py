#!/usr/bin/env python
from pathlib import Path
from typing import List

PARENT = Path(__file__).parent


def read_from_file(file: Path) -> list[int]:
    with open(file) as f:
        instructions: List[int] = []
        for line in f.readlines():
            parts = line.split()
            if len(parts) == 1:
                instructions.append(0)
            elif len(parts) == 2:
                instructions.append(int(parts[1]))
            else:
                raise Exception("Shouldn't get here...")
        return instructions


def __part_one__(file: Path) -> int:
    instructions: List[int] = read_from_file(file)

    signal_strengths: List[int] = []
    x: int = 1
    program_index: int = 0

    for instruction in instructions:
        cycles: int = 2 if instruction else 1

        for i in range(cycles):
            program_index += 1

            if program_index in [20, 60, 100, 140, 180, 220]:
                signal_strengths.append(x * program_index)

            if i == 1:
                x += instruction

    return sum(signal_strengths)


def __part_two__(file: Path) -> str:
    display: List[str] = ['.' for _ in range(240)]
    instructions: List[int] = read_from_file(file)
    x: int = 1
    program_index: int = 0

    for instruction in instructions:
        cycles: int = 2 if instruction else 1

        for i in range(cycles):
            if (program_index % 40) - 1 <= x <= (program_index % 40) + 1:
                display[program_index] = '#'
            if i == 1:
                x += instruction
            program_index += 1

    output: str = ""
    for i in range(6):
        output += "".join(display[i * 40:(i + 1) * 40])
        output += "\n"
    print(output)
    return output.strip()


def part_one() -> int:
    # example: int = __part_one__(PARENT.joinpath('example_2.txt'))
    example: int = __part_one__(PARENT.joinpath('example.txt'))
    assert example == 13140

    answer: int = __part_one__(PARENT.joinpath('input.txt'))
    return answer


def part_two() -> int:
    example: str = __part_two__(PARENT.joinpath('example.txt'))
    expected = """
##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....
""".strip()
    assert example == expected
    answer: str = __part_two__(PARENT.joinpath('input.txt'))
    print(answer)


def main():
    print("Part One: {}".format(part_one()))
    print("Part Two: {}".format(part_two()))


if __name__ == '__main__':
    main()
