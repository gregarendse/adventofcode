#!/use/bin/env python

from dataclasses import dataclass
from sys import argv
from typing import List


@dataclass
class Point(object):
    x: int = 0
    y: int = 0
    d: int = 0


def insert(point: Point, value: str, map: List[List[str]]):
    while len(map) <= point.y:
        map.append([])
    while len(map[point.y]) <= point.x:
        map[point.y].append(".")

    map[point.y][point.x] = value


def read_from_file(file: str) -> List[Point]:
    map: List[List[str]] = []

    with open(file) as f:
        sensors: List[Point] = []
        beacons: List[Point] = []
        for line in f.readlines():
            # 0      1  2   3       4       5      6  7 8     9
            # Sensor at x=2, y=18: closest beacon is at x=-2, y=15
            parts = line.split()
            sensor = Point(x=int(parts[2].split('=')[1][:-1]), y=int(parts[3].split('=')[1][:-1]))
            # insert(sensor, 'S', map)
            sensors.append(sensor)
            beacon = Point(x=int(parts[8].split('=')[1][:-1]), y=int(parts[9].split('=')[1]))
            sensor.d = abs(sensor.x - beacon.x) + abs(sensor.y - beacon.y)
            beacon.d = sensor.d
            # insert(beacon, 'B', map)
            beacons.append(beacon)

    return sensors, beacons


def display(m: List[List[str]]) -> None:
    for i in m:
        for j in i:
            print(j, end=' ')
        print()


def part_one(file: str) -> int:
    # line: int = 10
    line: int = 2000000
    sensors, beacons = read_from_file(file)
    count: int = 0

    valid_beacons: List[Point] = []
    valid_sensors: List[Point] = []
    on_line_beacons: List[int] = []
    for i in range(len(sensors)):
        beacon = beacons[i]
        sensor = sensors[i]

        # Check if sensor - beacon distance is close to the line
        d = sensor.d - abs(sensor.y - line)
        if d >= 0:
            valid_beacons.append(beacon)
            valid_sensors.append(sensor)
        if beacon.y == line:
            on_line_beacons.append(beacon.x)

    points = []
    on_line = []

    for j in range(len(valid_sensors)):
        sensor = valid_sensors[j]
        beacon = valid_beacons[j]

        d = sensor.d - abs(sensor.y - line)
        hits = range(sensor.x - d, sensor.x + d + 1)
        hits_s = set(hits)

        points.append(hits_s)

    print(len(set([]).union(*points) - set(on_line_beacons)))
    # print()
    print(count)

    pass


def part_two(file: str) -> int:
    pass


def main():
    print("Part One: {}".format(part_one(argv[1])))
    print("Part Two: {}".format(part_two(argv[1])))


if __name__ == '__main__':
    main()
