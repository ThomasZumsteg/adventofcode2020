"""Solution to day 11 of Advent of Code"""

from get_input import get_input


def surround(location, seek):
    total = 0
    for diff in (1+1j, 1+0j, 1-1j, 0+1j, 0-1j, -1+1j, -1+0j, -1-1j):
        if seek(location, diff):
            total += 1
    return total


def update(grid, rules):
    new = grid.copy()
    for location in grid.keys():
        new[location] = rules(location)
    return new


def part1(seating):
    last = None
    while seating != last:
        last = seating

        def seek(pos, diff):
            return last.get(pos + diff) == '#'

        def rules(location):
            seat = last.get(location)
            if seat == "L" and surround(location, seek) == 0:
                return '#'
            elif seat == '#' and surround(location, seek) >= 4:
                return 'L'
            return seat

        seating = update(last, rules)
        assert len(last) == len(seating)
    return sum(1 for value in seating.values() if value == '#')


def part2(seating):
    last = None
    while seating != last:
        last = seating

        def seek(pos, diff):
            seat = last.get(pos+diff)
            if seat == '#':
                return True
            elif seat == 'L' or seat is None:
                return False
            return seek(pos+diff, diff)

        def rules(location):
            seat = last.get(location)
            if seat == "L" and surround(location, seek) == 0:
                return '#'
            elif seat == '#' and surround(location, seek) >= 5:
                return 'L'
            return seat

        seating = update(last, rules)
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
