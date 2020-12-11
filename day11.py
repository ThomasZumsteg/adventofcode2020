"""Solution to day 11 of Advent of Code"""

from get_input import get_input
import itertools


def surround(grid, location, seek):
    total = 0
    for diff in (1+1j, 1+0j, 1-1j, 0+1j, 0-1j, -1+1j, -1+0j, -1-1j):
        if seek(location, diff):
            total += 1
    return total


def part1(seating):
    last = None
    while seating != last:
        last = seating

        def seek(pos, diff):
            return last.get(pos + diff) == '#'

        seating = {}
        for location, seat in last.items():
            if seat == '.':
                seating[location] = '.'
            elif seat == "L" and surround(last, location, seek) == 0:
                seating[location] = '#'
            elif seat == '#' and surround(last, location, seek) >= 4:
                seating[location] = 'L'
            else:
                seating[location] = seat
        assert len(last) == len(seating)
    return sum(1 for value in seating.values() if value == '#')


def part2(seating):
    last = None
    while seating != last:
        last = seating

        def seek(pos, diff):
            for count in itertools.count(1):
                seat = last.get(pos + count * diff)
                if seat == '#':
                    return True
                elif seat == 'L' or seat is None:
                    return False

        seating = {}
        for location, seat in last.items():
            if seat == '.':
                seating[location] = '.'
            elif seat == "L" and surround(last, location, seek) == 0:
                seating[location] = '#'
            elif seat == '#' and surround(last, location, seek) >= 5:
                seating[location] = 'L'
            else:
                seating[location] = seat
        assert len(last) == len(seating)
    return sum(1 for value in seating.values() if value == '#')


def parse(text):
    return {
        complex(r, c): seat
        for r, row in enumerate(text.strip().splitlines())
        for c, seat in enumerate(iter(row.strip()))
    }


TEST = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""


if __name__ == "__main__":
    assert part2(parse(TEST)) == 26
    LINES = parse(get_input(day=11, year=2020))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
