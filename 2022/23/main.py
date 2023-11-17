#!/usr/bin/env python
from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Set

PARENT = Path(__file__).parent


@dataclass
class Elf(object):
    x: int
    y: int

    def __hash__(self):
        return hash(self.x) + hash(self.y)

    def __eq__(self, __o):
        return self.x == __o.x and self.y == __o.y

    def __add__(self, other):
        return Elf(
            x=self.x + other.x,
            y=self.y + other.y
        )


def read_from_file(file: Path) -> set[Elf]:
    # elf_map: Dict[Tuple[int, int], str] = dict()
    elves: Set[Elf] = set()
    with open(file) as f:
        for y, line in enumerate(f.readlines()):
            for x, c in enumerate(line):
                if c == '#':
                    elves.add(Elf(x=int(x), y=int(y)))
                    # elf_map[(x, y)] = c
        return elves


def get_next_position(elf: Elf, current_positions: Set[Elf], counter: int = 0) -> Elf:
    #       N           0:  (x,y)
    #       |           1:  (0,1)
    #    8  1  2        2:  (1,1)
    #       |           3:  (1,0)
    # W--7-----3--E     4:  (1,-1)
    #       |           5:  (0,-1)
    #    6  5  4        6:  (-1,-1)
    #       |           7:  (-1,0)
    #       S           8:  (-1,1)

    movements: Dict[Elf, List[Elf]] = dict()
    # N
    movements[Elf(x=0, y=-1)] = [Elf(x=-1, y=-1), Elf(x=0, y=-1), Elf(x=1, y=-1)]
    # S
    movements[Elf(x=0, y=1)] = [Elf(x=-1, y=1), Elf(x=0, y=1), Elf(x=1, y=1)]
    # W
    movements[Elf(x=-1, y=0)] = [Elf(x=-1, y=-1), Elf(x=-1, y=0), Elf(x=-1, y=1)]
    # E
    movements[Elf(x=1, y=0)] = [Elf(x=1, y=-1), Elf(x=1, y=0), Elf(x=1, y=1)]

    possible_directions = deque(movements.keys())
    possible_directions.rotate(-counter)

    for direction, sub_directions in movements.items():
        for sub_direction in sub_directions:
            new_position = sub_direction + elf
            if new_position in current_positions:
                possible_directions.remove(direction)
                break

    if 0 < len(possible_directions) < 4:
        return elf + possible_directions.popleft()
    else:
        # No movement
        return elf


def process(elves: Set[Elf], counter: int = 0) -> Set[Elf]:
    # Keep track of all the elves wanting to move to the 'same' point. If only one elf wants to move there they can;
    # otherwise no-one moves
    possible_moves: Dict[Elf, List[Elf]] = defaultdict(list)

    # Find possible moves for each elf

    for elf in elves:
        next_position = get_next_position(elf, elves, counter)
        possible_moves[next_position].append(elf)

    moved_elves: Set[Elf] = set()

    for next_position, e in possible_moves.items():
        if len(e) == 1:
            moved_elves.add(next_position)
        else:
            for unmoved in e:
                moved_elves.add(unmoved)

    return moved_elves


def __part_one__(file: Path) -> int:
    elves: Set[Elf] = read_from_file(file)

    for i in range(10):
        elves = process(elves, i)

    elf = next(iter(elves))
    min_x: int = elf.x  # -3
    max_x: int = elf.x  # 9
    min_y: int = elf.y  # 2
    max_y: int = elf.y  # 5

    for elf in elves:
        min_x = min(min_x, elf.x)
        max_x = max(max_x, elf.x)
        min_y = min(min_y, elf.y)
        max_y = max(max_y, elf.y)

    x: int = max_x - min_x + 1  # 12
    y: int = max_y - min_y + 1  # 3
    ans: int = x * y  # 36
    ans -= len(elves)
    return ans


def __part_two__(file: Path) -> int:
    current_positions: Set[Elf] = read_from_file(file)
    next_positions = process(current_positions)

    counter: int = 1
    while current_positions != next_positions:
        current_positions = next_positions
        next_positions = process(current_positions, counter)
        counter += 1
    return counter


def part_one() -> int:

    elves: Set[Elf] = read_from_file(PARENT.joinpath("example_1.txt"))
    elves = process(elves)
    expected_state: Set[Elf] = read_from_file(PARENT.joinpath("state_1_1.txt"))
    assert len(elves.symmetric_difference(expected_state)) == 0
    elves = process(elves, 1)
    expected_state: Set[Elf] = read_from_file(PARENT.joinpath("state_1_2.txt"))
    assert elves == expected_state
    elves = process(elves, 2)
    expected_state: Set[Elf] = read_from_file(PARENT.joinpath("state_1_3.txt"))
    assert elves == expected_state

    elves: Set[Elf] = read_from_file(PARENT.joinpath("example_2.txt"))
    for state in range(5):
        elves = process(elves, state)
        expected_state: Set[Elf] = read_from_file(PARENT.joinpath(f"state_2_{state + 1}.txt"))
        assert len(elves.symmetric_difference(expected_state)) == 0

    example: int = __part_one__(PARENT.joinpath('example_2.txt'))
    assert example == 110
    answer: int = __part_one__(PARENT.joinpath('input.txt'))
    return answer


def part_two() -> int:
    example: int = __part_two__(PARENT.joinpath('example_2.txt'))
    assert example == 20
    answer: int = __part_two__(PARENT.joinpath('input.txt'))
    return answer


def main():
    # print("Part One: {}".format(part_one()))
    print("Part Two: {}".format(part_two()))


if __name__ == '__main__':
    main()
