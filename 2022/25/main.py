#!/usr/bin/env python
from pathlib import Path
from typing import Any, Dict, List

PARENT = Path(__file__).parent


class SNAFU(object):

    symbols: Dict[str, int] = {
        '2': 2,
        '1': 1,
        '0': 0,
        '-': -1,
        '=': -2
    }
    i_symbols: Dict[int, str] = {
        2: '2',
        1: '1',
        0: '0',
        -1: '-',
        -2: '='
    }

    value: int

    def __init__(self, _input: Any):
        super().__init__()

        if isinstance(_input, int):
            self.value = int(_input)
            return

        self.value = 0
        for i in range(len(_input)):
            c: str = _input[len(_input) - i - 1]
            self.value += (5 ** i) * self.symbols[c]

    def decimal(self) -> int:
        return self.value

    def snafu(self) -> str:
        #   Decimal          SNAFU
        #         1              1
        #         2              2  -> 2 * 10 ^ 0   :   2 * 5 ^ 0
        #         3             1=  ->  3 * 10 ^ 0  :   1 * 5 ^ 1 + (-2) * 5 ^ 0
        #         4             1-
        #         5             10
        #         6             11
        #         7             12  ->  7 * 10 ^ 0  :   1 * 5 ^ 1 + 2 * 5 ^ 0
        #                               (7 + 2) / 5 ->  1 R 4   ->  (4 - 2) (2)
        #                               (1 + 2) / 5 ->  0 R 3   ->  (3 - 2) (1)
        #         8             2=  ->  8 * 10 ^ 0  :   2 * 5 ^ 1 + (-2) * 5 ^ 0
        #                               (8 + 2) / 5   ->  2 R 0 -> (0 - 2)  (-2)
        #                               (2 + 2) / 5   ->  0 R 4 -> (4 - 2)  (2)
        #         9             2-
        #        10             20
        #        15            1=0  ->  1 * 10 ^ 1 + 5 * 10 ^ 0 :   1 * 5 ^ 2 + (-2) * 5 ^ 1 + (0) * 5 ^ 0
        #        20            1-0
        #      2022         1=11-2
        #     12345        1-0---0
        # 314159265  1121-1110-1=0

        snafu: str = ""
        quotient = self.value

        while quotient:
            remainder = (quotient + 2) % 5
            quotient = (quotient + 2) // 5
            s = self.i_symbols[remainder - 2]
            snafu = s + snafu

        return snafu


def read_from_file(file: Path) -> List[str]:
    with open(file) as f:
        return [line.strip() for line in f.readlines()]


def __part_one__(file: Path) -> str:
    snafus: List[str] = read_from_file(file)

    total: int = sum([SNAFU(snafu).decimal() for snafu in snafus])
    snafu: SNAFU = SNAFU(total)

    return snafu.snafu()


def __part_two__(file: Path) -> str:
    raise Exception("Not implemented")
    content: str = read_from_file(file)
    return None


def test() -> bool:
    #   SNAFU -> Decimal
    assert SNAFU("1").decimal() == 1
    assert SNAFU("2").decimal() == 2
    assert SNAFU("1=").decimal() == 3
    assert SNAFU("1-").decimal() == 4
    assert SNAFU("10").decimal() == 5
    assert SNAFU("11").decimal() == 6
    assert SNAFU("12").decimal() == 7
    assert SNAFU("2=").decimal() == 8
    assert SNAFU("2-").decimal() == 9
    assert SNAFU("20").decimal() == 10
    assert SNAFU("1=0").decimal() == 15
    assert SNAFU("1-0").decimal() == 20
    assert SNAFU("1=11-2").decimal() == 2022
    assert SNAFU("1-0---0").decimal() == 12345
    assert SNAFU("1121-1110-1=0").decimal() == 314159265

    #   Decimal          SNAFU
    assert SNAFU(1).snafu() == "1"
    assert SNAFU(2).snafu() == "2"
    assert SNAFU(3).snafu() == "1="
    assert SNAFU(4).snafu() == "1-"
    assert SNAFU(5).snafu() == "10"
    assert SNAFU(6).snafu() == "11"
    assert SNAFU(7).snafu() == "12"
    assert SNAFU(8).snafu() == "2="
    assert SNAFU(9).snafu() == "2-"
    assert SNAFU(10).snafu() == "20"
    assert SNAFU(15).snafu() == "1=0"
    assert SNAFU(20).snafu() == "1-0"
    assert SNAFU(2022).snafu() == "1=11-2"
    assert SNAFU(12345).snafu() == "1-0---0"
    assert SNAFU(314159265).snafu() == "1121-1110-1=0"

    return True


def part_one() -> str:
    test()
    example: str = __part_one__(PARENT.joinpath('example.txt'))
    assert example == '2=-1=0'
    answer: str = __part_one__(PARENT.joinpath('input.txt'))
    return answer


def part_two() -> str:
    example: str = __part_two__(PARENT.joinpath('example.txt'))
    assert example == 0
    answer: str = __part_two__(PARENT.joinpath('input.txt'))
    return answer


def main():
    print("Part One: {}".format(part_one()))
    print("Part Two: {}".format(part_two()))


if __name__ == '__main__':
    main()
