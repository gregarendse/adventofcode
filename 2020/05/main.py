from typing import List

class Seat(object):

    def __init__(self, row: int, column: int) -> None:
        super().__init__()
        self.row = int(row)
        self.column = int(column)
        self.seat_id = self.row * 8 + self.column



seat_ids: List[int] = []

with open('input.txt', 'r') as file:
    for line in file.readlines():
        line = line.strip()
        line = line.replace('F', '0')
        line = line.replace('B', '1')
        line = line.replace('R', '1')
        line = line.replace('L', '0')
        row = int(line[:7], 2)
        column = int(line[7:10], 2)
        seat_id = row * 8 + column
        seat_ids.append(seat_id)

seat_ids.sort()

print(max(seat_ids))

for i in range(max(seat_ids)):
    if (i + 1) in seat_ids and (i - 1) in seat_ids and i not in seat_ids:
        print(i)
        break
