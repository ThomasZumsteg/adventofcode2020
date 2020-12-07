"""Solution to day 7 of Advent of Code"""

from get_input import get_input, line_parser
from collections import defaultdict
import re


def part1(lines):
    contained = defaultdict(set)
    for bag, contains in lines:
        for _, contain in contains:
            contained[contain].add(bag)
    queue = ['shiny gold']
    seen = set()
    while queue:
        bag = queue.pop()
        if bag in seen:
            continue
        seen.add(bag)
        queue.extend(contained[bag])
    return len(seen) - 1


def part2(lines):
    contained = dict(lines)
    total = 0
    queue = list(contained['shiny gold'])
    while queue:
        count, bag_type = queue.pop()
        total += count
        for inner_count, inner_type in contained[bag_type]:
            queue.append((inner_count * count, inner_type))
    return total


def parse(line):
    bag = ' '.join(line.split(' ')[:2])
    contains = []
    # 1 muted blue bag
    for (count, bag_type) in re.findall(r'(\d+) (\w+ \w+) bags?', line):
        contains.append((int(count), bag_type))
    return (bag, tuple(contains))


test_text = """
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
"""

test_text_part_2 = """
shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.
"""

if __name__ == "__main__":
    assert part1(line_parser(test_text, parse=parse)) == 4
    assert part2(line_parser(test_text_part_2, parse=parse)) == 126
    LINES = line_parser(get_input(day=7, year=2020), parse=parse)
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
