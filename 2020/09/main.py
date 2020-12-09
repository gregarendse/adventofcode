from typing import List, Optional

lines: List[int] = []
preamble_size: int = 25
with open('input.txt', 'r') as file:
    for line in file.readlines():
        lines.append(int(line))


def is_valid(preamble: List[int], number: int) -> bool:
    for i in preamble:
        for j in preamble:
            if i == j:
                continue
            if i + j == number:
                return True
    return False


def find_invalid() -> Optional[int]:
    for _i in range(preamble_size, len(lines)):
        if not is_valid(lines[_i - preamble_size:_i], lines[_i]):
            return lines[_i]
    return None


def find_sum_list() -> Optional[int]:
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            part = lines[i:j]
            number_sum: int = sum(part)
            if number_sum == invalid_number and len(part) > 1:
                return min(part) + max(part)
            elif number_sum > invalid_number:
                break
    return None


invalid_number: Optional[int] = find_invalid()
min_max_sum: Optional[int] = find_sum_list()
print(invalid_number)
print(min_max_sum)
