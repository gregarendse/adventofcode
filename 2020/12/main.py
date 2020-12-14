from typing import List

import math

directions: {str, int} = {
    'N': [0, 1],
    'E': [1, 0],
    'S': [0, -1],
    'W': [-1, 0]
}


class Position(object):

    def __init__(self, x: float = 0, y: float = 0) -> None:
        super().__init__()
        self.x = round(x)
        self.y = round(y)

    def move(self, x: float, y: float):
        self.x += x
        self.y += y

    def way_point(self, way_point, magnitude: int):
        self.x += way_point.x * magnitude
        self.y += way_point.y * magnitude

    def manhattan_distance(self) -> float:
        return abs(self.x) + abs(self.y)

    def rotate(self, angle: float):
        x = (self.x * math.cos(angle)) - (self.y * math.sin(angle))
        y = (self.x * math.sin(angle)) + (self.y * math.cos(angle))
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return "{}, {}".format(self.x, self.y)


def part_one(lines: List[str]) -> int:
    direction: int = 90
    position: Position = Position()

    for line in lines:
        instruction: str = str(line[0])
        magnitude: int = int(line[1:])

        if instruction == 'F':
            radians = math.radians(direction)
            position.move(x=math.sin(radians) * magnitude, y=math.cos(radians) * magnitude)
        elif instruction == 'R':
            direction += magnitude
        elif instruction == 'L':
            direction -= magnitude
        elif instruction in directions.keys():
            position.move(x=directions[instruction][0] * magnitude, y=directions[instruction][1] * magnitude)

    return round(position.manhattan_distance())


def part_two(lines: List[str]) -> int:
    way_point: Position = Position(x=10, y=1)
    position: Position = Position()

    for line in lines:
        instruction: str = str(line[0])
        magnitude: int = int(line[1:])

        if instruction == 'F':
            position.way_point(way_point, magnitude)
        elif instruction == 'R':
            way_point.rotate(math.radians(magnitude) * -1)
        elif instruction == 'L':
            way_point.rotate(math.radians(magnitude))
        elif instruction in directions.keys():
            way_point.move(x=directions[instruction][0] * magnitude, y=directions[instruction][1] * magnitude)
        else:
            raise Exception

    return round(position.manhattan_distance())


with open('input.txt', 'r') as file:
    lines: List[str] = file.readlines()
    print(part_one(lines))
    print(part_two(lines))
