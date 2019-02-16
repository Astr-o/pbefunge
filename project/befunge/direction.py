from enum import IntEnum


class Direction(IntEnum):
    UP = 0,
    DOWN = 1,
    LEFT = 2,
    RIGHT = 3,

    @staticmethod
    def to_list():
        return list(map(int, Direction))
