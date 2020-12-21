"""Solution to day 21 of Advent of Code"""

from get_input import get_input, line_parser
import re


def get_mapping(recipies):
    all_ingredients = set(i for (ingred, _) in recipies for i in ingred)
    allergens = {a: all_ingredients.copy()
                 for (_, allergens) in recipies for a in allergens}
    for (parts, contains) in recipies:
        for c in contains:
            allergens[c] = allergens[c].intersection(set(parts))
    mapping = {}
    while len(allergens) > 0:
        new = {}
        for key, value in allergens.items():
            if len(value) == 1:
                mapping[key] = value.pop()
            else:
                new[key] = value.difference(set(mapping.values()))
        if new == allergens:
            raise NotImplementedError()
        allergens = new
    return mapping


def part1(lines):
    mapping = set(get_mapping(lines).values())
    return sum(1 for (ingred, _) in lines for i in ingred
               if i not in mapping)


def part2(lines):
    mapping = get_mapping(lines)
    return ','.join(kv[1] for kv in
                    sorted(mapping.items(), key=lambda kv: kv[0]))


def parse(line):
    m = re.match(r"([^()]+)(?: \(contains (.+)\))", line)
    ingredients = tuple(m.group(1).strip().split(' '))
    contains = tuple(m.group(2).split(', '))
    return (ingredients, contains)


if __name__ == "__main__":
    LINES = line_parser(get_input(day=21, year=2020), parse=parse)
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
