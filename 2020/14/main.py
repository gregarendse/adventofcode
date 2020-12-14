import re
import copy
from typing import List, Set


def get_memory_address(memory: {}, address: int) -> int:
    value: int = memory.get(address)

    if value is None:
        return 0
    else:
        return value


def set_memory_address(memory: {}, address: int, value: int, mask: str) -> None:
    bin_value = [str(0) for _ in range(len(mask) - len(bin(value)))]
    bin_value.extend(bin(value).replace('b', '0'))

    for i, v in enumerate(mask):
        if bin_value == v:
            continue
        elif v != 'X':
            bin_value[i] = v

    memory[address] = int("".join(bin_value), 2)


def set_all_memory_addresses(memory: {}, address: int, value: int, mask: str) -> None:
    bin_address: List[str] = [str(0) for _ in range(len(mask) - len(bin(address)))]
    bin_address.extend(bin(address).replace('b', '0'))

    x_count: int = 0
    for i, v in enumerate(mask):
        if v == '1':
            bin_address[i] = v
        elif v == 'X':
            x_count += 1
            bin_address[i] = 'X'

    bin_max = pow(2, x_count)
    for i in range(bin_max):
        address_copy = bin_address.copy()
        bin_i = [str(0) for _ in range(x_count)]
        bin_i.extend(bin(i)[2:])

        iteration: int = 0
        for j, v in enumerate(address_copy):
            if v == 'X':
                iteration += 1
                address_copy[j] = str(bin_i[len(bin_i) - iteration])

        set_address = int("".join(address_copy), 2)
        memory[set_address] = value




pattern = re.compile('\w+\[(?P<address>\d+)\]\s+=\s+(?P<value>\d+)')


def part_one(lines: List[str]):
    memory: {} = {}

    for _line in lines:
        _mask: str
        if _line.startswith('mask'):
            parts = _line.split("=")
            _mask = str(parts[1].strip())
        elif _line.startswith('mem'):
            match = pattern.match(_line)
            set_memory_address(memory, int(match.groupdict()['address']), int(match.groupdict()['value']), _mask)

    return sum(memory.values())


def part_two(lines: List[str]):
    memory: {} = {}

    for _line in lines:
        _mask: str
        if _line.startswith('mask'):
            parts = _line.split("=")
            _mask = str(parts[1].strip())
        elif _line.startswith('mem'):
            match = pattern.match(_line)
            set_all_memory_addresses(memory, int(match.groupdict()['address']), int(match.groupdict()['value']), _mask)

    return sum(memory.values())


with open('input.txt', 'r') as file:
    readlines: List[str] = file.readlines()
    print(part_one(readlines))
    print(part_two(readlines))
