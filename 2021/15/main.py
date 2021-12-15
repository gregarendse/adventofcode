#!/bin/python

from dataclasses import dataclass
from typing import Deque, Dict, List, Set
from collections import deque
import statistics
import copy
import sys
import heapq


@dataclass
class Node(object):
    x: int
    y: int
    distance: int = 999999999
    previouse = None
    neighbours = []
    visited: bool = False

    def __lt__(self, o: object) -> bool:
        return self.distance < o.distance

    def __eq__(self, __o: object) -> bool:
        return self.x == __o.x and self.y == __o.y

    def __hash__(self) -> int:
        return hash(self.x) + hash(self.y)


def print_risk_level_map(risk_level_map: List[List[int]]) -> None:
    for line in risk_level_map:
        for l in line:
            print(l, end='')
        print()


def print_path(node: Node, risk_level_map) -> None:
    map: List[List[int]] = [
        [0 for i in range(10)] for j in range(10)
    ]

    print("".join(['-' for i in range(10)]))
    print(node.distance)

    while node is not None:
        map[node.y][node.x] = risk_level_map[node.y][node.x]
        node = node.previouse

    print_risk_level_map(map)


def part_one(risk_map: List[List[int]]) -> int:

    unvisited_nodes: Deque[Node] = deque()
    node_map: List[List[Node]] = []

    for y in range(len(risk_map)):
        row: List[Node] = []
        for x in range(len(risk_map[y])):
            node: Node = Node(x=x, y=y)
            unvisited_nodes.append(node)
            row.append(node)
        node_map.append(row)

    for row in node_map:
        for node in row:
            node.neighbours = []
            if node.x + 1 < len(risk_map):
                node.neighbours.append(node_map[node.y][node.x + 1])
            if node.x - 1 > 0:
                node.neighbours.append(node_map[node.y][node.x - 1])
            if node.y + 1 < len(risk_map):
                node.neighbours.append(node_map[node.y + 1][node.x])
            if node.y - 1 > 0:
                node.neighbours.append(node_map[node.y - 1][node.x])

    node_map[0][0].distance = 0

    paths: List[Node] = [node_map[0][0]]

    while True:

        min_dist_node: Node = heapq.heappop(paths)

        if min_dist_node.visited:
            continue
        min_dist_node.visited = True

        if min_dist_node == Node(x=len(risk_map) - 1, y=len(risk_map[-1]) - 1):
            break

        for n in min_dist_node.neighbours:
            if not n.visited:
                distance: int = min_dist_node.distance + risk_map[n.y][n.x]
                if n.distance > distance:
                    n.distance = distance
                    n.previouse = min_dist_node
                heapq.heappush(paths, n)

    return min_dist_node.distance


def increase_map(risk_level_map: List[List[int]]) -> List[List[int]]:
    size: int = len(risk_level_map) * 5
    mod: int = len(risk_level_map)
    return [
        [
            (risk_level_map[i % mod][j % mod] +
             (1 * int(i / mod)) + (1 * int(j / mod)) - 1) % 9 + 1
            for j in range(size)
        ]
        for i in range(size)
    ]


def part_two(risk_level_map: List[List[int]]) -> int:
    map = increase_map(risk_level_map)
    return part_one(map)


with open('2021/15/input.txt', 'r') as file:
    risk_level_map: List[List[int]] = []
    for line in file.readlines():
        risk_level_map.append([int(x) for x in line.strip()])

print(part_one(risk_level_map))
print(part_two(risk_level_map))
