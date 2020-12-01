"""Solution do day 1 of Advent of Code"""

from get_input import get_input, line_parser

import itertools


def part1(lines):
    for a, b in itertools.combinations(lines, 2):
        if a + b == 2020:
            return a * b


def part2(lines):
    for a, b, c in itertools.combinations(lines, 3):
        if a + b + c == 2020:
            return a * b * c
    raise NotImplementedError


if __name__ == "__main__":
    LINES = line_parser(get_input(day=1, year=2020))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
