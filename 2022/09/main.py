#!/use/bin/env python
from dataclasses import dataclass
from sys import argv
from typing import List, Tuple, Set


def read_file(file: str) -> List[Tuple[str, int]]:
    with open(file, 'r') as f:
        moves: List[Tuple[str, int]] = []
        for line in f.readlines():
            [direction, count] = line.split(' ')
            moves.append(tuple((direction, int(count))))
        return moves


@dataclass
class Position(object):
    x: int
    y: int

    def adjacent(self, head_position) -> bool:
        if self.x in [head_position.x - 1, head_position.x, head_position.x + 1] \
                and self.y in [head_position.y - 1, head_position.y, head_position.y + 1]:
            return True
        return False

    def move_towards(self, head_position):
        if self.x - head_position.x >= 1:
            self.x -= 1
        elif head_position.x - self.x >= 1:
            self.x += 1
        if self.y - head_position.y >= 1:
            self.y -= 1
        elif head_position.y - self.y >= 1:
            self.y += 1

    def copy(self):
        return Position(self.x, self.y)

    def __hash__(self):
        return hash(self.x) + hash(self.y)


def part_one(file: str) -> int:
    moves: List[Tuple[str, int]] = read_file(file)

    head_position: Position = Position(0, 0)
    tail_position: Position = Position(0, 0)
    tail_positions: Set[Position] = set()

    for move in moves:
        for i in range(move[1]):
            if "R" == move[0]:
                head_position.x += 1
            elif "U" == move[0]:
                head_position.y += 1
            elif "L" == move[0]:
                head_position.x -= 1
            elif "D" == move[0]:
                head_position.y -= 1
            else:
                print("Problem " + str(move))
            if not tail_position.adjacent(head_position):
                tail_position.move_towards(head_position)
            tail_positions.add(tail_position.copy())

    return len(tail_positions)


def part_two(file: str) -> int:
    moves: List[Tuple[str, int]] = read_file(file)

    rope: List[Position] = [Position(0, 0) for i in range(10)]
    tail_positions: Set[Position] = set()

    for move in moves:
        for i in range(move[1]):
            if "R" == move[0]:
                rope[0].x += 1
            elif "U" == move[0]:
                rope[0].y += 1
            elif "L" == move[0]:
                rope[0].x -= 1
            elif "D" == move[0]:
                rope[0].y -= 1
            else:
                print("Problem " + str(move))

            for i in range(1, len(rope)):
                if not rope[i].adjacent(rope[i - 1]):
                    rope[i].move_towards(rope[i - 1])

            tail_positions.add(rope[-1].copy())

    return len(tail_positions)


def main():
    print("Part One: {}".format(part_one(argv[1])))
    print("Part Two: {}".format(part_two(argv[1])))


if __name__ == '__main__':
    main()
