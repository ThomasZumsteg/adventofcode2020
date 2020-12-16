"""Solution to day 15 of Advent of Code"""

from get_input import get_input
from itertools import count, islice


def game(starting):
    turns = {n: t for t, n in enumerate(starting[:-1], 1)}
    yield from iter(starting)
    last = starting[-1]
    for turn in count(len(starting)):
        if last not in turns:
            nxt = 0
        else:
            nxt = turn - turns[last]
        turns[last] = turn
        yield nxt
        last = nxt


def part1(lines):
    return next(islice(game(lines), 2020-1, None))


def part2(lines):
    return next(islice(game(lines), 30000000-1, None))


def parse(line):
    return tuple(int(n) for n in line.strip().split(','))


if __name__ == "__main__":
    assert part1((0, 3, 6)) == 436
    assert part1((1, 3, 2)) == 1
    assert part1((2, 1, 3)) == 10
    assert part1((1, 2, 3)) == 27
    assert part1((3, 1, 2)) == 1836
    assert part1((3, 2, 1)) == 438
    assert part1((3, 2, 1)) == 438
    LINES = parse(get_input(day=15, year=2020))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
