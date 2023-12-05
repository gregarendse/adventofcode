#!/usr/bin/env python
from dataclasses import dataclass
from pathlib import Path
from typing import List

PARENT = Path(__file__).parent


@dataclass
class Game(object):
    blue: int = 0
    red: int = 0
    green: int = 0


def read_from_file(file: Path) -> str:
    with open(file) as f:
        games: List[Game] = []
        for line in f.readlines():
            game: Game = Game()
            for round in line.split(':')[1].split(';'):
                for item in round.split(','):
                    count, color = item.split()
                    count = int(count)

                    if color == 'blue':
                        game.blue = max(game.blue, count)
                    elif color == 'red':
                        game.red = max(game.red, count)
                    elif color == 'green':
                        game.green = max(game.green, count)
                    else:
                        raise Exception
            games.append(game)

        return games


def __part_one__(file: Path) -> int:
    games = read_from_file(file)

    possible: List[int] = []

    for idx, game in enumerate(games):
        # only 12 red cubes, 13 green cubes, and 14 blue cubes
        if game.red <= 12 and game.green <= 13 and game.blue <= 14:
            possible.append(idx + 1)

    return sum(possible)


def __part_two__(file: Path) -> int:
    games = read_from_file(file)

    powers: List[int] = []

    for idx, game in enumerate(games):
        powers.append(
            game.blue * game.red * game.green
        )

    return sum(powers)


def part_one() -> int:
    example: int = __part_one__(PARENT.joinpath('example.txt'))
    assert example == 8
    answer: int = __part_one__(PARENT.joinpath('input.txt'))
    return answer


def part_two() -> int:
    example: int = __part_two__(PARENT.joinpath('example.txt'))
    assert example == 2286
    answer: int = __part_two__(PARENT.joinpath('input.txt'))
    return answer


def main():
    print("Part One: {}".format(part_one()))
    print("Part Two: {}".format(part_two()))


if __name__ == '__main__':
    main()
