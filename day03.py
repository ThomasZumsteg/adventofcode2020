"""Solution to day 3 of Advent of Code"""

from get_input import get_input, line_parser

from common import Point


def count_trees(lines, slope):
    pos = Point(0, 0)
    total = 0
    while pos.y < len(lines):
        if lines[pos.y][pos.x % len(lines[pos.y])] == '#':
            total += 1
        pos += slope
    return total


def part1(lines):
    return count_trees(lines, Point(3, 1))


def part2(lines):
    slopes = (
        Point(1, 1),
        Point(3, 1),
        Point(5, 1),
        Point(7, 1),
        Point(1, 2)
    )
    total = 1
    for slope in slopes:
        total *= count_trees(lines, slope)
    return total


if __name__ == "__main__":
    LINES = line_parser(get_input(day=3, year=2020), parse=list)
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
