#!/usr/bin/env python3

class Password(object):
    min: int
    max: int
    character: str
    password: str

    def __init__(self, min: int, max: int, character: str, password: str):
        self.min = int(min)
        self.max = int(max)
        self.character = str(character)
        self.password = str(password)

    def is_valid(self) -> bool:
        count: int = 0
        for c in self.password:
            if c == self.character:
                count = count + 1

        return self.min <= count and count <= self.max

    def is_position_valid(self) -> bool:
        return (self.password[self.min - 1] == self.character or self.password[self.max - 1] == self.character)    \
            and not (self.password[self.min - 1] == self.character and self.password[self.max - 1] == self.character)


part_one: int=0
part_two: int=0

with open('input.txt', 'r') as file:
    for line in file.readlines():
        line=line.replace('-', '#')
        line=line.replace(' ', '#')
        line=line.replace(':', '#')
        parts=line.split('#')
        password: Password=Password(
            min = parts[0], max = parts[1], character = parts[2], password = parts[4])

        if (password.is_valid()):
            part_one = part_one + 1

        if (password.is_position_valid()):
            part_two = part_two + 1

print("Part 1: " + str(part_one))
print("Part 2: " + str(part_two))
