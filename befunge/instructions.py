import random
from collections import namedtuple

from direction import Direction

Instruction = namedtuple('Instruction', [
    'push', 'output', 'direction', 'put', 'toggle_str_mode', 'skip', 'end', 'get'], )


def return_ops(direction=None, push=[], output=[], put={}, toggle_str_mode=False, end=False, skip=False, get=None):
    return Instruction(push, output, direction, put, toggle_str_mode, skip, end, get)


class PassThroughOps:
    ''' will write the symbol directy to the stack, when string_mode is activated all character will be added to the stack as literals '''

    def __init__(self):
        self.string_mode = False
        self.normal_ops = [str(n) for n in range(10)]

    def __getitem__(self, key):
        return lambda: return_ops(push=[key])

    def __contains__(self, key):
        if self.string_mode:
            return key != '"'
        else:
            return key in self.normal_ops

    def toggle_string_mode(self):
        self.string_mode = not self.string_mode


OPS_PASS = PassThroughOps()

''' instructions with not requirements to access stack for input '''
OPS_0 = {
    ' ': lambda: return_ops(),
    '>': lambda: return_ops(direction=Direction.RIGHT),
    '<': lambda: return_ops(direction=Direction.LEFT),
    '^': lambda: return_ops(direction=Direction.UP),
    'v': lambda: return_ops(direction=Direction.DOWN),
    '?': lambda: return_ops(direction=random.choice(Direction.to_list())),
    '"': lambda: return_ops(toggle_str_mode=True),
    '@': lambda: return_ops(end=True),
    '#': lambda: return_ops(skip=True)
}

OPS_1 = {
    '$': lambda a: return_ops(),
    '!': lambda a: return_ops(push=[1] if not a else [0]),
    '_': lambda a: return_ops(direction=Direction.RIGHT if a == 0 else Direction.LEFT),
    '|': lambda a: return_ops(direction=Direction.DOWN if a == 0 else Direction.UP),
    ':': lambda a: return_ops(push=[a, a] if a != 0 else [0, 0]),
    '.': lambda a: return_ops(output=[int(a)]),
    ',': lambda a: return_ops(output=[chr(a) if type(a) is int else a]),
}

OPS_2 = {
    '+': lambda a, b: return_ops(push=[a+b]),
    '-': lambda a, b: return_ops(push=[b - a]),
    '*': lambda a, b: return_ops(push=[a*b]),
    '/': lambda a, b: return_ops(push=[b//a] if a != 0 else [0]),
    '%': lambda a, b: return_ops(push=[b % a] if a != 0 else [0]),
    '`': lambda a, b: return_ops(push=[1] if b > a else [0]),
    '\\': lambda a, b: return_ops(push=[b, a] if b is not None else [0, a]),
    'g': lambda a, b: return_ops(get=[(b, a)]),
}

OPS_3 = {
    'p': lambda a, b, c: return_ops(put={(b, a): c}),
}


def lookup_symbol(c):
    if c in OPS_PASS:
        return (0, OPS_PASS[c])
    elif c in OPS_0:
        return (0, OPS_0[c])
    elif c in OPS_1:
        return (1, OPS_1[c])
    elif c in OPS_2:
        return (2, OPS_2[c])
    elif c in OPS_3:
        return (3, OPS_3[c])
    else:
        raise LookupError('symbol - {0} could not be mapped'.format(c))
