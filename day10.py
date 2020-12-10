"""Solution to day 10 of Advent of Code"""

from get_input import get_input, line_parser
from collections import defaultdict


def part1(adaptors):
    chain = [0] + sorted(adaptors) + [max(adaptors) + 3]
    diffs = [b - a for a, b in zip(chain, chain[1:])]
    return diffs.count(1) * diffs.count(3)


def part2(adaptors):
    assert len(set(adaptors)) == len(adaptors)
    chain = [0] + sorted(adaptors)
    paths = defaultdict(int, {0: 1})
    for adaptor in chain:
        for value in [a for a in chain if 1 <= a - adaptor <= 3]:
            paths[value] += paths[adaptor]
    return paths[max(adaptors)]


TEST1 = [16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4]

if __name__ == "__main__":
    assert part2(TEST1) == 8
    LINES = line_parser(get_input(day=10, year=2020))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
