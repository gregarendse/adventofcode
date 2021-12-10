#!/bin/python

from dataclasses import dataclass
from typing import Dict, List, Set
import statistics


score_table: Dict[str, int] = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}


def part_one(lines: List[str]) -> int:
    score: int = 0

    for line in lines:
        character_stack: List[str] = []

        for char in line.strip():
            # If closing, is previous mathcing opening?
            if ')' == char or ']' == char or '}' == char or '>' == char:

                # Get last character
                if len(character_stack) > 0:
                    last_char: str = character_stack.pop()

                    if last_char == '(' and char != ')':
                        score += score_table.get(char)
                        break

                    if last_char == '[' and char != ']':
                        score += score_table.get(char)
                        break

                    if last_char == '{' and char != '}':
                        score += score_table.get(char)
                        break

                    if last_char == '<' and char != '>':
                        score += score_table.get(char)
                        break
            else:
                character_stack.append(char)
    
    return score
        

def autocomplete_score(character_stack: List[str]) -> int:
    score: int = 0
    for char in reversed(character_stack):
        score *= 5
        if char == '(':
            score += 1
        elif char == '[':
            score += 2
        elif char == '{':
            score += 3
        elif char == '<':
            score += 4
    return score


def part_two(lines: List[str]) -> None:
    score: int = 0
    scores: List[int] = []

    for line in lines:
        character_stack: List[str] = []
        incomplete: bool = False

        for char in line.strip():

            # If closing, is previous mathcing opening?
            if ')' == char or ']' == char or '}' == char or '>' == char:

                # Get last character
                if len(character_stack) > 0:
                    last_char: str = character_stack.pop()

                    if last_char == '(' and char != ')':
                        incomplete = True
                        break

                    if last_char == '[' and char != ']':
                        incomplete = True
                        break

                    if last_char == '{' and char != '}':
                        incomplete = True
                        break

                    if last_char == '<' and char != '>':
                        incomplete = True
                        break
            else:
                character_stack.append(char)
        
        if incomplete:
            continue

        score = autocomplete_score(character_stack)
        scores.append(score)
    
    return statistics.median(scores)
 


with open('2021/10/input.txt', 'r') as file:
    lines: List[str] = file.readlines()

print(part_one(lines))
print(part_two(lines))
