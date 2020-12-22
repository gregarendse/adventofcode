import copy
from typing import List, Dict


def part_one(players: List[List[int]]) -> int:
    while min([len(player) for player in players]):
        round: Dict[int, int] = dict()

        for player_id, player in enumerate(players):
            round[player.pop(0)] = player_id

        winner = round[max(round.keys())]
        players[winner].extend(sorted(round.keys(), reverse=True))

    winner: List[int] = []
    for player in players:
        if len(player) > 0:
            winner = player
            break

    return sum([i * v for i, v in enumerate(reversed(winner), 1)])


def part_two(players: List[List[int]]) -> int:
    winner: int = game(players)
    return sum([i * v for i, v in enumerate(reversed(players[winner]), 1)])


def game(players: List[List[int]]) -> int:
    previous_rounds = set()

    while min([len(player) for player in players]):
        t = (tuple(players[0]), tuple(players[1]))
        if t in previous_rounds:
            return 0
        previous_rounds.add(t)

        round: Dict[int, int] = dict()
        cards: Dict[int, int] = dict()

        for player_id, player in enumerate(players):
            card: int = player.pop(0)
            round[card] = player_id
            cards[player_id] = card

        sub_game: bool = True
        for key, value in round.items():
            sub_game &= len(players[value]) >= key

        if sub_game:
            winner: int = game([copy.deepcopy(player[:cards[i]]) for i, player in enumerate(players)])
        else:
            winner: int = round[max(round.keys())]

        players[winner].append(cards[winner])
        players[winner].append(cards[len(cards) - winner - 1])

    for i, player in enumerate(players):
        if len(player) > 0:
            return i


with open('input.txt', 'r') as file:
    read = file.read()

    players: List[List[int]] = [[int(v) for v in player.splitlines()[1:]] for player in read.split('\n\n')]

    print(part_one(copy.deepcopy(players)))
    print(part_two(copy.deepcopy(players)))
