#!/use/bin/env python
from sys import argv
from typing import List, Tuple


def read_file(file: str) -> List[List[int]]:
    with open(file, 'r') as f:
        trees: List[List[int]] = []
        for line in f.readlines():
            line = line.strip()
            row: List[int] = []
            for l in line:
                row.append(int(l))
            trees.append(row)
        return trees


def print_trees(trees: List[List[int]]) -> None:
    for column in trees:
        for row in column:
            print(row, end="")
        print()


def part_one(file: str) -> int:
    trees: List[List[int]] = read_file(file)

    visible_trees: List[Tuple[int, int]] = []
    for i in range(1, len(trees) - 1):
        for j in range(1, len(trees[i]) - 1):

            visible: bool = True
            for x in range(i):
                if trees[i][j] <= trees[x][j]:
                    visible = False
                    break

            if visible:
                visible_trees.append(tuple((i, j)))
                continue

            visible = True
            for x in range(i + 1, len(trees)):
                if trees[i][j] <= trees[x][j]:
                    visible = False
                    break

            if visible:
                visible_trees.append(tuple((i, j)))
                continue

            visible = True
            for y in range(j):
                if trees[i][j] <= trees[i][y]:
                    visible = False
                    break

            if visible:
                visible_trees.append(tuple((i, j)))
                continue

            visible = True
            for y in range(j + 1, len((trees[i]))):
                if trees[i][j] <= trees[i][y]:
                    visible = False
                    break

            if visible:
                visible_trees.append(tuple((i, j)))
                continue

    print(visible_trees)
    return (len(visible_trees) + (len(trees) + len(trees[0]) - 2) * 2)


def part_two(file: str) -> int:
    trees: List[List[int]] = read_file(file)

    visible_trees: List[Tuple[int, int]] = []
    scores: List[int] = []
    for i in range(1, len(trees) - 1):
        for j in range(1, len(trees[i]) - 1):

            up: int = 0
            for u in range(i - 1, 0, -1):
                if trees[i][j] <= trees[u][j]:
                    up = u
                    break
            if up != 0:
                up = i - up
            else:
                up = i

            down: int = 0
            for d in range(i + 1, len(trees)):
                if trees[i][j] <= trees[d][j]:
                    down = d
                    break
            if down != 0:
                down = down - i
            else:
                down = len(trees) - i - 1

            left: int = 0
            for l in range(j - 1, 0, -1):
                if trees[i][j] <= trees[i][l]:
                    left = l
                    break
            if left != 0:
                left = j - left
            else:
                left = j

            right: int = 0
            for r in range(j + 1, len((trees[i]))):
                if trees[i][j] <= trees[i][r]:
                    right = r
                    break
            if right != 0:
                right = right - j
            else:
                right = len(trees[i]) - j - 1

            score: int = left * right * up * down
            print("{} * {} * {} * {}".format(
                up,
                left,
                down,
                right
            ))
            print("{} {},{} : {}".format(trees[i][j], i, j, score))
            scores.append(score)

    return max(scores)


def main():
    print("Part One: {}".format(part_one(argv[1])))
    print("Part Two: {}".format(part_two(argv[1])))


if __name__ == '__main__':
    main()
