#!/usr/bin/env python
from pathlib import Path

PARENT = Path(__file__).parent


def read_from_file(file: Path) -> str:
    with open(file) as f:
        return f.read()


def __part_one__(file: Path) -> int:
    raise Exception("Not implemented")
    content: str = read_from_file(file)
    return 0


def __part_two__(file: Path) -> int:
    raise Exception("Not implemented")
    content: str = read_from_file(file)
    return 0


def part_one() -> int:
    example: int = __part_one__(PARENT.joinpath('example.txt'))
    assert example == {part_one_example_answer}
    answer: int = __part_one__(PARENT.joinpath('input.txt'))
    return answer


def part_two() -> int:
    example: int = __part_two__(PARENT.joinpath('example.txt'))
    assert example == {part_two_example_answer}
    answer: int = __part_two__(PARENT.joinpath('input.txt'))
    return answer


def main():
    print("Part One: {{}}".format(part_one()))
    print("Part Two: {{}}".format(part_two()))


if __name__ == '__main__':
    main()
