"""Solution to day 6 of Advent of Code"""

from get_input import get_input


def part1(groups):
    result = 0
    for group in groups:
        result += len(set(answer for person in group for answer in person))
    return result


def part2(groups):
    result = 0
    for group in groups:
        result += sum(
            1 for q in set(answer for person in group for answer in person)
            if all(q in person for person in group))
    return result


def parse(text):
    result = [[]]
    for line in text.splitlines():
        if line == "":
            result.append([])
        else:
            result[-1].append(list(line))
    return result


if __name__ == "__main__":
    LINES = parse(get_input(day=6, year=2020))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
