import unittest
from collections import defaultdict
from typing import Dict

from main import compatible, Point


class Test(unittest.TestCase):

    def test_compatible(self):
        """
   | is a vertical pipe connecting north and south.
    - is a horizontal pipe connecting east and west.
    L is a 90-degree bend connecting north and east.
    J is a 90-degree bend connecting north and west.
    7 is a 90-degree bend connecting south and west.
    F is a 90-degree bend connecting south and east.
    . is ground; there is no pipe in this tile.
    S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
        """
        answers: Dict[str, bool] = defaultdict(bool)
        answers["S\n|"] = True
        answers["|\nS"] = True
        answers["-S"] = True
        answers["S-"] = True
        answers["S\nL"] = True
        answers["LS"] = True
        pipes: str = "S|-LJ7F"
        for i in range(len(pipes)):
            for j in range(i + 1, len(pipes)):
                expr = compatible(Point(pipe=pipes[i], x=0, y=1), Point(pipe=pipes[j], x=1, y=1))
                s = pipes[i] + pipes[j]
                # print(f"'{s}':{expr},")
                self.assertEqual(expr, answers[s], s)

                expr = compatible(Point(pipe=pipes[j], x=0, y=1), Point(pipe=pipes[i], x=1, y=1))
                s = pipes[j] + pipes[i]
                # print(f"'{s}':{expr},")
                self.assertEqual(expr, answers[s], s)

                expr = compatible(Point(pipe=pipes[i], x=0, y=1), Point(pipe=pipes[j], x=0, y=2))
                s = pipes[i] + "\n" + pipes[j]
                # print(f"'{s}':{expr},")
                self.assertEqual(expr, answers[s], s)

                expr = compatible(Point(pipe=pipes[j], x=0, y=1), Point(pipe=pipes[i], x=0, y=2))
                s = pipes[j] + "\n" + pipes[i]
                # print(f"'{s}':{expr},")
                self.assertEqual(expr, answers[s], s)
