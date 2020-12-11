import copy

seat_map: [[str]] = []
with open('input.txt', 'r') as file:
    for line in file.read().splitlines():
        items = []
        for item in line:
            items.append(item)
        seat_map.append(items)


def find_seat(x: int, y: int, x_inc: int, y_inc: int, seats: [[str]]) -> int:
    x_pos: int = x + x_inc
    y_pos: int = y + y_inc

    if not 0 <= x_pos < len(seats) or not 0 <= y_pos < len(seats[x_pos]):
        return 0

    seat = seats[x_pos][y_pos]
    if seat == '#':
        return 1
    if seat == 'L':
        return 0

    return find_seat(x_pos, y_pos, x_inc, y_inc, seats)


def check_visable_seats(x_pos: int, y_pos: int, seats: [[int]]) -> int:
    _occupied_count: int = 0
    _occupied_count += find_seat(x_pos, y_pos, -1, 0, seats)
    _occupied_count += find_seat(x_pos, y_pos, -1, -1, seats)
    _occupied_count += find_seat(x_pos, y_pos, 0, -1, seats)
    _occupied_count += find_seat(x_pos, y_pos, +1, -1, seats)
    _occupied_count += find_seat(x_pos, y_pos, +1, 0, seats)
    _occupied_count += find_seat(x_pos, y_pos, +1, +1, seats)
    _occupied_count += find_seat(x_pos, y_pos, 0, +1, seats)
    _occupied_count += find_seat(x_pos, y_pos, -1, +1, seats)
    return _occupied_count


def check_surrounding_seats(x_pos: int, y_pos: int, seats: [[str]]) -> int:
    _occupied_count: int = 0
    x_minus = x_pos - 1 >= 0
    y_minus = y_pos - 1 >= 0
    x_plus = x_pos + 1 < len(seats)
    y_plus = y_pos + 1 < len(seats[x_pos])

    if x_minus and seats[x_pos - 1][y_pos] == '#':
        _occupied_count += 1
    if x_plus and seats[x_pos + 1][y_pos] == '#':
        _occupied_count += 1
    if y_minus and seats[x_pos][y_pos - 1] == '#':
        _occupied_count += 1
    if y_plus and seats[x_pos][y_pos + 1] == '#':
        _occupied_count += 1
    if x_minus and y_minus and seats[x_pos - 1][y_pos - 1] == '#':
        _occupied_count += 1
    if x_minus and y_plus and seats[x_pos - 1][y_pos + 1] == '#':
        _occupied_count += 1
    if x_plus and y_plus and seats[x_pos + 1][y_pos + 1] == '#':
        _occupied_count += 1
    if x_plus and y_minus and seats[x_pos + 1][y_pos - 1] == '#':
        _occupied_count += 1

    return _occupied_count


def print_seat_map(seats: [[str]]):
    print("".join(['-' for _ in seats]))
    for row in seats:
        for seat in row:
            print(seat, end="")
        print()


def count_seats(seats: [[]]) -> int:
    _count: int = 0
    for row in seats:
        for seat in row:
            if seat == '#':
                _count += 1
    return _count


def simulate_surrounding(seat_map: [[str]]) -> [[str]]:
    seat_map = copy.deepcopy(seat_map)
    change: bool = True
    while change:

        change = False
        original = copy.deepcopy(seat_map)

        for x in range(len(seat_map)):
            for y in range(len(seat_map[x])):
                occupied_count: int = check_surrounding_seats(x, y, original)
                prev: str = original[x][y]

                if occupied_count == 0 and prev == 'L':
                    seat_map[x][y] = '#'
                    change = True
                elif occupied_count >= 4 and prev == '#':
                    seat_map[x][y] = 'L'
                    change = True

    return seat_map


def simulate_visable(seat_map: [[str]]) -> [[str]]:
    seat_map = copy.deepcopy(seat_map)
    change: bool = True
    while change:

        change = False
        original = copy.deepcopy(seat_map)

        for x in range(len(seat_map)):
            for y in range(len(seat_map[x])):
                occupied_count: int = check_visable_seats(x, y, original)
                prev: str = original[x][y]

                if occupied_count == 0 and prev == 'L':
                    seat_map[x][y] = '#'
                    change = True
                elif occupied_count >= 5 and prev == '#':
                    seat_map[x][y] = 'L'
                    change = True

    return seat_map


print(count_seats(simulate_surrounding(seat_map)))
print(count_seats(simulate_visable(seat_map)))
