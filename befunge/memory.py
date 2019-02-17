
import math
from direction import Direction


class XBoundError(ValueError):

    def __init__(self, x, y, x_max, x_min=0):
        self.message = '({0},{1}) - XBound Error - {2} <= x <= {3}'.format(x,
                                                                           y, x_min, x_max)

        self.x = x
        self.y = y
        self.x_min = x_min
        self.x_max = x_max


class YBoundError(ValueError):
    def __init__(self, x, y, y_max, y_min=0):
        self.message = '({0},{1}) - YBound Error - {2} <= y <= {3}'.format(x,
                                                                           y, y_min, y_max)

        self.x = x
        self.y = y
        self.y_min = y_min
        self.y_max = y_max


class Memory:
    ''' abtracts pointer handling and memory interface '''

    EMPTY = [[' ']]

    def __init__(self, code):
        self.pointer = (0, 0)

        if code is None:
            self._memory = Memory.EMPTY
        elif type(code) is str:
            self._memory = [list(line) for line in code.split('\n')]
        elif type(code) is list:
            self._memory = [list(line) for line in code]
        else:
            raise TypeError(
                'code is {0} expected [str, list]'.format(type(code)))

    def update_pointer(self, direction, skip=False):
        x, y = self.pointer

        step = 2 if skip else 1

        if direction == Direction.DOWN:
            self.pointer = (x, y+step)
        elif direction == Direction.UP:
            self.pointer = (x, y-step)
        elif direction == Direction.LEFT:
            self.pointer = (x-step, y)
        elif direction == Direction.RIGHT:
            self.pointer = (x+step, y)
        else:
            raise TypeError('direction is not valid: ' + direction)

        # check if pointer is at the edge
        x, y = self.pointer

        if y >= len(self._memory) or y < 0:
            self.pointer = (x, y % len(self._memory))

        x, y = self.pointer

        if x >= len(self._memory[y]) or x < 0:
            self.pointer = (x % len(self._memory[y]), y)

        return self.current_op

    def dump(self):
        dump = ""

        for i, line in enumerate(self._memory):
            dump += str(i) + " " + " ".join(line) + "\n"

        return dump

    def get(self, x, y):
        x_len, y_len = self.shape

        if x >= x_len or x < 0:
            raise XBoundError(x, y, x_max=x_len - 1)

        if y >= y_len or y < 0:
            raise YBoundError(x, y, y_max=y_len - 1)

        return self._memory[y][x]

    def put(self, x, y, v):

        x_len, y_len = self.shape

        if x < 0:
            raise XBoundError(x, y, x_len)

        if y < 0:
            raise YBoundError(x, y, y_len)

        if y >= y_len:
            self.add_rows(y - y_len + 1)

        if x >= x_len:
            self.add_columns(x - x_len + 1)

        self._memory[y][x] = v

    def add_rows(self, n):
        x_len, _ = self.shape

        for _ in range(n):
            self._memory.append([" " for _ in range(x_len)])

    def add_columns(self, n):
        _, y_len = self.shape

        for _ in range(n):
            for y in range(y_len):
                self._memory[y].append(" ")

    @property
    def shape(self):
        if len(self._memory) == 0:
            return (0, 0)

        return (len(self._memory), len(self._memory[0]))

    @property
    def size(self):
        return self.shape[0] * self.shape[1]

    @property
    def current_op(self):
        x, y = self.pointer

        return self._memory[y][x]
