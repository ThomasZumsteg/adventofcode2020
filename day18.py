"""Solution to day 18 of Advent of Code"""

from get_input import get_input, line_parser
import re


def rpn_evaluate(tokens):
    result = []
    for token in tokens:
        if isinstance(token, int):
            result.append(token)
        elif token == '+':
            result.append(result.pop() + result.pop())
        elif token == '*':
            result.append(result.pop() * result.pop())
        else:
            raise NotImplementedError
    assert len(result) == 1
    return result[0]


def rpn_parse(tokens, prec):
    stack = []
    output = []
    for token in tokens:
        if isinstance(token, int):
            output.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while True:
                temp = stack.pop()
                if temp == '(':
                    break
                output.append(temp)
        else:
            while len(stack) > 0 and prec(stack[-1], token):
                output.append(stack.pop())
            stack.append(token)
    return output + stack[::-1]


def part1(lines):
    total = 0

    def comp(a, b):
        return a in ('*', '+') and b in ('*', '+')

    for line in lines:
        tokens = rpn_parse(line, comp)
        total += rpn_evaluate(tokens)
    return total


def part2(lines):
    total = 0

    def comp(a, b):
        if a == '+':
            return a != b
        elif a == '*':
            if b == '+':
                return False
            return a != b
        return False

    for line in lines:
        tokens = rpn_parse(line, comp)
        total += rpn_evaluate(tokens)
    return total


def parse(line):
    return tuple(int(n) if n.isdigit() else n
                 for n in re.findall(r'\(|\d+|\+|\*|\)', line))


if __name__ == "__main__":
    assert part1([parse("1 + 2 * 3 + 4 * 5 + 6")]) == 71
    assert part2([parse("1 + 2 * 3 + 4 * 5 + 6")]) == 231
    assert part2([parse("1 + (2 * 3) + (4 * (5 + 6))")]) == 51
    LINES = line_parser(get_input(day=18, year=2020), parse=parse)
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
