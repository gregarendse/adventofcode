import copy
from typing import List, Optional


class Node(object):

    def __init__(self, value, next=None) -> None:
        super().__init__()
        self.value = value
        self.next = next

    def __eq__(self, o: object) -> bool:
        return hasattr(o, 'value') and self.value == o.value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value


class LinkedList(object):

    def __init__(self, nodes: [] = None, head=None, size=None) -> None:
        super().__init__()
        self.head = head

        if size is not None:
            node: Optional[Node] = None
            for _ in range(size + 1):
                node = self.head.next
            node.next = self.head

        if nodes is not None:
            node: Node = Node(value=nodes.pop(0))
            self.head = node
            for item in nodes:
                node.next = Node(value=item)
                node = node.next
            node.next = self.head

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return "[" + ",".join([str(node.value) for node in self]) + "]"

    def __iter__(self):
        node = self.head
        first: bool = True
        while node is not None and (first or node != self.head):
            yield node
            node = node.next
            first = False


def part_one(cups: List[int]) -> int:
    head: LinkedList = LinkedList(cups)

    for i in range(100):
        print("-- move {} --".format(i))
        head = move(cups=head)
        head.head = head.head.next

    return 0
    # while final_cups[0] != 1:
    #     final_cups.append(final_cups.pop(0))
    #
    # return int("".join([str(i) for i in final_cups if i != 1]))


def move(cups: LinkedList) -> LinkedList:
    print("cups: {}".format(cups))

    removed_cups: Node = cups.head.next
    cups.head.next = cups.head.next.next.next.next
    print("pick up: {}".format(removed_cups))
    print("remaining: {}".format(cups))

    destination_cup: Optional[Node] = None
    counter: int = 2
    node = None

    while destination_cup is None:
        position_counter = (cups.head.value - counter) % max(cups).value + 1

        found: bool = False
        node = removed_cups
        for i in range(3):
            if node.value == position_counter:
                found = True


        counter += 1
        node = cups.head
        while position_counter != node.value:
            node = node.next
        destination_cup = node

    tmp = node.next
    node.next = removed_cups
    removed_cups.next.next.next = tmp

    return cups


def part_two(cups: List[int]) -> int:
    final_cups: List[int] = []
    final_cups.extend(cups)
    final_cups.extend([i for i in range(max(final_cups) + 1, 1000000 + 1)])

    for _ in range(10000000):
        final_cups: List[int] = move(cups=final_cups)
        final_cups.append(final_cups.pop(0))

    while final_cups[0] != 1:
        final_cups.append(final_cups.pop(0))

    return final_cups[1] * final_cups[2]


with open('example.txt', 'r') as file:
    for line in file.readlines():
        cups: List[int] = [int(i) for i in line.strip()]
        print(part_one(copy.deepcopy(cups)))
        # print(part_two(copy.deepcopy(cups)))
