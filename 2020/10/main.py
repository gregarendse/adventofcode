from typing import List

import time

lines: List[int] = []
with open('example.txt', 'r') as file:
    for line in file.readlines():
        lines.append(int(line))

lines.append(0)
lines.sort()
lines.append(max(lines) + 3)

differences: {int, int} = {1: 0, 2: 0, 3: 0}
diffs: List[int] = []

input: int = 0
output: int = max(lines) + 3

for i in range(1, len(lines)):
    current = lines[i]
    prev = lines[i - 1]
    diff = (current - prev)

    if diff <= 3:
        diffs.append(diff)
        differences[diff] += 1

print(differences)
print((differences[1]) * (differences[3]))


def find_option(adaptors: List[int], memory: {}) -> int:
    _count: int = 0
    last = max(adaptors)

    if len(adaptors) == 1:
        return 1

    for i in range(1, 4):
        if 0 <= i < len(adaptors) and adaptors[-i - 1] is not None:
            _count += find_option(adaptors[:-i], memory)

    memory[last] = _count
    return _count


def find_option_rev(adaptors: List[int], path: List[int] = [], count: int = 0) -> int:
    adaptor_len: int = len(adaptors)
    if adaptor_len == 1:
        return 1

    current = adaptors[adaptor_len - 1]
    new_path = [current]
    for p in path:
        new_path.append(p)

    try:
        index = adaptors.index(current - 1)
        count = count + find_option_rev(adaptors[:index + 1], new_path)
    except ValueError:
        pass

    try:
        index = adaptors.index(current - 2)
        count = count + find_option_rev(adaptors[:index + 1], new_path)
    except ValueError:
        pass

    try:
        index = adaptors.index(current - 3)
        count = count + find_option_rev(adaptors[:index + 1], new_path)
    except ValueError:
        pass

    # for _i in range(adaptor_len(adaptors)):
    #     if adaptors[_i] + 1 in adaptors:
    #         # print(adaptors[_i] + 1, end=" ")
    #         index = adaptors.index(adaptors[_i] + 1)
    #         copy = path.copy()
    #         copy.append(adaptors[_i])
    #         count = find_option(adaptors[index:], copy, count) + count
    #
    #     if adaptors[_i] + 2 in adaptors:
    #         # print(adaptors[_i] + 2, end=' ')
    #         index = adaptors.index(adaptors[_i] + 2)
    #         copy = path.copy()
    #         copy.append(adaptors[_i])
    #         count = find_option(adaptors[index:], copy, count) + count
    #
    #     if adaptors[_i] + 3 in adaptors:
    #         # print(adaptors[_i] + 3, end=" ")
    #         index = adaptors.index(adaptors[_i] + 3)
    #         copy = path.copy()
    #         copy.append(adaptors[_i])
    #         count = find_option(adaptors[index:], copy, count) + count

    # print("adaptor_len: " + str(adaptor_len(adaptors)))

    return count


def fib(input: int):
    if input < 2:
        return 1
    return max(1, fib(input - 1)) + input


def find_options(diffs: List[int]) -> List[int]:
    _options: int = 0
    _variations: List[int] = [1 for _ in diffs]
    for _i in range(len(diffs)):
        current: int = diffs[_i]
        if _i > 1 and current - diffs[_i - 1] == 1:
            _variations[_i - 1] += 1
        if _i > 2 and current - diffs[_i - 1] == 2:
            _variations[_i - 2] += 1
        # if _i > 3 and current - diffs[_i - 3] == 3:
        #     _variations[_i - 3] += 1

    print(_variations)
    return _variations



print(find_option(lines, {}))
# print(find_option(lines, []))

#   1111111111
#   2111111111
#   3111111111
#   1211111111
#   2211111111
#   3211111111
#   3311111111
#   1121111111

# combinations: Set[int] = set()
# options: List[int] = []
#
#
# def get_combination(iteration: int) -> Optional[int]:
#     invalid: bool = False
#     jolt: int = 0
#     seq: List[int] = []
#     for j in range(len(lines)):
#         m = ((iteration // pow(3, j)) % 3) + 1
#         if not jolt + m in lines:
#             invalid = True
#             break
#         else:
#             jolt = jolt + m
#             seq.append(m)
#
#         if jolt >= max(lines):
#             break
#
#     if not invalid:
#         _combo = int("".join([str(i - 1) for i in seq]), 3)
#         options.append(_combo)
#         return _combo
#     else:
#         return None
#

# for i in range(pow(3, len(lines))):
#
#     combination: int = get_combination(i)
#
#     if combination is not None:
#         combinations.add(combination)


# print(len(set(options)))
# for i in range(pow(3, len(lines))):
#     for j in range(1, len(lines)):
#         m = (i // j) % 3
#         print(m, end=" ")
#         # print("{} {} {}".format(i, j, m))

# print(i)
#
