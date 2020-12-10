"""Solution to day 10 of Advent of Code"""

from get_input import get_input, line_parser
from collections import defaultdict
import functools


def part1(adaptors):
    chain = [0] + sorted(adaptors) + [max(adaptors) + 3]
    diffs = [b - a for a, b in zip(chain, chain[1:])]
    return diffs.count(1) * diffs.count(3)


def part2(adaptors):
    assert len(set(adaptors)) == len(adaptors)
    chain = [0] + sorted(adaptors)
    paths = defaultdict(int, {0: 1})
    for i, adaptor in enumerate(chain):
        for value in chain[i+1:]:
            if value - adaptor > 3:
                break
            paths[value] += paths[adaptor]
    return paths[max(adaptors)]


def part2_recurse(adaptors):
    assert len(set(adaptors)) == len(adaptors)

    @functools.lru_cache
    def paths(step):
        if step == 0:
            return 1
        if step not in adaptors:
            return 0
        return paths(step-1) + paths(step-2) + paths(step-3)

    return paths(max(adaptors))


TEST1 = [16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4]

if __name__ == "__main__":
    assert part2(TEST1) == 8
    LINES = line_parser(get_input(day=10, year=2020))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
    # assert part2_recurse(LINES) == part2(LINES)
