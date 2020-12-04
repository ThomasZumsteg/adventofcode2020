"""Solution to day 4 of Advent of Code"""

from get_input import get_input
from string import hexdigits, digits


def valid(passport, checks):
    for field, check in checks.items():
        if check is None:  # Skip optional fields
            continue
        if field not in passport or not check(passport[field]):
            return False
    return True


def part1(passports):
    checks = {
        "byr": lambda _: True,
        "iyr": lambda _: True,
        "eyr": lambda _: True,
        "hgt": lambda _: True,
        "hcl": lambda _: True,
        "ecl": lambda _: True,
        "pid": lambda _: True,
        "cid": None,  # Optional field
    }
    return sum(1 for passport in passports if valid(passport, checks))


def part2(passports):

    def height(f):
        if f.endswith("in"):
            return 59 <= int(f[:-2]) <= 76
        elif f.endswith("cm"):
            return 150 <= int(f[:-2]) <= 193
        return False

    def hair(f):
        return f[0] == "#" and \
            len(f) == 7 and \
            all(d in set(list(hexdigits)) for d in f[1:])

    def eye_color(f):
        valid_eye_colors = ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth')
        return f in valid_eye_colors

    def pid(f):
        return len(f) == 9 and all(d in digits for d in f)

    checks = {
        "byr": lambda f: 1920 <= int(f) <= 2002,
        "iyr": lambda f: 2010 <= int(f) <= 2020,
        "eyr": lambda f: 2020 <= int(f) <= 2030,
        "hgt": height,
        "hcl": hair,
        "ecl": eye_color,
        "pid": pid,
        "cid": None,
    }
    return sum(1 for passport in passports if valid(passport, checks))


def parse(text):
    entries = []
    entry = {}
    text += "\n"
    for line in text.splitlines():
        line = line.strip()
        if line == "" and entry != {}:
            entries.append(entry)
            entry = {}
        else:
            entry.update(dict(field.split(':') for field in line.split(' ')))
    return entries


if __name__ == "__main__":
    LINES = parse(get_input(day=4, year=2020))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
