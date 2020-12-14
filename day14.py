"""Solution to day 14 of Advent of Code"""

from get_input import get_input, line_parser
from collections import defaultdict
import re
import itertools


def apply_mask(value, mask):
    value = list(f"{value:036b}")
    assert len(value) == len(mask) == 36
    result = []
    for v, m in zip(value, mask):
        if m == 'X':
            result.append(v)
        elif m == '1' or m == '0':
            result.append(m)
        else:
            raise NotImplementedError
    return int(''.join(result), 2)


def part1(lines):
    mem = defaultdict(int)
    mask = None
    for line in lines:
        if 'mask' == line[0]:
            mask = line[1]
        elif 'mem' == line[0]:
            mem[line[1]] = apply_mask(line[2], mask)
        else:
            raise NotImplementedError
    return sum(mem.values())


def make_masks(mask, value):
    count = mask.count('X')
    value = list(f"{value:036b}")
    assert len(value) == len(mask) == 36
    for combo in itertools.product('10', repeat=count):
        combo = list(combo)
        result = []
        for m, v in zip(mask, value):
            if m == 'X':
                result.append(combo.pop())
            elif m == '0':
                result.append(v)
            elif m == '1':
                result.append(m)
        assert len(combo) == 0
        assert len(result) == 36
        yield int(''.join(result), 2)


def part2(lines):
    mem = defaultdict(int)
    mask = None
    for line in lines:
        if 'mask' == line[0]:
            mask = line[1]
        elif 'mem' == line[0]:
            for addr in make_masks(mask, line[1]):
                mem[addr] = line[2]
        else:
            raise NotImplementedError
    return sum(mem.values())


def parse(line):
    mem = re.match(r"mem\[(\d+)\] = (\d+)", line)
    if mem:
        address, value = mem.groups()
        return ('mem', int(address), int(value))
    mask = re.match(r'mask = ([01X]+)', line)
    if mask:
        return ('mask',) + mask.groups()
    raise NotImplementedError


if __name__ == "__main__":
    LINES = line_parser(get_input(day=14, year=2020), parse=parse)
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
