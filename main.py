#!/usr/bin/python

from datetime import date
from subprocess import Popen

import click


@click.command()
@click.option('-d', '--day', type=int, default=date.today().day)
@click.option('-y', '--year', type=int, default=date.today().year)
@click.option('-t', '--test', is_flag=True, type=bool, default=False)
def main(day: int = None, year: int = None, test: bool = False):
    input_file: str
    if test:
        input_file = "example.txt"
    else:
        input_file = "input.txt"

    popen = Popen(
        ["python", "main.py", input_file],
        cwd="{year:0>4}/{day:0>2}".format(year=year, day=day)
    )
    popen.wait()


if __name__ == '__main__':
    main()
