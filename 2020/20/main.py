import copy
from typing import List, Set, Dict, Optional

from math import sqrt


class Tile(object):

    def __hash__(self) -> int:
        return self.id

    def __eq__(self, o: object) -> bool:
        return self.id.__eq__(o)

    def __init__(self, id: int, raw_image: List[str]) -> None:
        super().__init__()
        self.id = int(id)
        self.raw_image = raw_image

        self.image = []

        for line in raw_image:
            image_line: List[str] = []
            for i in enumerate(line):
                image_line.append(str(i))
            self.image.append(image_line)

        self.top = self.raw_image[0]
        # self.top_invert = self.__inverse__(self.top)
        # self.top_value = self.__get_value__(self.top)

        self.bottom = self.raw_image[-1]
        # self.bottom_value = self.__get_value__(self.bottom)

        left: List[str] = []
        right: List[str] = []
        for line in raw_image:
            left.append(line[0])
            right.append(line[-1])
        self.left = "".join(left)
        self.right = "".join(right)

        # self.left_value = self.__get_value__(self.left)
        # self.right_value = self.__get_value__(self.right)

    @staticmethod
    def __inverse__(input: str) -> str:
        image_ = [i for i in input]
        image_.reverse()
        return ''.join(image_)

    @staticmethod
    def __get_value__(input: str):
        return int(input.replace('#', '1').replace('.', '0'), 2)

    @staticmethod
    def parse(input: str):
        lines: List[str] = input.splitlines()

        return Tile(int(lines[0].replace(':', '').split()[1]), lines[1:])

    def get_side_values(self) -> List[int]:
        return [self.__get_value__(self.top), self.__get_value__(self.right), self.__get_value__(self.bottom),
                self.__get_value__(self.left)]

    def vertical_flip(self):
        top = self.top
        self.top = self.bottom
        self.bottom = top

        self.left = self.__inverse__(self.left)
        self.right = self.__inverse__(self.right)

    def horizontal_flip(self):
        left = self.left
        self.left = self.right
        self.right = left

        self.top = self.__inverse__(self.top)
        self.bottom = self.__inverse__(self.bottom)

    def __str__(self) -> str:
        return "Tile {}".format(self.id)

    def rotate(self):
        top = self.top
        self.top = self.left
        self.left = self.bottom
        self.bottom = self.right
        self.right = top


def part_one(tiles: List[Tile]) -> int:
    tile_match_map = get_edge_count_map(tiles)
    mult: int = 1
    for k, v in tile_match_map.items():
        if v == 2:
            mult *= k.id

    return mult


def get_edge_count_map(tiles: List[Tile]) -> Dict[Tile, int]:
    __tiles = copy.deepcopy(tiles)
    tile_match_map: Dict[Tile, int] = dict.fromkeys(__tiles, 0)
    for tile in __tiles:
        tile_sides: Set[int] = set(tile.get_side_values())
        for other_tile in __tiles:
            if tile == other_tile:
                continue
            other_sides: Set[int] = set(other_tile.get_side_values())
            if len(tile_sides & other_sides) > 0:
                tile_match_map[tile] += 1

            other_tile.horizontal_flip()
            other_tile.vertical_flip()

            other_sides: Set[int] = set(other_tile.get_side_values())
            if len(tile_sides & other_sides) > 0:
                tile_match_map[tile] += 1
    return tile_match_map


def get_required_edge_count(i: int, j: int, size: int) -> int:
    count: int = 2

    if i != 0 and i != size - 1:
        count += 1

    if j != 0 and j != size - 1:
        count += 1

    return count


def get_tile(y: int, x: int, grid: List[List[Optional[Tile]]]) -> Optional[Tile]:
    if 0 <= y < len(grid) and 0 <= x < len(grid[y]):
        return grid[y][x]
    return None


