#!/bin/python

from typing import Dict, List, Set


def print_board(board) -> None :
    for row in board:
        print(row)

def find_bingo(board) -> bool:
    board_size: int = len(board)

    counts: Dict[int, int] = {}
    
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is None:

                if counts.get(i) is None:
                    counts[i] = 0
                counts[i] = counts[i] + 1

                if counts.get(j + board_size) is None:
                    counts[j + board_size] = 0
                counts[j + board_size] = counts[j + board_size] + 1
    
    for k, v in counts.items():
        if v == board_size:
            return True
    
    return False

def mark_number(board, number):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == number:
                board[i][j] = None
                return

def score(board, n: int) -> int:
    score: int = 0

    for row in board:
        score += sum([int(item) for item in row if item is not None])
    
    return (score * int(n))



with open('2021/04/input.txt', 'r') as file:
    content = file.read()

    parts = content.split('\n\n')

    numbers_drawn = parts[0].split(',')

    boards = [ [n.split() for n in board.split('\n')] for board in parts[1:] ]

    scores: List[int] = []
    complete: Set = set()

    for n in numbers_drawn:
        for board in boards:

            mark_number(board, n)
            
            if find_bingo(board):
                if (boards.index(board)) not in complete:
                    s = score(board, n)
                    scores.append(s)
                    complete.add(boards.index(board))
    
    print(scores[0])
    print(scores[-1])

