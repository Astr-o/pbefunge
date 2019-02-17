import unittest
import os
import sys

from .helpers import convert_list_to_chars, set_python_env

set_python_env()

from memory import Memory, XBoundError, YBoundError
from direction import Direction


class TestMemory(unittest.TestCase):

    def test_create_from_string(self):
        code = '123\n456\n789'
        memory = Memory(code)

        expected = convert_list_to_chars([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

        self.assertTupleEqual(memory.shape, (3, 3), 'shape is not correct')
        self.assertEqual(memory.size, 9, 'size is not correct')
        self.assertListEqual(memory._memory, expected)

    def test_create_from_list(self):
        code = ['123', '456', '789']
        memory = Memory(code)

        self.assertEqual(len(memory._memory), 3, 'y size incorrect')
        self.assertListEqual([len(l) for l in memory._memory], [
                             3, 3, 3], 'x size incorrect')

        self.assertListEqual(memory._memory, convert_list_to_chars(
            [[1, 2, 3], [4, 5, 6], [7, 8, 9]]))

    def test_pointer_directions(self):
        code = ['ab', 'dc']
        memory = Memory(code)

        self.assertEqual(memory.pointer, (0, 0),
                         'pointer at correct starting position')
        self.assertEqual(memory.current_op, 'a', 'operation is a')

        memory.update_pointer(Direction.RIGHT)

        self.assertEqual(memory.pointer, (1, 0),
                         'pointer at correct starting position')
        self.assertEqual(memory.current_op, 'b', 'operation is b')

        memory.update_pointer(Direction.DOWN)

        self.assertEqual(memory.pointer, (1, 1),
                         'pointer at correct starting position')
        self.assertEqual(memory.current_op, 'c', 'operation is c')

        memory.update_pointer(Direction.LEFT)

        self.assertEqual(memory.pointer, (0, 1),
                         'pointer at correct starting position')
        self.assertEqual(memory.current_op, 'd', 'operation is d')

    def test_pointer_ring_x(self):
        code = ['ab', 'dc']
        memory = Memory(code)

        self.assertEqual(memory.pointer, (0, 0),
                         'pointer at correct starting position')
        self.assertEqual(memory.current_op, 'a', 'operation is a')

        for _ in range(2):
            memory.update_pointer(Direction.LEFT)

        self.assertEqual(memory.pointer, (0, 0),
                         'pointer at correct starting position')
        self.assertEqual(memory.current_op, 'a', 'operation is a')

        for _ in range(2):
            memory.update_pointer(Direction.RIGHT)

        self.assertEqual(memory.pointer, (0, 0),
                         'pointer at correct starting position')
        self.assertEqual(memory.current_op, 'a', 'operation is a')

    def test_pointer_ring_y(self):
        code = ['ab', 'dc']
        memory = Memory(code)

        self.assertEqual(memory.pointer, (0, 0),
                         'pointer at correct starting position')
        self.assertEqual(memory.current_op, 'a', 'operation is a')

        for _ in range(2):
            memory.update_pointer(Direction.DOWN)

        self.assertEqual(memory.pointer, (0, 0),
                         'pointer at correct starting position')
        self.assertEqual(memory.current_op, 'a', 'operation is a')

        for _ in range(2):
            memory.update_pointer(Direction.UP)

        self.assertEqual(memory.pointer, (0, 0),
                         'pointer at correct starting position')
        self.assertEqual(memory.current_op, 'a', 'operation is a')

    def test_get(self):

        target = 'b'
        x, y = (1, 1)

        memory = Memory(['abc', 'd' + target + 'd'])

        result = memory.get(x, y)

        self.assertEqual(result, target, 'get result doesnt match target')

    def test_get_out_of_bound(self):

        memory = Memory(['abc', 'def', 'ghi'])

        test_cases = [
            (-1, 0, XBoundError),
            (5, 0, XBoundError),
            (0, -1, YBoundError),
            (0, 5, YBoundError)
        ]

        for x, y, error in test_cases:
            try:
                memory.get(x, y)
            except Exception as e:
                self.assertIsInstance(
                    e, error, 'test_case={0}'.format((x, y, type(error))))

    def test_put(self):

        inital_code = ['abc', 'def', 'ghi']

        test_cases = [
            (0, 0, 'z', [['z', 'b', 'c'],
                         ['d', 'e', 'f'],
                         ['g', 'h', 'i']]),
            (3, 0, 'z', [['a', 'b', 'c', 'z'],
                         ['d', 'e', 'f', ' '],
                         ['g', 'h', 'i', ' ']]),
            (1, 3, 'z', [['a', 'b', 'c'],
                         ['d', 'e', 'f'],
                         ['g', 'h', 'i'],
                         [' ', 'z', ' ']])
        ]

        for c in test_cases:
            x, y, v, expected = c

            memory = Memory(inital_code)
            memory.put(x, y, v)

            self.assertEqual(memory._memory, expected)

    def test_put_out_of_bound(self):

        memory = Memory(['abc', 'def', 'ghi'])

        test_cases = [
            (-1, 0, XBoundError),
            (0, -1, YBoundError),
        ]

        for x, y, expected in test_cases:
            try:
                memory.get(x, y)
            except Exception as e:
                self.assertIsInstance(
                    e, expected,  'test_case={0}'.format((x, y, type(expected))))


if __name__ == '__main__':
    unittest.main()
