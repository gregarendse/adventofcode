#!/usr/bin/env python3

def print_grid():
    for line in grid:
        for item in line:
            print(item, end='')
        print()


def count_trees(grid: [], x_inc: int = 1, y_inc: int = 1) -> int:
    x: int = 0
    y: int = 0
    count: int = 0

    while y < len(grid):
        if grid[y][x % len(grid[y])] == '#':
            count = count + 1

        y = y + y_inc
        x = x + x_inc

    return count


grid = []

with open('input.txt', 'r') as file:

    lines = file.read().splitlines()

    for line in lines:
        grid.append(list(line))


slope_tree_count = [
    count_trees(grid=grid, x_inc=1, y_inc=1),
    count_trees(grid=grid, x_inc=3, y_inc=1),
    count_trees(grid=grid, x_inc=5, y_inc=1),
    count_trees(grid=grid, x_inc=7, y_inc=1),
    count_trees(grid=grid, x_inc=1, y_inc=2),
]

ans = 1
for slope in slope_tree_count:
    ans = slope * ans
print(ans)
