"""Solution to day 13 of Advent of Code"""

from get_input import get_input
import math
import itertools


def part1(lines):
    start, buses = lines
    next_arrival = (None, float("inf"))
    for bus in buses:
        if bus == 'x':
            continue
        next_arrival = min(
            next_arrival,
            (bus, math.ceil(start / bus) * bus),
            key=lambda n: n[1]
        )
    return next_arrival[0] * (next_arrival[1] - start)


def bus_lcm(bus_a, bus_b):
    period = bus_a[1] * bus_b[1] // math.gcd(bus_a[1], bus_b[1])
    for offset in itertools.count(bus_a[0], bus_a[1]):
        if (offset - bus_b[0]) % bus_b[1] == 0:
            return (offset, period)


def part2(lines):
    buses = list(e for e in enumerate(lines[1]) if e[1] != "x")
    final = buses[0]
    for bus in buses[1:]:
        final = bus_lcm(final, bus)
    return final[1] - final[0]


def parse(text):
    lines = text.splitlines()
    start = int(lines[0].strip())
    buses = [
        int(val) if val != 'x' else val
        for val in lines[1].strip().split(',')
    ]
    return (start, buses)


TEST = """939
7,13,x,x,59,x,31,19"""

if __name__ == "__main__":
    assert part1(parse(TEST)) == 295
    assert part2((None, [17, 'x', 13, 19])) == 3417
    assert part2(parse(TEST)) == 1068781
    LINES = parse(get_input(day=13, year=2020))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
