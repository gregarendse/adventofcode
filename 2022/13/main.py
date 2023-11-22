#!/usr/bin/env python
import json
from functools import cmp_to_key
from pathlib import Path
from typing import Any, List, Optional, Tuple

PARENT = Path(__file__).parent


def read_from_file(file: Path) -> list[tuple[str, str]]:
    with open(file) as f:
        content = f.read()

        packets: List[Tuple[str, str]] = []

        for p in content.split("\n\n"):
            left, right = p.splitlines()
            packets.append((left, right))

        return packets


def compare(left, right) -> Optional[int]:

    for i in range(min(len(left), len(right))):
        if isinstance(left[i], int) and isinstance(right[i], int):
            if left[i] < right[i]:
                return 1
            if left[i] > right[i]:
                return -1
        else:
            if isinstance(left[i], int):
                left_list = [left[i]]
            else:
                left_list = left[i]
            if isinstance(right[i], int):
                right_list = [right[i]]
            else:
                right_list = right[i]
            result = compare(left_list, right_list)
            if result != 0:
                return result

    return len(right) - len(left)


def __part_one__(file: Path) -> int:
    packets: list[tuple[str, str]] = read_from_file(file)
    correct_order_indexes: List[int] = []

    for index, packet in enumerate(packets):
        left, right = packet

        left = json.loads(left)
        right = json.loads(right)

        correct_order: int = compare(left, right)
        if correct_order == 0:
            correct_order_indexes.append(index + 1)

    return sum(correct_order_indexes)


def __part_two__(file: Path) -> Optional[int]:
    packets: list[tuple[str, str]] = read_from_file(file)
    decoder_key_2 = "[[2]]"
    decoder_key_6 = "[[6]]"
    packets.append((decoder_key_2, decoder_key_6))
    packet_list: List[Any] = []
    for packet in packets:
        for p in packet:
            packet_list.append(
                json.loads(p)
            )
    packet_list = sorted(packet_list, key=cmp_to_key(compare), reverse=True)

    decoder_key_2_idx = packet_list.index(json.loads(decoder_key_2)) + 1
    decoder_key_6_idx = packet_list.index(json.loads(decoder_key_6)) + 1

    return decoder_key_6_idx * decoder_key_2_idx


def part_one() -> int:
    example: int = __part_one__(PARENT.joinpath('example.txt'))
    assert example == 13
    answer: int = __part_one__(PARENT.joinpath('input.txt'))
    return answer


def part_two() -> int:
    example: int = __part_two__(PARENT.joinpath('example.txt'))
    assert example == 140
    answer: int = __part_two__(PARENT.joinpath('input.txt'))
    return answer


def main():
    print("Part One: {}".format(part_one()))
    print("Part Two: {}".format(part_two()))


if __name__ == '__main__':
    main()
