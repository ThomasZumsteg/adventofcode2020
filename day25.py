"""Solution to day 25 of Advent of Code"""

from get_input import get_input, line_parser
import itertools


def transform(subject_number, loop_size):
    result = subject_number
    for _ in range(loop_size-1):
        result *= subject_number
        result %= 20201227
    return result


def part1(lines):
    door_public, card_public = lines
    door_loop = None
    card_loop = None
    loop_number = 1
    public = 7
    while door_loop is None or card_loop is None:
        print(f"{loop_number}: {public}")
        loop_number += 1
        public = (7 * public) % 20201227

        if card_loop is None and public == card_public:
            card_loop = loop_number
        if door_loop is None and public == door_public:
            door_loop = loop_number
    private = transform(door_public, card_loop)
    assert private == transform(card_public, door_loop)
    return private


def part2(lines):
    return "Merry Christmas!"


if __name__ == "__main__":
    assert part1([17807724, 5764801]) == 14897079
    LINES = line_parser(get_input(day=25, year=2020))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
