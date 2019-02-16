from direction import Direction
import random


class PassThroughOps:
    def __init__(self):
        self.string_mode = False
        self.normal_ops = [str(n) for n in range(10)]

    def __getitem__(self, key):
        return lambda d: ([key], [], d)

    def __contains__(self, key):
        if self.string_mode:
            return key != '"'
        else:
            return key in self.normal_ops

    def toggle_string_mode(self):
        self.string_mode = not self.string_mode


OPS_PUSH = PassThroughOps()

OPS_END = {
    '@': None
}

OPS_SKIP = {
    '#': None
}

OPS_STR = {
    '"': None
}

OPS_0 = {
    ' ': lambda d: ([], [], d),
    '>': lambda d: ([], [], Direction.RIGHT),
    '<': lambda d: ([], [], Direction.LEFT),
    '^': lambda d: ([], [], Direction.UP),
    'v': lambda d: ([], [], Direction.DOWN),
    '?': lambda d: ([], [], random.choice(Direction.to_list()))
}

OPS_1 = {
    '!': lambda d, a: ([1] if not a else [0], [], d),
    '_': lambda d, a: ([], [], Direction.RIGHT if a == 0 else Direction.LEFT),
    '|': lambda d, a: ([], [], Direction.DOWN if a == 0 else Direction.UP),
    ':': lambda d, a: ([a, a] if a != 0 else [0, 0], [], d),
    '$': lambda d, a: ([], [], d),
    '.': lambda d, a: ([], [int(a)], d),
    ',': lambda d, a: ([], [chr(a) if type(a) is int else a], d),
}

OPS_2 = {
    '+': lambda d, a, b: ([a+b], [], d),
    '-': lambda d, a, b: ([b-a], [], d),
    '*': lambda d, a, b: ([a*b], [], d),
    '/': lambda d, a, b: ([b//a] if a != 0 else [0], [], d),
    '%': lambda d, a, b: ([b % a] if a != 0 else [0], [], d),
    '`': lambda d, a, b: ([1] if b > a else [0], [], d),
    '\\': lambda d, a, b: ([b, a] if b is not None else [0, a], [], d),
}
