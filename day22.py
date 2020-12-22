"""Solution to day 22 of Advent of Code"""

from get_input import get_input


def part1(lines):
    player_1 = lines[1].copy()
    player_2 = lines[2].copy()
    while len(player_1) > 0 and len(player_2) > 0:
        a = player_1.pop(0)
        b = player_2.pop(0)
        if a > b:
            player_1.extend((a, b))
        elif b > a:
            player_2.extend((b, a))
        else:
            raise NotImplementedError
    if len(player_1) == 0:
        player_1 = player_2
    return sum(n * v for n, v in enumerate(player_1[::-1], 1))


def part2(lines):
    player_1 = lines[1].copy()
    player_2 = lines[2].copy()
    seen = set()
    stack = []
    while True:
        while len(player_1) > 0 and len(player_2) > 0:
            if (tuple(player_1), tuple(player_2)) in seen:
                if len(stack) > 0:
                    seen, cards, (old_player_1, old_player_2) = stack.pop()
                    player_1 = list(old_player_1 + cards)
                    player_2 = list(old_player_2)
                    continue
                else:
                    return sum(n * v for n, v in enumerate(player_1[::-1], 1))
            seen.add((tuple(player_1), tuple(player_2)))

            a = player_1.pop(0)
            b = player_2.pop(0)
            if len(player_1) >= a and len(player_2) >= b:
                stack.append((
                    seen,
                    (a, b),
                    (tuple(player_1), tuple(player_2)))
                )
                player_1 = player_1[:a]
                player_2 = player_2[:b]
                seen = set()
            elif a > b:
                player_1.extend((a, b))
            elif b > a:
                player_2.extend((b, a))
            else:
                raise NotImplementedError
        if len(stack) > 0:
            seen, cards, (old_player_1, old_player_2) = stack.pop()
            if len(player_1) == 0:
                player_2 = list(old_player_2 + cards[::-1])
                player_1 = list(old_player_1)
            else:
                player_1 = list(old_player_1 + cards)
                player_2 = list(old_player_2)
        else:
            break
    if len(player_1) == 0:
        player_1 = player_2
    return sum(n * v for n, v in enumerate(player_1[::-1], 1))


def parse(text):
    player = None
    decks = {
        1: [],
        2: [],
    }
    for line in text.splitlines():
        line = line.strip()
        if player is None:
            player = int(line.split(' ')[1][:1])
        elif line == "":
            player = None
        else:
            decks[player].append(int(line))
    return decks


TEST = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""


if __name__ == "__main__":
    assert part1(parse(TEST)) == 306
    assert part2(parse(TEST)) == 291
    LINES = parse(get_input(day=22, year=2020))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
