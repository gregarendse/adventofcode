from typing import List, Dict, Set


class Range(object):

    def __init__(self, min: int, max: int) -> None:
        super().__init__()
        self.min = min
        self.max = max

    def __str__(self) -> str:
        return "{}-{}".format(str(self.min), str(self.max))


class Rule(object):

    def __init__(self, line: str) -> None:
        super().__init__()

        [self.name, rules] = line.split(":")

        self.ranges = []
        for rule in rules.split('or'):
            [min, max] = rule.split('-')
            self.ranges.append(Range(int(min.strip()), int(max.strip())))

    def validate(self, values: List[int]) -> bool:
        valid: bool = False
        for value in values:
            valid |= self.is_valid(value)
        return valid

    def is_valid(self, value: int):
        valid: bool = False
        for range in self.ranges:
            valid |= range.min <= value <= range.max
        return valid

    def __str__(self) -> str:
        return "{}: {}".format(self.name, [str(range) for range in self.ranges])


def any_valid(value, rules: List[Rule]) -> bool:
    valid: bool = False

    for rule in rules:
        valid |= rule.is_valid(value)

    return valid


def all_valid(values, rules: List[Rule]) -> bool:
    valid: bool = True
    for value in values:
        valid &= any_valid(value, rules)
    return valid


def part_one(parts: List[str]) -> int:
    nearby_tickets: List[List[int]] = []

    rules: List[Rule] = get_rules(parts)

    invalid_numbers: List[int] = []
    for ticket in parts[2].splitlines()[1:]:
        nearby_tickets.append([int(x) for x in ticket.split(',')])
        for value in [int(x) for x in ticket.split(',')]:
            if not any_valid(value, rules):
                invalid_numbers.append(value)

    return sum(invalid_numbers)


def get_rules(parts) -> List[Rule]:
    rules: List[Rule] = []
    for rule in parts[0].splitlines():
        rules.append(Rule(rule))
    return rules


def part_two(parts: List[str]) -> int:
    your_ticket: List[int] = [int(x) for x in parts[1].splitlines()[1].split(',')]
    rules: List[Rule] = get_rules(parts)
    nearby_tickets: List[List[int]] = []

    for ticket in parts[2].splitlines()[1:]:
        if all_valid([int(x) for x in ticket.split(',')], rules):
            nearby_tickets.append([int(x) for x in ticket.split(',')])

    rule_index_map: Dict[Rule, Set[int]] = dict()
    for rule in rules:
        final_options: Set[int] = None
        for ticket in nearby_tickets:
            options: Set[int] = set()
            for i, value in enumerate(ticket):
                if rule.is_valid(value):
                    options.add(i)

            if final_options is None:
                final_options = options
            else:
                final_options &= options

        rule_index_map[rule] = final_options

    while max([len(value) for value in rule_index_map.values()]) != 1:
        for value in rule_index_map.values():
            if len(value) == 1:
                for other_value in rule_index_map.values():
                    if other_value != value:
                        other_value -= value

    departures: List[Rule] = [rule for rule in rule_index_map.keys() if rule.name.startswith("departure")]
    mult: int = 1
    for departure in departures:
        mult *= your_ticket[rule_index_map.get(departure).pop()]
    return mult


with open('input.txt', 'r') as file:
    parts = file.read().split('\n\n')
    print(part_one(parts))
    print(part_two(parts))
