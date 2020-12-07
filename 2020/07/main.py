import re
from typing import Optional, List, Set


class Bag(object):
    color: Optional[str] = None
    outer_bag = None
    bags: {} = {}

    def __init__(self, color: str = None, bags=None, outer_bag=None) -> None:
        super().__init__()

        if bags is None:
            bags = {}

        self.color = str(color)
        self.bags = bags
        self.outer_bag = outer_bag

    def __str__(self) -> str:
        return "{} ({}) {}".format(self.color, self.count(), [str(bag) for bag in self.bags])

    def contains(self, color: str) -> bool:
        for bag in self.bags:
            if bag.color == color:
                return True
            else:
                if bag.contains(color):
                    return True

        return False

    def count(self) -> int:
        _count: int = 0
        for k in self.bags:
            _count = _count + self.bags[k] + self.bags[k] * k.count()

        return _count

    def level(self) -> int:
        if self.outer_bag is None:
            return 0
        else:
            return self.outer_bag.level() + 1


bag_map: {str, Bag} = {}
bags: List[Bag] = []


def get_bag(color: str) -> Bag:
    bag = bag_map.get(str(color))

    if bag is None:
        bag = Bag(color)
        bag_map[str(color)] = bag

    return bag


with open('input.txt', 'r') as input:
    file = input.read()

    for line in file.splitlines():
        split = re.split("([\w\s]+)\s+bags\s+contain\s+(.*)", line)

        outer_bag = get_bag(split[1])

        if split[2].startswith('no other bags'):
            pass
        else:
            parts = split[2].split(',')
            for part in parts:
                sub_split = re.split("(\d+)\s+([\w\s]+)\s+bags?", part)
                bag = get_bag(sub_split[2])
                bag.outer_bag = outer_bag
                outer_bag.bags[bag] = int(sub_split[1])

        bags.append(outer_bag)

count: int = 0
for bag in bags:
    if bag.contains('shiny gold'):
        count = count + 1

print(count)

print(bag_map['shiny gold'].count())
