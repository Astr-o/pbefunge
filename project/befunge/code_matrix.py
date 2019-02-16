from direction import Direction


class CodeMatrix:
    ''' abtracts pointer handling '''

    def __init__(self, code):
        if type(code) is str:
            self.code_matrix = [list(line) for line in code.split('\n')]
        elif type(code) is list:
            self.code_matrix = [list(line) for line in code]
        else:
            raise TypeError(
                'code is {0} expected [str, list]'.format(type(code)))
        self.pointer = (0, 0)

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

        if y >= len(self.code_matrix) or y < 0:
            self.pointer = (x, y % len(self.code_matrix))

        x, y = self.pointer

        if x >= len(self.code_matrix[y]) or x < 0:
            self.pointer = (x % len(self.code_matrix[y]), y)

        return self.current_op

    def code_to_string(self):
        output = ""

        for i, line in enumerate(self.code_matrix):
            output += str(i) + " " + " ".join(line) + "\n"

        return output

    @property
    def current_op(self):
        x, y = self.pointer

        return self.code_matrix[y][x]
