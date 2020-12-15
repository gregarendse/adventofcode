from typing import List, Dict


def part_one(starting_numbers: List[int], turn_count: int = 2020) -> int:
    previous_numbers: List[int] = starting_numbers.copy()
    previous_numbers.reverse()

    previous_number_map: Dict[int, int] = dict()

    for i, number in enumerate(starting_numbers[:-1]):
        previous_number_map[number] = i + 1

    next_number: int = 0
    previous_number = starting_numbers[-1]

    for i in range(len(starting_numbers), turn_count):

        last_turn = previous_number_map.get(previous_number)
        if last_turn is None:
            next_number = 0
        else:
            next_number = i - last_turn

        previous_number_map[previous_number] = i
        previous_number = next_number

    return next_number


with open('input.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        print(
            "{} {}".format(
                line.strip(),
                part_one([int(n) for n in line.split(',')], 2020)
            )
        )
    for line in lines:
        print(
            "{} {}".format(
                line.strip(),
                part_one([int(n) for n in line.split(',')], 30000000)
            )
        )
