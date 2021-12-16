#!/bin/python

from typing import List


def decode_literal(bin_str: str, values: List[int]) -> int:
    literal_bin: str = ""

    for i in range(0, len(bin_str), 5):
        literal_bin += bin_str[i+1:i+5]
        if bin_str[i] == '0':
            break

    values.append(int(literal_bin, 2))

    return i + 5


def decode_packet(bin_str: str, version_numbers: List[int] = [], values: List[int] = []):
    index: int = 0
    version: int = int(bin_str[index:index+3], 2)
    index += 3
    version_numbers.append(version)
    type_id: int = int(bin_str[index:index+3], 2)
    index += 3

    if 4 == type_id:
        return index + decode_literal(bin_str[index:], values)
    else:
        sub_values: List[int] = []
        length_type_id: int = int(bin_str[index:index+1])
        index += 1
        if 0 == length_type_id:
            total_length_bits = int(bin_str[index:index+15], 2)
            index += 15
            end = index + total_length_bits

            while index < end:
                index += decode_packet(
                    bin_str=bin_str[index:end],
                    version_numbers=version_numbers,
                    values=sub_values
                )

        elif 1 == length_type_id:
            sub_packet_count_bits = int(bin_str[index:index+11], 2)
            index += 11

            for i in range(sub_packet_count_bits):
                index += decode_packet(
                    bin_str=bin_str[index:],
                    version_numbers=version_numbers,
                    values=sub_values
                )

        if 0 == type_id:
            values.append(sum(sub_values))
        elif 1 == type_id:
            product: int = 1
            for value in sub_values:
                product *= value
            values.append(product)
        elif 2 == type_id:
            values.append(min(sub_values))
        elif 3 == type_id:
            values.append(max(sub_values))
        elif 5 == type_id:
            values.append(1 if sub_values[0] > sub_values[1] else 0)
        elif 6 == type_id:
            values.append(1 if sub_values[0] < sub_values[1] else 0)
        elif 7 == type_id:
            values.append(1 if sub_values[0] == sub_values[1] else 0)

    return index


with open('2021/16/input.txt', 'r') as file:
    for line in file.readlines():
        bin_str: str = format(int(line, 16), f'#0{2 + len(line) * 4}b')[2:]

        version_numbers: List[int] = []
        values: List[int] = []
        decode_packet(bin_str, version_numbers=version_numbers, values=values)

        print(sum(version_numbers))
        print(values[0])
