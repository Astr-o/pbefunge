from direction import Direction
from instructions import Instruction, lookup_symbol, OPS_PASS


class ProcessorState:
    def __init__(self):
        self.tick = 0
        self.direction = Direction.RIGHT
        self.output = ""
        self.stack = []
        self.terminated = False
        self.string_mode = False

    def __str__(self):
        return "InterpraterState: tick={0} direction={1} stack={2} output={3} terminated={4}".format(self.tick, self.direction, self.stack, self.output, self.terminated)

    # stack operations

    def pop(self):
        try:
            return self.stack.pop()
        except IndexError:
            return 0

    def push(self, i):
        self.stack.append(i)

    def stop(self):
        self.terminated = True

    def toggle_string_mode(self):
        self.string_mode = not self.string_mode


class Processor:

    def __init__(self, memory, verbose=False):
        self.state = ProcessorState()
        self.memory = memory
        self.verbose = False

    def _exec_instruction(self, instruction):
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

        # retrieve values from memory
        if instruction.get:
            x, y = instruction.get
            v = self.memory.get(x, y)

            # put any values into memory
        for loc, v in instruction.put.items():
            x, y = loc
            self.memory.put(x, y, v)

        #
        if instruction.toggle_str_mode:
            self.state.toggle_string_mode()

        return self.memory.update_pointer(self.state.direction, skip=instruction.skip)

    def _fetch_instruction(self, op):
         # lookup symbol nargs, number of values to pop from the stack

        nargs, func = lookup_symbol(op)

        # pop relavent values from the stack
        args = [self.state.pop() for _ in range(nargs)]

        # build instruction by calling lambda
        instruction = func(*args) if args else func()

        return instruction

    def next_op(self):
        ''' excutes a single operation by loading for current pointer and updates pointer '''
        op = self.memory.current_op

        # fetch instruction and data from memory
        instruction = self._fetch_instruction(op)

        # update interperater state
        return self._exec_instruction(instruction)

    @property
    def pointer_value(self):
        return (self.memory.pointer, self.memory.current_op)

    @property
    def terminated(self):
        return bool(self.state.terminated)

    @property
    def output(self):
        return self.state.output
