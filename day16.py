"""Solution to day 16 of Advent of Code"""

from get_input import get_input
import re


def fits(rule, value):
    assert rule[0][1] <= rule[0][1] and rule[1][0] <= rule[1][1]
    return rule[0][0] <= value <= rule[0][1] or\
        rule[1][0] <= value <= rule[1][1]


def part1(lines):
    rules = lines['rules'].copy()
    invalid = 0
    invalid_ticket = set()
    for ticket in lines['nearby_tickets']:
        for number in ticket:
            matches = [name for name, rule in rules.items()
                       if fits(rule, number)]
            if len(matches) == 0:
                invalid_ticket.add(tuple(ticket))
                invalid += number
    return invalid


def part2(lines):
    rules = lines['rules'].copy()
    valid_tickets = []
    for ticket in lines['nearby_tickets']:
        if all(any(fits(rule, number) for rule in rules.values())
               for number in ticket):
            valid_tickets.append(ticket)
    fields = {}
    for col in range(len(lines['your_ticket'])):
        fields[col] = set(lines['rules'].keys())
        for ticket in valid_tickets:
            for name, rule in rules.items():
                if not fits(rule, ticket[col]):
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
        total *= lines['your_ticket'][col]
    return total

    raise NotImplementedError


def parse(text):
    output = {
        'your_ticket': [],
        'rules': {},
        'nearby_tickets': []
    }
    state = "RULES"
    pointer = output['rules']
    for line in text.splitlines():
        line = line.strip()
        if state == "RULES":
            if line == "":
                state = "YOUR_TICKET"
                continue
            m = re.match(r'(.+): (\d+)-(\d+) or (\d+)-(\d+)', line)
            pointer[m.group(1)] = (
                (int(m.group(2)), int(m.group(3))),
                (int(m.group(4)), int(m.group(5))),
            )
        elif state == 'YOUR_TICKET':
            if line == "your ticket:":
                pointer = output['your_ticket']
                continue
            elif line == "":
                state = "NEARBY_TICKETS"
                continue
            else:
                pointer.extend(int(n) for n in line.split(','))
        elif state == "NEARBY_TICKETS":
            if line == "nearby tickets:":
                pointer = output["nearby_tickets"]
                continue
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
