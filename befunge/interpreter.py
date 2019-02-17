from memory import Memory
from direction import Direction
from instructions import Instruction, lookup_symbol, OPS_PASS


class InterpereterState:
    def __init__(self, code):
        self.tick = 0
        self._memory = Memory(code)
        self.direction = Direction.RIGHT
        self.output = ""
        self.stack = []
        self.terminated = False

    def __str__(self):
        return "InterpraterState: tick={5} pointer={3} current_op={4} direction={0} stack={2} output={1}".format(self.direction, self.output, self.stack, self._memory.pointer, self._memory.current_op, self.tick)

    @property
    def pointer(self):
        return self._memory.pointer

    @property
    def current_op(self):
        return self._memory.current_op

    def get(self, x, y):
        self._memory.get(x, y)

    def put(self, x, y, v):
        self._memory.put(x, y)

    def pop(self):
        return self.stack.pop()

    def push(self, i):
        self.stack.append(i)

    def advance_pointer(self, skip=False):
        self.tick += 1
        return self._memory.update_pointer(self.direction, skip)

    def stop(self):
        self.terminated = True


class Interpereter:

    def __init__(self, code, verbose=False):
        self.state = InterpereterState(code)
        self.verbose = False

    def _exec_op(self, instruction):
        ''' 
        this method executes a insturction by modifying InterpereterState 
        '''
        if not isinstance(instruction, Instruction):
            raise TypeError('instruction must be of type ' + str(Instruction))

        # exit instruction
        if instruction.end:
            return self.state.stop()

        # direction change instruction
        if instruction.direction is not None:
            self.state.direction = instruction.direction

        # push any new values to stack
        for i in instruction.push:
            self.state.push(i)

        # append items to the output buffer
        for i in instruction.output:
            self.state.output += str(i)

        if instruction.get:
            x, y = instruction.get
            v = self.state.get(x, y)

            # put any values into memory
        for p, v in instruction.put.items():
            x, y = p
            self.state._memory.put(x, y, v)

        #
        if instruction.toggle_str_mode:
            OPS_PASS.toggle_string_mode()

        return self.state.advance_pointer(skip=instruction.skip)

    def run_op(self):
        op = self.state.current_op

        # lookup symbol nargs, number of values for the function
        nargs, func = lookup_symbol(op)

        # pop relavent values from the stack
        args = [self.state.pop() for _ in range(nargs)]

        # build instruction output from args
        instruction = func(*args) if args else func()

        # update interperater state
        return self._exec_op(instruction)

    @property
    def terminated(self):
        return bool(self.state.terminated)

    @property
    def output(self):
        return self.state.output
