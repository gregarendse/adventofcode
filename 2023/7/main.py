#!/usr/bin/env python
from collections import defaultdict
from dataclasses import dataclass
from functools import cmp_to_key
from pathlib import Path
from typing import Dict, List

PARENT = Path(__file__).parent


@dataclass
class Card(object):
    type: str
    value: int

    def __repr__(self):
        return self.type


class Hand(object):
    cards: List[Card]
    card_dict: Dict[int, int]

    def __init__(self, cards: List, bid: int):
        super().__init__()
        self.cards = list(cards)
        self.bid = int(bid)

        self.card_dict: Dict[int, int] = defaultdict(int)
        jokers: int = 0
        for card in cards:
            self.card_dict[card.value] += 1
            if card.value == 0:
                jokers += 1

        if jokers:
            jokers: int = self.card_dict.pop(0)
            #         we have Jokers, power up?

            v_max_value = 0
            v_max_key = 0
            for key, value in self.card_dict.items():
                if v_max_value <= value:
                    if v_max_value == value:
                        v_max_key = max(v_max_key, key)
                    else:
                        v_max_key = key

                    v_max_value = value

            key_set = set(self.card_dict.keys())
            key_set_len = len(key_set)

            # 5 & 4
            if v_max_value + jokers >= 4:
                self.card_dict[v_max_key] += jokers

            # full house
            elif key_set_len <= 2:
                if key_set_len == 0:
                    self.card_dict[0] = 0
                    self.card_dict[1] = 0
                elif key_set_len == 1:
                    self.card_dict[0] = 0
                elif key_set_len == 2:
                    pass

                while jokers > 0:
                    for key, value in self.card_dict.items():
                        if value < 3:
                            self.card_dict[key] += 1
                            jokers -= 1
                        if jokers == 0:
                            break
            # 3 of a kind
            # pairs...
            else:
                # elif v_max_value + jokers == 3:
                self.card_dict[v_max_key] += jokers

    def __repr__(self):
        return f"{self.cards} {self.bid}"


def card_cmp(s: List[Card], o: List[Card]) -> int:
    for i in range(len(s)):
        if s[i].value != o[i].value:
            return s[i].value - o[i].value
    return 0


def cmp(s: Hand, o: Hand) -> int:
    """
Five of a kind, where all five cards have the same label: AAAAA
Four of a kind, where four cards have the same label and one card has a different label: AA8AA
Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
High card, where all cards' labels are distinct: 23456
    """
    s_max = max(s.card_dict.values())
    o_max = max(o.card_dict.values())

    # 5 of a kind
    # 4 of a kind
    if s_max >= 4 or o_max >= 4:
        if s_max == o_max:
            return card_cmp(s.cards, o.cards)
        else:
            return s_max - o_max

    s_set = set(s.card_dict.keys())
    s_set_len = len(s_set)
    o_set = set(o.card_dict.keys())
    o_set_len = len(o_set)

    #     full house
    if s_set_len == 2 or o_set_len == 2:
        if s_set_len == 2 and o_set_len == 2:
            return card_cmp(s.cards, o.cards)
        elif s_set_len == 2:
            return 1
        else:
            return -1

    #  3 of a kind
    if s_max == 3 or o_max == 3:
        if s_max == 3 and o_max == 3:
            return card_cmp(s.cards, o.cards)
        else:
            return s_max - o_max

    # 2 pair
    if (s_max == 2 and s_set_len == 3) or (o_max == 2 and o_set_len == 3):
        if (s_max == 2 and s_set_len == 3) and (o_max == 2 and o_set_len == 3):
            return card_cmp(s.cards, o.cards)
        else:
            if s_max == 2 and s_set_len == 3:
                return 1
            else:
                # (o_max == 2 and o_set == 2))
                return -1

    # 1 pair
    if s_max == 2 or o_max == 2:
        if s_max == 2 and o_max == 2:
            return card_cmp(s.cards, o.cards)
        else:
            return s_max - o_max

    # High cards
    return card_cmp(s.cards, o.cards)


def read_from_file(file: Path) -> list[Hand]:
    hands: List[Hand] = []
    with open(file) as f:
        for line in f.readlines():
            a, b = line.split()

            cards: List[Card] = []
            for c in a:
                idx = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A'].index(c)
                card = Card(type=str(c), value=int(idx))
                cards.append(card)

            hand: Hand = Hand(cards=cards, bid=int(b))

            hands.append(hand)

    return hands


def __part_one__(file: Path) -> int:
    hands: list[Hand] = read_from_file(file)

    hands.sort(key=cmp_to_key(cmp))

    total: int = 0
    for idx, hand in enumerate(hands):
        total += (idx + 1) * hand.bid

    return total


def __part_two__(file: Path) -> int:
    hands: list[Hand] = read_from_file(file)

    hands.sort(key=cmp_to_key(cmp))
    print("\n".join([str(hand) for hand in hands]))

    total: int = 0
    for idx, hand in enumerate(hands):
        total += (idx + 1) * hand.bid

    return total


def part_one() -> int:
    example_file = PARENT.joinpath('example.txt')
    hands: list[Hand] = read_from_file(example_file)

    h1 = sorted(hands[:2], key=cmp_to_key(cmp))
    print(h1)
    assert h1[0].bid == 765
    assert h1[1].bid == 684

    h1 = sorted(hands[1:3], key=cmp_to_key(cmp))
    print(h1)
    assert h1[0].bid == 28
    assert h1[1].bid == 684

    h1 = sorted(hands[2:4], key=cmp_to_key(cmp))
    print(h1)
    assert h1[0].bid == 220
    assert h1[1].bid == 28

    h1 = sorted(hands[3:5], key=cmp_to_key(cmp))
    print(h1)
    assert h1[0].bid == 220
    assert h1[1].bid == 483

    example: int = __part_one__(example_file)
    assert example == 6440
    answer: int = __part_one__(PARENT.joinpath('input.txt'))
    return answer


def part_two() -> int:
    path = PARENT.joinpath('example_2.txt')
    hands: list[Hand] = read_from_file(path)

    for hand in hands:
        print(hand)
        for o in hands:
            result = cmp(hand, o)
            print(f"  {o} : {result}")

    hands.sort(key=cmp_to_key(cmp))

    assert hands[2].bid == 3

    example: int = __part_two__(PARENT.joinpath('example.txt'))
    assert example == 5905
    answer: int = __part_two__(PARENT.joinpath('input.txt'))
    return answer


def main():
    print("Part One: {}".format(part_one()))
    print("Part Two: {}".format(part_two()))


if __name__ == '__main__':
    main()
