"""Solution to day 24 of Advent of Code"""

from get_input import get_input, line_parser
from collections import defaultdict


BLACK = False
WHITE = True
COMPASS = {
    'e': 2+0j,
    'se': 1-1j,
    'sw': -1-1j,
    'w': -2+0j,
    'nw': -1+1j,
    'ne': 1+1j,
}


def init_board(directions):
    tiles = defaultdict(lambda: WHITE)
    for direction in directions:
        position = 0+0j
        for d in direction:
            position += d
        tiles[position] = not tiles[position]
    return tiles


def adjacent(tiles, t):
    return sum(1 for a in COMPASS.values() if not tiles[t+a])


def part1(lines):
    board = init_board(lines)
    return sum(1 for v in board.values() if not v)


def part2(lines):
    tiles = init_board(lines)
    for _ in range(100):
        new = defaultdict(lambda: True)
        points = set(t + d for d in list(COMPASS.values()) + [0+0j]
                     for t, v in tiles.items() if not v)
        for p in points:
            adj = adjacent(tiles, p)
            if tiles[p] and adj == 2:
                new[p] = False
            elif not tiles[p] and (0 == adj or 2 < adj):
                new[p] = True
            else:
                new[p] = tiles[p]
        tiles = new
    return sum(1 for v in tiles.values() if not v)


def parse(line):
    # 'ew' + 'ns'
    direction = []
    while line:
        match = {(s, v) for s, v in COMPASS.items() if line.startswith(s)}
        assert len(match) == 1
        symbol, value = match.pop()
        direction.append(value)
        line = line[len(symbol):]
    return tuple(direction)


TEST = """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew"""

if __name__ == "__main__":
    assert part1(line_parser(TEST, parse=parse)) == 10
    assert part2(line_parser(TEST, parse=parse)) == 2208
    LINES = line_parser(get_input(day=24, year=2020), parse=parse)
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
