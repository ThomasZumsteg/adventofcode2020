"""Solution to day 9 of Advent of Code"""

from get_input import get_input, line_parser
import itertools


def part1(lines, preamble=25):
    for i in itertools.count(preamble):
        if not any(a + b == lines[i] for a, b in
                   itertools.combinations(lines[i-preamble:i], 2)):
            return lines[i]
    raise NotImplementedError


def part2(lines, preamble=25):
    target = part1(lines, preamble=preamble)
    for i in range(0, len(lines)):
        for j in range(i+1, len(lines)):
            total = sum(lines[i:j])
            if total == target:
                return min(lines[i:j]) + max(lines[i:j])
            elif total > target:
                break
    raise NotImplementedError


TEST = [35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182, 127,
        219, 299, 277, 309, 576]

if __name__ == "__main__":
    assert part1(TEST, preamble=5) == 127
    assert part2(TEST, preamble=5) == 62
    LINES = line_parser(get_input(day=9, year=2020))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
