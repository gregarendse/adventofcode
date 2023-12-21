#!/usr/bin/python
import importlib
import os
from datetime import date

import click
from aocd.exceptions import PuzzleLockedError
from aocd.models import Puzzle
from aocd.utils import blocker


@click.group()
@click.option('-d', '--day', type=int, default=date.today().day)
@click.option('-y', '--year', type=int, default=date.today().year)
# @click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, day: int = None, year: int = None):
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    ctx.ensure_object(dict)

    ctx.obj['day'] = int(day)
    ctx.obj['year'] = int(year)
    ctx.obj['puzzle'] = Puzzle(day=day, year=year)
    ctx.obj['dir'] = "{year}/{day}".format(year=year, day=day)


@cli.command()
@click.pass_context
def init(ctx):
    year: int = ctx.obj['year']
    day: int = ctx.obj['day']

    day_directory: str = "{year}/{day}".format(year=year, day=day)
    os.makedirs(day_directory, exist_ok=True)

    puzzle = Puzzle(day=day, year=year)

    try:
        data = puzzle.input_data
    except PuzzleLockedError:
        blocker(quiet=False, until=(year, day))
        data = puzzle.input_data

    with open(day_directory + "/input.txt", 'w') as f:
        f.write(data)

    for i, example in enumerate(puzzle.examples):
        with open(day_directory + f"/example.txt", "w") as f:
            f.write(example.input_data)

        parameters = {
            'part_one_example_answer': example.answer_a if example.answer_a is not None else 0,
            'part_two_example_answer': example.answer_b if example.answer_b is not None else 0
        }

        with open("template/00/main.py") as i_f:
            with open(day_directory + "/main.py", "w") as o_f:
                template = i_f.read()
                template = template.format(**parameters)
                o_f.write(template)
        break


@cli.command()
@click.pass_context
def solve(ctx):
    puzzle: Puzzle = ctx.obj['puzzle']
    module: str = "{year}.{day}.main".format(year=ctx.obj['year'], day=ctx.obj['day'])
    solver = importlib.import_module(module)

    if not puzzle.answered_a:
        part_one: int = solver.part_one()
        print("Part One: {}".format(part_one))
        puzzle.answer_a = part_one
    elif not puzzle.answered_b:
        part_two = solver.part_two()
        print("Part Two: {}".format(part_two))
        puzzle.answer_b = part_two


if __name__ == '__main__':
    cli(obj={})
