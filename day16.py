"""Solution to day 16 of Advent of Code"""

from get_input import get_input
import itertools
import re


def fits(rule, value):
    assert rule[0][1] <= rule[0][1] and rule[1][0] <= rule[1][1]
    return rule[0][0] <= value <= rule[0][1] or\
        rule[1][0] <= value <= rule[1][1]


def part1(lines):
    invalid = 0
    for number in itertools.chain(*lines['nearby tickets']):
        if all(not fits(rule, number) for rule in lines['rules'].values()):
            invalid += number
    return invalid


def part2(lines):
    rules = lines['rules'].copy()
    fields = {n: set(lines['rules']) for n in range(len(lines['rules']))}
    for ticket in lines['nearby tickets']:
        if not all(any(fits(rule, number) for rule in rules.values())
                   for number in ticket):
            continue
        for col, num in enumerate(ticket):
            for name, rule in rules.items():
                if not fits(rule, num):
                    fields[col].remove(name)
    solved = set()
    names = {}
    while len(solved) != len(fields):
        for key, value in fields.items():
            if key in names:
                continue
            diff = value - solved
            if len(diff) == 1:
                name = next(iter(diff))
                solved.add(name)
                names[key] = name
                break
            elif len(diff) == 0:
                raise NotImplementedError
    total = 1
    for col, name in names.items():
        if not name.startswith('departure'):
            continue
        total *= lines['your ticket'][col]
    return total


def parse(text):
    output = {
        'your ticket': [],
        'rules': {},
        'nearby tickets': []
    }
    state = 'rules'
    pointer = output['rules']
    for line in text.splitlines():
        line = line.strip()
        if line == '':
            state = None
        elif state is None:
            state = line.strip(':')
            pointer = output[state]
        elif state == 'rules':
            m = re.match(r'(.+): (\d+)-(\d+) or (\d+)-(\d+)', line)
            pointer[m.group(1)] = (
                (int(m.group(2)), int(m.group(3))),
                (int(m.group(4)), int(m.group(5))),
            )
        elif state == 'your ticket':
            pointer.extend(int(n) for n in line.split(','))
        elif state == 'nearby tickets':
            pointer.append([int(n) for n in line.split(',')])
    return output


TEST = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
"""


if __name__ == "__main__":
    assert part1(parse(TEST)) == 71
    LINES = parse(get_input(day=16, year=2020))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
