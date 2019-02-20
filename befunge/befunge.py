from memory import Memory
from processor import Processor


class BefungeVM:

    @staticmethod
    def run_program(code, verbose=False):

        # creates memory and loads code provided
        memory = Memory(code)

        # create processor with access to memory
        processor = Processor(memory, verbose)

        while not processor.terminated:

            if verbose:
                print("pointer = {0}".format(processor.pointer_value))
                print(str(processor.state))

            processor.next_op()

        return processor.output
