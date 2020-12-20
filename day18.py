"""Solution to day 18 of Advent of Code"""

from get_input import get_input, line_parser
from operator import add, mul
import re


def find_match_index(symbols):
    stack = 0
    for j, sym in enumerate(symbols):
        if sym == ')':
            stack += 1
        elif sym == '(':
            stack -= 1
        if stack == 0:
            return j


# def evaluate(symbols):
#     if len(symbols) == 1 and isinstance(symbols[0], int):
#         return symbols[0]
#     elif symbols[0] == ')':
#         j = find_match_index(symbols)
#         lnum = evaluate(symbols[1:j])
#         if len(symbols) <= j+1:
#             return lnum
#         op = symbols[j+1]
#         rnum = evaluate(symbols[j+2:])
#     else:
#         lnum, op = symbols[:2]
#         rnum = evaluate(symbols[2:])
#     return eval(f"{int(lnum)}{op}{int(rnum)}")


def find_match_index_v2(symbols):
    stack = 0
    for j, sym in enumerate(symbols):
        if sym == '(':
            stack += 1
        elif sym == ')':
            stack -= 1
        if stack == 0:
            return j


def evaluate_v2(symbols):
    symbols = list(symbols)
    if len(symbols) == 1 and isinstance(symbols[0], int):
        return symbols[0]
    elif symbols[0] == '(':
        j = find_match_index(symbols)
        num = evaluate_v2(symbols[1:j])
        symbols[0:j+1] = [num]
    elif symbols[1] == '+':
        if isinstance(symbols[2], int):
            symbols[:3] = [symbols[0] + symbols[2]]
        elif symbols[2] == '(':
            j = find_match_index_v2(symbols[2:]) + 2
            symbols[:j+1] = [symbols[0] + evaluate_v2(symbols[3:j])]
    elif symbols[1] == '*':
        symbols[0:] = [symbols[0] * evaluate_v2(symbols[2:])]
    else:
        raise NotImplementedError()
    return evaluate_v2(symbols)


def evaluate(symbols):
    operators = []
    output = []
    for symbol in symbols:
        if isinstance(symbol, int):
            output.append(symbol)
        elif symbol == '+':
            operators.append(add)
        elif symbol == '*':
            operators.append(mul)
        elif symbol == '(':
            operators.append('(')
        elif symbol == ')':
            symbol = operators.pop()
            while symbol != '(':
                output.append(symbol)
                symbol = operators.pop()
    breakpoint()
    while True:
        operator = operators.pop()
        opera


def part1(lines):
    total = 0
    for line in lines:
        val = evaluate(line)
        total += val
    return total


def part2(lines):
    total = 0
    for line in lines:
        val = evaluate_v2(line)
        total += val
    return total
    raise NotImplementedError


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
