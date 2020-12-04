"""Solution to day 2 of Advent of Code"""

from get_input import get_input, line_parser

import re


def exactly_one(value, a, b):
    return a != b and (a == value or b == value)


def part1(lines):
    return sum(1 for ((a, b), letter, password) in lines
               if a <= password.count(letter) <= b)


def part2(lines):
    return sum(1 for ((a, b), letter, password) in lines
               if exactly_one(letter, password[a-1], password[b-1]))


def parse(line):
    m = re.match(r'^(\d+)-(\d+) (.+): (.+)$', line)
    small, big, letter, password = m.groups()
    return ((int(small), int(big)), letter, password)


if __name__ == "__main__":
    LINES = line_parser(get_input(day=2, year=2020), parse=parse)
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
