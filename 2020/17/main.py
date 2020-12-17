from typing import List


def part_one(initial_state: List[str]) -> int:
    state: List[List[List[List[str]]]] = initialize(initial_state)

    for _ in range(6):
        state = iteration(state)

    return count(state, '#')


def count(grid: List[List[List[List[str]]]], state: str) -> int:
    state_count: int = 0

    for w in grid:
        for z in w:
            for y in z:
                for x in y:
                    if x == state:
                        state_count += 1

    return state_count


def get_state(grid: List[List[List[List[str]]]], z: int, y: int, x: int, w: int) -> str:
    if 0 <= w < len(grid) and 0 <= z < len(grid[w]) and 0 <= y < len(grid[w][z]) and 0 <= x < len(grid[w][z][y]):
        return grid[w][z][y][x]
    return '.'


def iteration(state: List[List[List[List[str]]]]) -> List[List[List[List[str]]]]:
    current_state: List[List[List[List[str]]]] = []

    for w in range(-1, len(state) + 1):
        z_row: List[List[List[str]]] = []
        for z in range(-1, len(state[0]) + 1):
            y_row: List[List[str]] = []
            for y in range(-1, len(state[0][0]) + 1):
                x_row: List[str] = []
                for x in range(-1, len(state[0][0][0]) + 1):
                    neighbours = count_neighbours(z, y, x, w, state)
                    if get_state(state, z, y, x, w) == '#':
                        if neighbours in [2, 3]:
                            x_row.append('#')
                        else:
                            x_row.append('.')
                    elif get_state(state, z, y, x, w) == '.':
                        if neighbours == 3:
                            x_row.append('#')
                        else:
                            x_row.append('.')
                    else:
                        x_row.append('.')
                y_row.append(x_row)
            z_row.append(y_row)
        current_state.append(z_row)

    return current_state


def count_neighbours(z: int, y: int, x: int, w: int, state: List[List[List[List[str]]]]) -> int:
    _count: int = 0

    for _w in range(w - 1, w + 2):
        for _z in range(z - 1, z + 2):
            for _y in range(y - 1, y + 2):
                for _x in range(x - 1, x + 2):

                    if w == _w and z == _z and x == _x and y == _y:
                        continue

                    if get_state(state, _z, _y, _x, _w) == '#':
                        _count += 1
    return _count


def initialize(initial_state: List[str]) -> List[List[List[List[str]]]]:
    state: List[List[List[List[str]]]] = []
    z_row: List[List[List[str]]] = []
    for z in range(1):
        y_row: List[List[str]] = []
        for y in range(len(initial_state)):
            x_row: List[str] = []
            y_initial_state = initial_state[y].strip()[:]
            for x in range(len(initial_state)):
                x_row.append(y_initial_state[x])
            y_row.append(x_row)
        z_row.append(y_row)
    state.append(z_row)
    return state


def print_state(state: List[List[List[List[str]]]]):
    for j, w in enumerate(state):
        for i, z in enumerate(w):
            print("z={}, w={}".format(i - len(w) // 2, j - len(state) // 2))
            for y in z:
                for x in y:
                    print(x, end="")
                print("")
            print("")


with open('input.txt', 'r') as file:
    lines = file.readlines()
    print(
        part_one(lines)
    )
