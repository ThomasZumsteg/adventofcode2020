"""Solution to day 20 of Advent of Code"""

from get_input import get_input
import copy
import collections
import pickle


class Image:
    def __init__(self, img_id, tile=None):
        self.id = img_id
        self._tile = tile if tile is not None else []

    def __str__(self):
        return '\n'.join(self._tile)

    def __repr__(self):
        return f"Image({self.id})"

    def __hash__(self):
        return hash(str(self.id) + '\n'.join(self._tile))

    def from_str(image_id, text):
        return Image(image_id, tuple(text.splitlines()))

    def get_edge(self, edge):
        if edge == 0-1j:
            return self._tile[0]
        elif edge == 0+1j:
            return self._tile[-1]
        elif edge == 1+0j:
            return ''.join(row[-1] for row in self._tile)
        elif edge == -1+0j:
            return ''.join(row[0] for row in self._tile)
        raise NotImplementedError

    def mirror(self):
        return Image(self.id, [line[::-1] for line in self._tile])

    def rotate(self, steps):
        size = len(self._tile)
        rows = copy.deepcopy(self._tile)
        for _ in range(steps % 4):
            rows = [
                ''.join(list(rows[r][c] for r in range(size))[::-1])
                for c in range(size)]
        return Image(self.id, rows)

    def __eq__(self, other):
        return self.id == other.id


def fits(board, peice, location):
    for diff in (0+1j, 0-1j, 1+0j, -1+0j):
        space = board[diff + location]
        if len(space) == 0:
            continue
        if space[0].get_edge(-diff) != peice.get_edge(diff):
            return False
    return True


def get_possible(board, pos, images):
    in_use = set(img_row[0].id for img_row in board.values() if img_row != [])
    possible = []
    for image in images:
        if image.id in in_use:
            continue
        for image in (img.rotate(r) for img in (image.mirror(), image)
                      for r in range(4)):
            if fits(board, image, pos):
                possible.append(image)
    return possible


def part1(images):
    images = copy.deepcopy(images)
    size = len(images)**0.5
    board = collections.defaultdict(list)
    current = 0+0j
    board[current] = get_possible(board, current, images)
    while 0 <= current.real < size and 0 <= current.imag < size:
        print(current)
        if board[current] == []:
            if current.real-1 >= 0:
                current = complex(current.real-1, current.imag)
            else:
                current = complex(size-1, current.imag-1)
            board[current].pop(0)
        else:
            if current.real+1 < size:
                current = complex(current.real+1, current.imag)
            else:
                current = complex(0, current.imag+1)
            board[current] = get_possible(board, current, images)
    breakpoint()
    return board[0+0j][0].id * board[complex(0, size-1)][0].id *\
        board[complex(size-1, 0)][0].id *\
        board[complex(size-1, size-1)][0].id


SEA_MONSTER = """                  # \n#    ##    ##    ###\n #  #  #  #  #  #   """ # noqa


def flip(text):
    return '\n'.join(line[::-1] for line in text.splitlines())


def rotate(text, value):
    rows = text.splitlines()
    size = (len(text.splitlines()), len(text.splitlines()[0]))
    for _ in range(value % 4):
        rows = [''.join(rows[r][c] for r in range(size[0]))[::-1] for c in range(size[1])]  # noqa
        size = (size[1], size[0])
    return '\n'.join(rows)


def part2(images):
    with open('day20.pickle', 'rb') as fh:
        data = pickle.load(fh)
    size = int(len(images)**0.5)
    assert size * size == len(images)
    bottom = 0
    image = []
    for img_row in range(size):
        for img_col in range(size):
            tile = str(data[complex(img_col, img_row)][0]).splitlines()
            for r, row in enumerate(tile[1:-1], bottom):
                if img_col == 0:
                    image.append(row[1:-1])
                else:
                    image[r] += row[1:-1]
        bottom = len(image)
    image = '\n'.join(image)
    sea_monster = {}
    for r, row in enumerate(SEA_MONSTER.splitlines()):
        for c, value in enumerate(row):
            sea_monster[complex(r, c)] = value
    for mapping in [image, rotate(image, 1),
                    rotate(image, 2), rotate(image, 3),
                    flip(image), rotate(flip(image), 1),
                    rotate(flip(image), 2), rotate(flip(image), 3)]:
        sea_map = {}
        found = []
        for r, row in enumerate(mapping.splitlines()):
            for c, value in enumerate(row):
                sea_map[complex(r, c)] = value
        for point in sea_map.keys():
            for m, value in sea_monster.items():
                if value != '#':
                    continue
                if sea_map.get(point + m) != '#':
                    break
            else:
                found.append(point)
        if found:
            rough_water = set(p for p, v in sea_map.items() if v == '#')
            for point in found:
                for m, value in sea_monster.items():
                    if (point + m) in rough_water and value == '#':
                        rough_water.remove(point + m)
            return len(rough_water)
    raise NotImplementedError


def parse(text):
    tiles = []
    tile = None
    for line in text.splitlines():
        line = line.strip()
        if line == "":
            tile = None
        elif line.startswith('Tile'):
            tile = int(line.split(' ')[1].strip(':'))
            tiles.append(Image(tile))
        else:
            tiles[-1]._tile.append(line)
    return tiles


if __name__ == "__main__":
    LINES = parse(get_input(day=20, year=2020))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
