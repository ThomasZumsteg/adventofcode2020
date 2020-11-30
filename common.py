import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return Point(self.x - other.x, self.y - other.y)

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def angle(self, first, second):
        """Self if is the pivot"""
        angle = math.degrees(
            math.atan2(first.y-self.y, first.x-self.x) -
            math.atan2(second.y-self.y, second.x-self.x)
        )
        return angle + 360 if angle < 0 else angle

    def distance(self, other):
        diff = self - other
        return (diff.x**2 + diff.y**2)*0.5

    def turn_left(self):
        # > (1, 0) => ^ (0, -1)
        # ^ (0, -1) => < (-1, 0)
        # < (-1, 0) => v (0, 1)
        # v (0, 1) => > (1, 0)
        return Point(self.y, -self.x)

    def turn_right(self):
        return Point(-self.y, self.x)


Point.directions = (Point(0, 1), Point(0, -1), Point(1, 0), Point(-1, 0))
