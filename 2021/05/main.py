#!/bin/python

from typing import Dict, List, Set
from dataclasses import dataclass
import math 

diagram = []

@dataclass
class point:
    x: int
    y: int

    def __hash__(self) -> int:
        return hash(x) + hash(y)

def find_points(start: point, end: point) -> List[point]:
    points: Set[point] = set()

    x_points: List[int] = []
    y_points: List[int] = []

    if start.x == end.x:
        for i in range(abs(end.y - start.y) + 1):
            y_points.append(min(end.y, start.y) + i)
            x_points.append(start.x)
    
    elif start.y == end.y:
        for i in range(abs(end.x - start.x) + 1):
            x_points.append(min(end.x, start.x) + i)
            y_points.append(start.y)
    
    else:
        for i in range(abs(end.x - start.x) + 1):
            if end.x > start.x:
                x_points.append(start.x + i)
            else:
                x_points.append(start.x - i)

            if end.y > start.y:
                y_points.append(start.y + i)
            else:
                y_points.append(start.y - i)

 

    # for i in range(abs(end.x - start.x) + 1):
    #     if end.x > start.x:
    #         x_points.append(start.x + i)
    #     else:
    #         x_points.append(start.x - i)

    #     y_points.append(start.y)

    # for i in range(abs(end.y - start.y) + 1):
    #     x_points.append(start.x)

    #     if end.y > start.y:
    #         y_points.append(start.y + i)
    #     else:
    #         y_points.append(start.y - i)

    for i in range(len(x_points)):
        p=point(x=(x_points[i]), y=y_points[i])
        # print(p)
        points.add(p)

    return points


with open('2021/05/input.txt', 'r') as file:

    diagram: List[List[int]] = [[0 for i in range(1000)] for i in range(1000)]

    for line in file.readlines():
        # print(line)
        start, end = line.split(' -> ')

        x, y = start.split(',')
        start_point = point(int(x), int(y))

        x, y = end.split(',')
        end_point = point(int(x), int(y))

        points: List[point] = find_points(start_point, end_point)

        for p in points:
            # print(p)
            diagram[p.y][p.x]+=1
        
        # print(['-' for i in range(10)])
        # for row in diagram:
        #     for item in row:
        #         if item == 0:
        #             print('.', end=' ')
        #         else:
        #             print(item, end=' ')
        #     print()

    count: int = 0
    for row in diagram:
            for item in row:
                if item > 1:
                    count+=1
    print(count)


