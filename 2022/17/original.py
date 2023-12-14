#!/use/bin/env python
from dataclasses import dataclass
from sys import argv
from typing import List


@dataclass
class Rock:
    top: List[int]
    right: List[int]
    bottom: List[int]
    left: List[int]

    next: int

    x: int = 2  # Each rock appears so that its left edge is two units away from the left wall
    y: int = 0


shapes: List[Rock] = [
    # @@@@
    Rock(top=[1, 1, 1, 1], right=[4], bottom=[0, 0, 0, 0], left=[0], next=1),
    # .@.
    # @@@
    # .@.
    Rock(top=[2, 3, 2], right=[2, 3, 2], bottom=[1, 0, 1], left=[1, 0, 1], next=2),
    # ..@
    # ..@
    # @@@
    Rock(top=[1, 1, 3], right=[3, 3, 3], bottom=[0, 0, 0], left=[0, 2, 2], next=3),
    # @
    # @
    # @
    # @
    Rock(top=[4], right=[1, 1, 1, 1], bottom=[0], left=[0, 0, 0, 0], next=4),
    # @@
    # @@
    Rock(top=[2, 2], right=[2, 2], bottom=[0, 0], left=[0, 0], next=0)
]


def read_from_file(file: str) -> str:
    with open(file) as f:
        jet_patterns: str = f.readline().strip()
    return jet_patterns


def display(heights: List[int]) -> None:
    for height in heights:
        print("{}".format(height), end='\t')
    print()


def part_one(file: str) -> int:
    # Build window
    # loop:
    # drop rock
    # map landing
    # move window
    # keep track of current height

    jet_patterns: str = read_from_file(file)

    # 7 unites wide
    heights: List[int] = [0, 0, 0, 0, 0, 0, 0]

    rock: Rock = shapes[0]
    # 3 units above
    rock.y = 3
    rock.x = 2

    i: int = 0
    rock_count: int = 0

    while rock_count < 2022:
        jet_direction: str = jet_patterns[i % len(jet_patterns)]
        if '>' == jet_direction:
            # check that we are in the
            if rock.x + max(rock.right) + 1 <= 7:
                # check that there is nothing on the right edge
                clear: bool = True
                if max(heights) > rock.y:
                    for index, edge in enumerate(rock.right):
                        if heights[rock.x + edge] > rock.y + index:
                            clear = False
                            break
                if clear:
                    rock.x += 1
        elif '<' == jet_direction:
            # x with will ways be the bottom left of the rock
            if rock.x - 1 >= 0:
                clear: bool = True
                if max(heights) > rock.y:
                    for index, edge in enumerate(rock.left):
                        if heights[rock.x + edge - 1] > rock.y + index:
                            clear = False
                            break
                if clear:
                    rock.x -= 1
        else:
            print('FAIL!')

        clear: bool = True
        if max(heights) >= rock.y:
            for index, y_delta in enumerate(rock.bottom):
                if heights[rock.x + index] >= rock.y + y_delta:
                    clear = False
                    break

        if clear:
            rock.y -= 1
        else:
            for index, y_delta in enumerate(rock.top):
                heights[rock.x + index] = rock.y + y_delta

            # Select next rock
            rock = shapes[rock.next]
            # reset rock position
            rock.x = 2
            rock.y = max(heights) + 3
            rock_count += 1

        i += 1

    return max(heights)


def part_two(file: str) -> int:
    return None


def main(file: str):
    if file is None:
        file = argv[1]
    print("Part One: {}".format(part_one(file)))
    print("Part Two: {}".format(part_two(file)))


if __name__ == '__main__':
    main(file='example.txt')
