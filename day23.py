"""Solution to day 23 of Advent of Code"""

from get_input import get_input
from dataclasses import dataclass
import itertools


def part1(lines, rounds=100):
    cups = list(lines)
    for r in range(rounds):
        three = cups[1:4]
        cups[1:4] = []
        dest = cups[0] - 1
        while dest not in cups:
            dest -= 1
            if dest <= 0:
                dest = 9
        index = cups.index(dest)
        cups[index+1:index+1] = three
        cups.append(cups.pop(0))
    index = cups.index(1)
    cups = cups[index+1:] + cups[:index]
    return int(''.join(str(d) for d in cups))


@dataclass
class Node:
    value: int
    next: 'Node' = None

    def step(self, n):
        p = self
        for _ in range(n-1):
            p = p.next
        return p

    def snip(self, start, end):
        first = self.step(start-1).next
        last = first.step(end-start)
        self.next = last.next
        last.next = first
        return first, last

    def __repr__(self):
        rep = [str(self.value)]
        node = self.next
        while node != self:
            rep.append(str(node.value))
            node = node.next
        return f"[{','.join(rep)}]"


def part2(lines, rounds=10_000_000, num_nodes=1_000_000):
    last = Node(lines[0])
    cups = last
    values = {
        lines[0]: last
    }
    for c in itertools.chain(lines[1:], range(10, num_nodes+1)):
        last.next = Node(c)
        values[c] = last.next
        last = last.next
    last.next = cups
    for r in range(rounds):
        print(f"{r}", end="\r")
        first, last = cups.snip(1, 4)
        dest = cups.value - 1
        skip = {
            first.value,
            first.next.value,
            first.next.next.value,
        }
        while not (0 < dest <= num_nodes) or dest in skip:
            dest -= 1
            if dest <= 0:
                dest = num_nodes
        index = values[dest]
        last.next = index.next
        index.next = first
        cups = cups.next
    print()
    index = values[1]
    return index.next.value * index.next.next.value


def parse(text):
    return tuple(int(c) for c in text)


if __name__ == "__main__":
    assert part1(parse('389125467'), rounds=10) == 92658374
    assert part1(parse('389125467'), rounds=100) == 67384529
    assert part2(parse('389125467')) == 149245887792
    LINES = parse(get_input(day=23, year=2020).strip())
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
