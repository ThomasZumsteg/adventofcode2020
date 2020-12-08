"""Solution to day 8 of Advent of Code"""

from get_input import get_input, line_parser


class Program:
    def __init__(self, program):
        self._program = program
        self.index = 0
        self.accumulator = 0

    def jmp(self, value):
        self.index += value

    def acc(self, value):
        self.accumulator += value

    def nop(self, value):
        pass

    def __len__(self):
        return len(self._program)

    def __iter__(self):
        while 0 <= self.index < len(self):
            (op, value) = self._program[self.index]
            if op != "jmp":
                self.index += 1
            getattr(self, op)(value)
            yield self

    def run(self):
        seen = set()
        for step in self:
            if step.index in seen:
                break
            seen.add(step.index)
        return self


def part1(prog):
    computer = Program(prog)
    computer.run()
    return computer.accumulator


def part2(lines):
    for l_num, (cmd, value) in enumerate(lines):
        prog = lines[:]
        if cmd == 'jmp':
            prog[l_num] = ('nop', value)
        elif cmd == 'nop':
            prog[l_num] = ('jmp', value)
        else:
            continue
        result = Program(prog).run()
        if not (0 <= result.index < len(result)):
            return result.accumulator


def parse(line):
    command, value = line.split(' ')
    return (command, int(value))


TEST_TEST_PART1 = """
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
"""


if __name__ == "__main__":
    assert part1(line_parser(TEST_TEST_PART1, parse=parse)) == 5
    assert part2(line_parser(TEST_TEST_PART1, parse=parse)) == 8
    LINES = line_parser(get_input(day=8, year=2020), parse=parse)
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