def match(tile: Tile, y: int, x: int, grid: List[List[Optional[Tile]]], edge_set: Set[int]) -> bool:
    top_tile: Optional[Tile] = get_tile(y - 1, x, grid)
    right_tile: Optional[Tile] = get_tile(y, x + 1, grid)
    bottom_tile: Optional[Tile] = get_tile(y + 1, x, grid)
    left_tile: Optional[Tile] = get_tile(y, x - 1, grid)

    _match: bool = is_tile_match(bottom_tile, edge_set, grid, left_tile, right_tile, tile, top_tile, x, y)

    _rotate_count: int = 0
    while not _match:

        if _rotate_count == 4:
            tile.vertical_flip()
        elif _rotate_count == 9:
            tile.horizontal_flip()
        elif _rotate_count > 13:
            return False
        else:
            tile.rotate()

        _rotate_count += 1
        _match = is_tile_match(bottom_tile, edge_set, grid, left_tile, right_tile, tile, top_tile, x, y)

    return _match


def is_tile_match(bottom_tile, edge_set, grid, left_tile, right_tile, tile, top_tile, x, y):
    print("{} {}".format(x,y))
    print(tile.top)
    top: bool = (top_tile is None or top_tile.bottom == tile.top)
    right: bool = (right_tile is None or right_tile.left == tile.right)
    bottom: bool = (bottom_tile is None or bottom_tile.top == tile.bottom)
    left: bool = (left_tile is None or left_tile.right == tile.left)
    top_edge: bool = ((0 > y - 1) or Tile.__get_value__(tile.top) in edge_set)
    right_edge: bool = ((0 > x - 1) or Tile.__get_value__(tile.right) in edge_set)
    bottom_edge: bool = ((y + 1 >= len(grid)) or Tile.__get_value__(tile.bottom) in edge_set)
    left_edge: bool = ((x + 1 >= len(grid)) or Tile.__get_value__(tile.left) in edge_set)
    return top and right and bottom and left and top_edge and right_edge and bottom_edge and left_edge


def print_id_grid(grid: List[List[Optional[Tile]]]):
    for row in grid:
        for item in row:
            if item is not None:
                print(str(item.id), end=" ")
            else:
                print(str(item), end=" ")
        print()


def part_two(tiles: List[Tile]) -> int:
    tile_match_map: Dict[Tile, int] = get_edge_count_map(tiles)
    edge_set: Set[int] = set()

    for tile in copy.deepcopy(tiles):
        edge_set |= set(tile.get_side_values())

        tile.vertical_flip()
        tile.horizontal_flip()

        edge_set |= set(tile.get_side_values())

    for k, v in tile_match_map.items():
        print("{} {}".format(k, v))

    grid_size: int = int(sqrt(len(tiles)))
    grid: List[List[Optional[Tile]]] = [[None for _ in range(grid_size)] for _ in range(grid_size)]

    for i in range(grid_size):
        for j in range(grid_size):
            match_count: int = get_required_edge_count(i, j, grid_size)

            for tile, count in tile_match_map.items():
                if count == match_count and match(tile, i, j, grid, edge_set):
                    grid[i][j] = tile
                    tile_match_map.pop(tile)
                    break

            if grid[i][j] is None:
                print_id_grid(grid)
                raise Exception

    print_id_grid(grid)
    return 0


def fit_tile(edge_set, grid_size, i, j, tile) -> bool:
    rotate_count: int = 0
    while (
            (i == 0 and tile.right not in edge_set)
            or (j == grid_size - 1 and tile.left not in edge_set)
            or (j == 0 and tile.bottom not in edge_set)
            or (j == grid_size - 1 and tile.top not in edge_set)
    ):
        rotate_count += 1
        if rotate_count == 4:
            tile.horizontal_flip()
        elif rotate_count == 8:
            tile.vertical_flip()
        elif rotate_count > 8:
            raise Exception
        else:
            tile.rotate()


with open('example.txt', 'r') as file:
    raw_tiles: List[str] = file.read().split('\n\n')

    tiles: List[Tile] = [Tile.parse(item) for item in raw_tiles]

    print(part_one(tiles))
    print(part_two(tiles))
