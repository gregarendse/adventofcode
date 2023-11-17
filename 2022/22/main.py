#!/usr/bin/env python
import itertools
from pathlib import Path
from typing import Dict, Tuple

DIRECTIONS: list[tuple[int, int]] = [(1, 0), (0, 1), (-1, 0), (0, -1)]

PARENT = Path(__file__).parent


def read_from_file(file: Path) -> Tuple[dict[tuple[int, int], str], str]:
    with open(file) as f:
        board = dict()
        content = f.read()
        raw_board, path = content.split("\n\n")
        for y, line in enumerate(raw_board.splitlines()):
            for x, c in enumerate(line):
                if c in ['.', '#']:
                    board[(x, y)] = c
        return board, path


def add(a: Tuple[int, int], b: Tuple[int, int], maxes: Tuple[int, int]):
    return (a[0] + b[0]) % maxes[0], (a[1] + b[1]) % maxes[1]


def move(
        position: Tuple[int, int],
        direction: Tuple[int, int],
        board: Dict[Tuple[int, int], str],
        maxes: Tuple[int, int]
) -> Tuple[int, int]:
    new_position: Tuple[int, int] = add(position, direction, maxes)
    if new_position in board.keys():
        if board.get(new_position) == '.':
            return new_position
        elif board.get(new_position) == '#':
            return position
    else:
        # Wrap around the board
        while new_position not in board.keys():
            new_position = add(new_position, direction, maxes)
        if board.get(new_position) == '.':
            return new_position
        elif board.get(new_position) == '#':
            return position
    raise Exception("We shouldn't get here...")


def rotate(turn: str, direction: Tuple[int, int]) -> Tuple[int, int]:
    # ^   :   (0,-1)    *R  (1,0)   *L  (-1,0)
    # >   :   (1,0)     *R  (0,1)   *L  (0,-1)
    # v   :   (0,1)     *R  (-1,0)  *L  (1,0)
    # <   :   (-1,0)    *R  (0,-1)  *L  (0,1)

    possible_directions: list[tuple[int, int]] = DIRECTIONS

    index = possible_directions.index(direction)

    if "L" == turn:
        index -= 1
    elif "R" == turn:
        index += 1
    else:
        raise Exception("Unknown turn: " + turn)

    index = index % len(possible_directions)

    return possible_directions[index]


def facing(direction: Tuple[int, int]) -> int:
    return DIRECTIONS.index(direction)


def __part_one__(board, path) -> int:
    instructions = ["".join(v) for k, v in itertools.groupby(path, str.isdigit)]

    maxes: Tuple[int, int] = (
        max([x[0] + 1 for x in board.keys()]),
        max([x[1] + 1 for x in board.keys()]),
    )

    position: Tuple[int, int] = (min([x[0] for x in board.keys() if x[1] == 0]), 0)
    dir: Tuple[int, int] = (1, 0)  # Facing right

    for inst in instructions:
        if inst.isnumeric():
            for _ in range(int(inst)):
                position = move(position, dir, board, maxes)

        elif inst in ['L', 'R']:
            dir = rotate(inst, dir)

        else:
            raise Exception("Not good...")
    x, y = position
    return sum([4 * (x + 1), 1000 * (y + 1), facing(dir)])


def __part_two__(file: Path) -> int:
    content: str = read_from_file(file)
    return 0


def part_one() -> int:
    board, path = read_from_file(PARENT.joinpath('example.txt'))
    example: int = __part_one__(board, path)
    assert example == 6032
    assert __part_one__(board, "1R") == 1041
    assert __part_one__(board, "2R") == 1045
    assert __part_one__(board, "3R") == 1045
    assert __part_one__(board, "1L") == 1043
    assert __part_one__(board, "2L") == 1047
    assert __part_one__(board, "1L1L1L1L") == 1036

    board, path = read_from_file(PARENT.joinpath('input.txt'))
    answer: int = __part_one__(board, path)
    return answer


def part_two() -> int:
    example: int = __part_two__(PARENT.joinpath('example.txt'))
    assert example == 5031
    answer: int = __part_two__(PARENT.joinpath('input.txt'))
    return answer


def main():
    assert rotate('R', (0, -1)) == (1, 0)
    assert rotate('L', (0, -1)) == (-1, 0)
    assert rotate('R', (1, 0)) == (0, 1)
    assert rotate('L', (1, 0)) == (0, -1)

    # ^   :   (0,-1)    *R  (1,0)   *L  (-1,0)
    # >   :   (1,0)     *R  (0,1)   *L  (0,-1)
    # v   :   (0,1)     *R  (-1,0)  *L  (1,0)
    # <   :   (-1,0)    *R  (0,-1)  *L  (0,1)

    print("Part One: {}".format(part_one()))
    print("Part Two: {}".format(part_two()))


if __name__ == '__main__':
    main()
