#!/usr/bin/env python
from collections import deque
from pathlib import Path
from typing import List, Tuple

PARENT = Path(__file__).parent


def read_from_file(file: Path) -> list[tuple[list[int], list[int]]]:
    with open(file) as f:
        cards: List[Tuple[List[int], List[int]]] = []
        for line in f.readlines():
            winning_str, number_str = line.split(':')[1].split('|')

            winning: List[int] = [int(x) for x in winning_str.split()]
            numbers: List[int] = [int(x) for x in number_str.split()]

            cards.append((winning, numbers))

        return cards


def __part_one__(file: Path) -> int:
    cards = read_from_file(file)

    scores = []

    for card in cards:
        both = set(card[0]) & set(card[1])
        n = len(both)

        if n > 0:
            score = 2 ** (n - 1)
        else:
            score = 0

        scores.append(score)

    return sum(scores)


def __part_two__(file: Path) -> int:
    cards = read_from_file(file)

    scores = []

    kept_cards = deque([1])

    for card in cards:
        both = set(card[0]) & set(card[1])
        n = len(both)

        number_of_cards = kept_cards.popleft()
        kept_cards.append(1)

        for i in range(n):
            if len(kept_cards) <= i:
                kept_cards.append(1)
            kept_cards[i] += 1 * number_of_cards

        scores.append(number_of_cards)

    return sum(scores)


def part_one() -> int:
    example: int = __part_one__(PARENT.joinpath('example.txt'))
    assert example == 13
    answer: int = __part_one__(PARENT.joinpath('input.txt'))
    return answer


def part_two() -> int:
    example: int = __part_two__(PARENT.joinpath('example.txt'))
    assert example == 30
    answer: int = __part_two__(PARENT.joinpath('input.txt'))
    return answer


def main():
    print("Part One: {}".format(part_one()))
    print("Part Two: {}".format(part_two()))


if __name__ == '__main__':
    main()
