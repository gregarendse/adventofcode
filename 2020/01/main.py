#!/usr/bin/env python3

lines = []

with open('input.txt', 'r') as file:
    for line in file.readlines():
        lines.append(int(line))

for first in lines:
    for second in lines:
        if ((first + second) == 2020):
            print("{first} * {second} : {mult}".format(first=first, second=second, mult=(first*second)))

        for third in lines:
            if ((first + second + third) == 2020):
                print("{first} * {second} * {third} : {mult}".format(first=first, second=second, third=third, mult=(first*second*third)))

        