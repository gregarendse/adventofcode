#!/bin/python

from typing import Dict, List, Set


def solve(output: List[str], digit_segment_map: Dict[int, List[str]]) -> int:
    solution: str = ""
    for o in output:

        if len(o) == 2:
            """
                Only 1 has a length of 2
            """
            solution += '1'
        elif len(o) == 3:
            """
                Only 7 has a length of 3
            """
            solution += '7'
        elif len(o) == 4:
            """
                Only 4 has a length of 4
            """
            solution += '4'
        elif len(o) == 7:
            """
                Only 8 has a length of 7
            """
            solution += '8'
        elif len(o) == 6 and set.union(digit_segment_map[3], digit_segment_map[4]).issubset(set(o[:])):
            """
                _           _
                 | + |_| = |_|
                 |     |     |
                
                The union of set of the 7 and the 4 segments results in the segments needed to display a 9
            """
            solution += '9'
        elif len(o) == 6 and set.union((digit_segment_map[7] - digit_segment_map[4]), digit_segment_map[3]).issubset(set(o[:])):
            """
                 _           _
                |_| - |_| = 
                |_|     |   |_
    
                 _    _    _
                    +  | =  |
                |_     |  |_|

                Looks like a 0
            """
            solution += '0'
        elif len(o) == 6 and (digit_segment_map[7] - digit_segment_map[2]).issubset(set(o[:])):
            """
                 _           _
                |_| -   | = |_  < Unique feature
                |_|     |   |_
                  
                Looks like a 6
            """
            solution += '6'
        elif len(o) == 5 and set(digit_segment_map[3]).issubset(set(o[:])):
            """
                _     _
                 | in _|
                 |    _|

                Looks like a 3
            """
            solution += '3'
        elif len(o) == 5 and (digit_segment_map[4] - digit_segment_map[2]).issubset(set(o[:])):
            """
                       
                |_| -  | = |_   < Unique feature
                  |    |

                Looks like a 5
            """
            solution += '5'
        elif len(o) == 5 and (digit_segment_map[7] - digit_segment_map[4]).issubset(set(o[:])):
            """
                 _           _
                |_| - |_| = 
                |_|     |   |_  < Unique feature

                Looks like a 2
            """
            solution += '2'
        else:
            solution += " "
            print(f"error: {o}, solution: {solution}")
            raise Exception

    return int(solution)


def part_one(lines: List[str]) -> None:
    count: int = 0

    for line in lines:
        output: str = line.split('|')[1].strip()

        for value in output.split():
            if len(value) in [2, 4, 3, 7]:
                count += 1

    print(count)


def part_two(lines: List[str]) -> None:
    total: int = 0

    for line in lines:

        signal_patterns, output = line.strip().split('|')
        output: List[str] = output.strip().split(' ')

        digit_segment_map: Dict[int, Set[str]] = {
            len(pattern): set(pattern[:]) for pattern in signal_patterns.strip().split(" ")
        }

        total += int(solve(output, digit_segment_map))

    print(total)


with open('2021/08/input.txt', 'r') as file:
    lines: List[str] = file.readlines()

part_one(lines)
part_two(lines)
