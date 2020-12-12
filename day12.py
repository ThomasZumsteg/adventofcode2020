"""Solution to day 12 of Advent of Code"""

from get_input import get_input, line_parser


def move(direction):
    def move_func(heading, position, value):
        return heading, position + (direction * value)
    return move_func


def turn(direction):
    def turn_func(heading, position, value):
        while value > 0:
            heading = direction(heading)
            value -= 90
        assert value == 0
        return heading, position
    return turn_func


RULES = {
    'N': move(0+1j),
    'S': move(0-1j),
    'E': move(1+0j),
    'W': move(-1+0j),
    'R': turn(lambda h: complex(h.imag, -h.real)),
    'L': turn(lambda h: complex(-h.imag, h.real)),
    'F': lambda h, p, v: (h, p + h * v),
}


def part1(lines):
    heading = 1+0j
    position = 0+0j
    rules = RULES.copy()
    for (order, value) in lines:
        heading, position = rules[order](heading, position, value)
    return int(abs(position.real) + abs(position.imag))


def swap(function):
    def swapped(heading, position, value):
        position, heading = function(position, heading, value)
        return heading, position
    return swapped


def part2(lines):
    waypoint = 10+1j
    position = 0+0j
    rules = RULES.copy()
    for order in ('N', 'S', 'E', 'W'):
        rules[order] = swap(rules[order])
    for (order, value) in lines:
        waypoint, position = rules[order](waypoint, position, value)
    return int(abs(position.real) + abs(position.imag))


def parse(line):
    return (line[0], int(line[1:]))


TEST = """F10
N3
F7
R90
F11"""

if __name__ == "__main__":
    assert part1(line_parser(TEST, parse=parse)) == 25
    assert part2(line_parser(TEST, parse=parse)) == 286
    LINES = line_parser(get_input(day=12, year=2020), parse=parse)
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
