"""Solution to day 5 of Advent of Code"""

from get_input import get_input, line_parser

import math


def binary_search(directions, start, stop):
    for d in directions:
        if d:
            stop = math.floor((stop - start) / 2) + start
        else:
            start = math.ceil((stop - start) / 2) + start
    return start


def part1(boardingpasses):
    max_id = 0
    for boardingpass in boardingpasses:
        row = binary_search([char == "F" for char in boardingpass[:7]], 0, 127)
        col = binary_search([char == "L" for char in boardingpass[7:]], 0, 7)
        max_id = max(row * 8 + col, max_id)
    return max_id


def part2(boardingpasses):
    seats = {(row, col) for row in range(128) for col in range(8)}
    for boardingpass in boardingpasses:
        row = binary_search([char == "F" for char in boardingpass[:7]], 0, 127)
        col = binary_search([char == "L" for char in boardingpass[7:]], 0, 7)
        seats.remove((row, col))
    seat = [s for s in seats if 10 < s[0] and s[0] < 100]
    assert len(seat) == 1
    seat = seat.pop()
    return seat[0] * 8 + seat[1]


if __name__ == "__main__":
    LINES = line_parser(get_input(day=5, year=2020), parse=list)
    assert binary_search([c == "F" for c in "FBFBBFF"], 0, 127) == 44
    assert binary_search([c == 'L' for c in "RLR"], 0, 7) == 5
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
