"""Solution to day 19 of Advent of Code"""

from get_input import get_input


def matches_rule(rule, message, rules):
    queue = [(message, r) for r in rules[rule]]
    while queue:
        msg, steps = queue.pop()
        # print(f"{msg}: {steps}")
        if len(steps) == 0:
            if len(msg) == 0:
                return True
        elif isinstance(steps[0], str):
            if msg.startswith(steps[0]):
                msg = msg[len(steps[0]):]
                queue.append((msg, steps[1:]))
        elif isinstance(steps[0], int):
            for add in rules[steps[0]]:
                queue.append((msg, add + steps[1:]))
        else:
            raise NotImplementedError()
    return False


def part1(lines):
    rules = lines['RULES']
    total = 0
    for message in lines['MESSAGES']:
        if matches_rule(0, message, rules):
            total += 1
    return total


def part2(lines):
    rules = lines['RULES'].copy()
    rules[8] = ((42,), (42, 8))
    rules[11] = ((42, 31), (42, 11, 31))
    total = 0
    for message in lines['MESSAGES']:
        if matches_rule(0, message, rules):
            total += 1
    return total


def parse(text):
    state = 'RULES'
    result = {
        'RULES': {},
        'MESSAGES': [],
    }
    for line in text.splitlines():
        line = line.strip()
        if state == 'RULES':
            if line == '':
                state = 'MESSAGES'
                continue
            num, rule = line.split(': ')
            if rule.count(' | ') == 1:
                rule = tuple(rule.split(' | '))
            elif rule.count('|') == 0:
                rule = tuple((rule, ))
            else:
                raise NotImplementedError()
            result[state][int(num)] =\
                tuple(tuple(
                    int(r) if r.isdigit() else r.strip('"')
                    for r in rule.split(' ')
                ) for rule in rule)
        elif state == 'MESSAGES':
            result[state].append(line)
    return result


TEST = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb"""


TEST2 = """42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba"""

if __name__ == "__main__":
    assert part1(parse(TEST)) == 2
    assert part2(parse(TEST2)) == 12
    LINES = parse(get_input(day=19, year=2020))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
