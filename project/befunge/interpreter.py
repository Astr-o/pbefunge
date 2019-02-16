from code_matrix import CodeMatrix
from direction import Direction
from instructions import OPS_0, OPS_1, OPS_2, OPS_END, OPS_PUSH, OPS_SKIP, OPS_STR


class InterperaterState:

    def __init__(self, code):
        self.tick = 0
        self.code_matrix = CodeMatrix(code)
        self.direction = Direction.RIGHT

        self.output = ""
        self.stack = []
        self.run = True

    def pop(self):
        return self.stack.pop()

    def push(self, i):
        self.stack.append(i)

    def run_op(self):
        op = self.code_matrix.current_op
        d = self.direction

        if op in OPS_PUSH:
            result = OPS_PUSH[op](d)
        elif op is OPS_SKIP:
            self.code_matrix.update_pointer(self.direction, skip=True)
            return
        elif op in OPS_END:
            self.run = False
            return
        elif op in OPS_STR:
            OPS_PUSH.toggle_string_mode()
            self.code_matrix.update_pointer(self.direction)
            return
        elif op in OPS_0:
            result = OPS_0[op](d)
        elif op in OPS_1:
            a = self.pop()
            result = OPS_1[op](d, a)
        elif op in OPS_2:
            a = self.pop()
            b = self.pop()
            result = OPS_2[op](d, a, b)

        if not result:
            raise Exception('no result found')

        stack_vals, output_vals, d = result

        self.direction = d

        for v in stack_vals:
            self.push(v)

        for v in output_vals:
            self.output += v

        self.code_matrix.update_pointer(self.direction)

    def __str__(self):
        return "InterpraterState: direction={0} output={1} stack={2} pointer={3} current_op={4}".format(self.direction, self.output, self.stack, self.code_matrix.pointer, self.code_matrix.current_op)
