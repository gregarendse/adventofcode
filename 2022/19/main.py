#!/usr/bin/env python
from collections import deque
from dataclasses import dataclass
from typing import Dict, List, Optional, Set


@dataclass
class Robot(object):
    cost: Dict[str, int]
    produces: str


@dataclass
class Blueprint(object):
    id: int
    robots: List[Robot]


@dataclass
class State(object):
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geodes: int = 0

    # Start with one ore robot
    ore_robot: int = 1
    clay_robot: int = 0
    obsidian_robot: int = 0
    geode_robot: int = 0

    time_step: int = 0

    @staticmethod
    def iterate(state, maxes: Dict[str, float]):
        # Max to keep is how long it would take to get to max?
        # robot -> max[ore] / robot = turns to get to max -> ore * t_max
        # 1 ->  14 / 1 = 14 -> 14 * 14
        # 7 ->  14 / 7 = 2  ->  14 * 2
        # 14 -> 14 / 14 = 1 -> 14 * 1

        ore_robot = min(state.ore_robot, maxes['ore'])
        ore = min(
            state.ore + ore_robot,
            (maxes['ore'] // max(ore_robot, 1)) * maxes['ore']
        )

        clay_robot = min(state.clay_robot, maxes['clay'])
        clay = min(
            state.clay + state.clay_robot,
            (maxes['clay'] // max(ore_robot, 1)) * maxes['clay']
        )

        obsidian_robot = min(state.obsidian_robot, maxes['obsidian'])
        obsidian = min(
            state.obsidian + state.obsidian_robot,
            (maxes['obsidian'] // max(obsidian_robot, 1)) * maxes['obsidian']
        )

        return State(
            ore=ore,
            ore_robot=ore_robot,  # No need to keep more than max price of robots
            clay=clay,
            clay_robot=clay_robot,
            obsidian=obsidian,
            obsidian_robot=obsidian_robot,
            geodes=state.geodes + state.geode_robot,
            geode_robot=state.geode_robot,
            time_step=state.time_step + 1
        )

    def __hash__(self):
        h: int = hash(self.ore_robot) + hash(self.ore) \
                 + hash(self.clay_robot) + hash(self.clay) \
                 + hash(self.obsidian_robot) + hash(self.obsidian) \
                 + hash(self.geode_robot) + hash(self.geodes)
        return h

    @staticmethod
    def copy(state):
        return State(
            ore=state.ore,
            ore_robot=state.ore_robot,
            clay=state.clay,
            clay_robot=state.clay_robot,
            obsidian=state.obsidian,
            obsidian_robot=state.obsidian_robot,
            geodes=state.geodes,
            geode_robot=state.geode_robot,
            time_step=state.time_step
        )


def read_from_file(file: str) -> List[Blueprint]:
    blueprints: List[Blueprint] = []
    with open(file) as f:
        for line in f.readlines():
            parts: List[str] = line.strip().split(':')

            i: int = int(parts[0].strip().split()[1])
            robots: List[str] = parts[1].strip().split('.')

            r: List[Robot] = []
            for robot in robots:
                if len(robot.strip()) == 0:
                    continue
                p: List[str] = robot.strip().split(' robot costs ')
                produces: str = p[0].strip().split()[1]
                costs: Dict[str, int] = dict()

                for resource in p[1].split(' and '):
                    cost, name = resource.split()
                    costs[name] = int(cost)

                r.append(Robot(cost=costs, produces=produces))
            blueprints.append(Blueprint(i, r))

    return blueprints


def engine(blueprint: Blueprint, time_left: int = 24):
    resources: Dict[str, int] = {'ore': 0, 'clay': 0, 'obsidian': 0, 'geode': 0}
    robots: Dict[str, int] = {'ore': 1, 'clay': 0, 'obsidian': 0, 'geode': 0}
    distance: Dict[str, float] = {'ore': 99, 'clay': 99, 'obsidian': 99, 'geode': 99}
    maxes: Dict[str, float] = {'ore': 0, 'clay': 0, 'obsidian': 0, 'geode': 0}

    building: Optional[str] = None

    for robot in blueprint.robots:
        for k, v in robot.cost.items():
            maxes[k] = max(maxes[k], v)

    queue = deque([State()])
    seen: Set[State] = set()
    best: int = 0
    geode_robots: int = 0

    while queue:
        state: State = queue.popleft()
        best = max(best, state.geodes)

        if state.time_step >= time_left:
            continue

        # if state.geode_robot < geode_robots:
        #     continue
        # geode_robots = max(geode_robots, state.geode_robot)

        if state in seen:
            continue
        seen.add(state)

        queue.append(
            State.copy(
                State.iterate(state, maxes)
            )
        )

        for robot in blueprint.robots:
            afford: bool = True

            for k, v in robot.cost.items():
                if 'ore' == k:
                    afford &= state.ore >= v
                elif 'clay' == k:
                    afford &= state.clay >= v
                elif 'obsidian' == k:
                    afford &= state.obsidian >= v
                elif 'geode' == k:
                    afford &= state.geodes >= v

            if afford:
                new_state = State.copy(
                    State.iterate(state, maxes)
                )

                for k, v in robot.cost.items():
                    if 'ore' == k:
                        new_state.ore -= v
                    elif 'clay' == k:
                        new_state.clay -= v
                    elif 'obsidian' == k:
                        new_state.obsidian -= v

                if 'ore' == robot.produces:
                    if new_state.ore_robot < maxes['ore']:
                        new_state.ore_robot += 1
                    else:
                        continue
                elif 'clay' == robot.produces:
                    if new_state.clay_robot < maxes['clay']:
                        new_state.clay_robot += 1
                    else:
                        continue
                elif 'obsidian' == robot.produces:
                    if new_state.obsidian_robot < maxes['obsidian']:
                        new_state.obsidian_robot += 1
                    else:
                        continue
                elif 'geode' == robot.produces:
                    new_state.geode_robot += 1

                    queue = deque(
                        filter(
                            lambda n: n.geode_robot >= new_state.geode_robot and n.time_step >= new_state.time_step,
                            queue
                        )
                    )

                else:
                    print(robot)
                    raise NameError('Unknown mineral')
                queue.append(new_state)
    print(best)
    return best

    # for i in range(24):
    #
    #     if building is not None:
    #         robots[building] += 1
    #         building = None
    #
    #     for robot in reversed(blueprint.robots):
    #
    #         total: int = -1
    #
    #         for resource, cost in robot.cost.items():
    #             if robots[resource] > 0:
    #                 total = max(ceil((cost - resources[resource]) / robots[resource]), total)
    #             else:
    #                 total = 99
    #
    #         distance[robot.produces] = total
    #
    #     for robot in reversed(blueprint.robots):
    #         if distance[robot.produces] <= min(robot.cost.values()):
    #
    #             afford: bool = True
    #
    #             for resource, cost in robot.cost.items():
    #                 if resources[resource] < cost:
    #                     afford = False
    #                     break
    #             if not afford:
    #                 break
    #
    #             building = robot.produces
    #
    #             for resource, cost in robot.cost.items():
    #                 resources[resource] -= cost
    #
    #             break
    #
    #     for resource, value in robots.items():
    #         resources[resource] += value
    #
    #     # print("{} -> {}".format(i, distance))
    #
    # return resources


def part_one(file: str) -> int:
    blueprints: List[Blueprint] = read_from_file(file)

    quality_sum: int = 0

    for blueprint in blueprints:
        # assert engine(blueprint, time_left=19) == 1
        # assert engine(blueprint, time_left=22) == 5
        resources = engine(blueprint)
        # assert resources == 9

        quality_sum += (blueprint.id * resources)

    return quality_sum


def part_two(file: str) -> int:
    content: str = read_from_file(file)

    return 0


def main():
    p1_example: int = part_one('example.txt')
    assert p1_example == 33
    p1: int = part_one('input.txt')
    print("Part One: {}".format(p1))

    p2_example: int = part_two('example.txt')
    assert p2_example == 0
    p2: int = part_two('input.txt')
    print("Part Two: {}".format(p2))


if __name__ == '__main__':
    main()
