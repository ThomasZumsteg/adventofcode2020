"""Solution to day 17 of Advent of Code"""

from get_input import get_input
from collections import defaultdict
import itertools


def print_grid(grid):
    for z in range(-2, 3, 1):
        print(f"z={z}")
        for r in range(-1, 4):
            for c in range(-1, 4):
                print(grid.get((r, c, z), '.'), end='')
            print()
        print()
    print('-'*10)


def neighbors(point):
    for diff in itertools.product((-1, 0, 1), repeat=len(point)):
        if all(d == 0 for d in diff):
            continue
        neighbor = tuple(a + b for a, b in zip(point, diff))
        yield neighbor


def part1(grid):
    current = {k: v for k, v in grid.items() if v == '#'}
    for _ in range(6):
        prev = current
        current = {}
        active = set(n for p, v in prev.items()
                     for n in neighbors(p) if v == '#')
        for point in active:
            value = prev.get(point, '.')
            count = sum(1 for n in neighbors(point) if prev.get(n, '.') == '#')
            if value == '#' and (count == 2 or count == 3):
                current[point] = '#'
            elif value == '.' and count == 3:
                current[point] = '#'
    return len(current)


def part2(grid):
    current = {}
    for k, v in grid.items():
        k = k + (0,)
        if v != '#':
            continue
        current[k] = v
    for _ in range(6):
        prev = current
        current = {}
        active = set(n for p, v in prev.items()
                     for n in neighbors(p) if v == '#')
        for point in active:
            value = prev.get(point, '.')
            count = sum(1 for n in neighbors(point) if prev.get(n, '.') == '#')
            if value == '#' and (count == 2 or count == 3):
                current[point] = '#'
            elif value == '.' and count == 3:
                current[point] = '#'
    return len(current)


def parse(text):
    result = defaultdict(lambda: '.')
    for r, row in enumerate(text.splitlines()):
        row = row.strip()
        for c, value in enumerate(row):
            result[(r, c, 0)] = value
    return result


TEST = """.#.
..#
###"""


if __name__ == "__main__":
    assert part1(parse(TEST)) == 112
    assert part2(parse(TEST)) == 848
    LINES = parse(get_input(day=17, year=2020))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
