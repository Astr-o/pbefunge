import unittest
import os
import sys

MODULE_FOLDER = os.path.join(os.path.split(
    os.path.dirname(__file__))[0], 'befunge')

print(MODULE_FOLDER)

if MODULE_FOLDER not in sys.path:
    sys.path.append(MODULE_FOLDER)


from code_matrix import CodeMatrix
from direction import Direction

from helpers import convert_list_to_chars


class TestCodeMatrix(unittest.TestCase):

    def test_create_from_string(self):
        code = '123\n456\n789'
        matrix = CodeMatrix(code)

        self.assertEqual(len(matrix.code_matrix), 3, 'y size incorrect')
        self.assertListEqual([len(l) for l in matrix.code_matrix], [
                             3, 3, 3], 'x size incorrect')

        self.assertListEqual(matrix.code_matrix, convert_list_to_chars(
            [[1, 2, 3], [4, 5, 6], [7, 8, 9]]))

    def test_create_from_list(self):
        code = ['123', '456', '789']
        matrix = CodeMatrix(code)

        self.assertEqual(len(matrix.code_matrix), 3, 'y size incorrect')
        self.assertListEqual([len(l) for l in matrix.code_matrix], [
                             3, 3, 3], 'x size incorrect')

        self.assertListEqual(matrix.code_matrix, convert_list_to_chars(
            [[1, 2, 3], [4, 5, 6], [7, 8, 9]]))

    def test_pointer_directions(self):
        code = ['ab', 'dc']
        matrix = CodeMatrix(code)

        self.assertEqual(matrix.pointer, (0, 0),
                         'pointer at correct starting position')
        self.assertEqual(matrix.current_op, 'a', 'operation is a')

        matrix.update_pointer(Direction.RIGHT)

        self.assertEqual(matrix.pointer, (1, 0),
                         'pointer at correct starting position')
        self.assertEqual(matrix.current_op, 'b', 'operation is b')

        matrix.update_pointer(Direction.DOWN)

        self.assertEqual(matrix.pointer, (1, 1),
                         'pointer at correct starting position')
        self.assertEqual(matrix.current_op, 'c', 'operation is c')

        matrix.update_pointer(Direction.LEFT)

        self.assertEqual(matrix.pointer, (0, 1),
                         'pointer at correct starting position')
        self.assertEqual(matrix.current_op, 'd', 'operation is d')

    def test_pointer_ring_x(self):
        code = ['ab', 'dc']
        matrix = CodeMatrix(code)

        self.assertEqual(matrix.pointer, (0, 0),
                         'pointer at correct starting position')
        self.assertEqual(matrix.current_op, 'a', 'operation is a')

        for _ in range(2):
            matrix.update_pointer(Direction.LEFT)

        self.assertEqual(matrix.pointer, (0, 0),
                         'pointer at correct starting position')
        self.assertEqual(matrix.current_op, 'a', 'operation is a')

        for _ in range(2):
            matrix.update_pointer(Direction.RIGHT)

        self.assertEqual(matrix.pointer, (0, 0),
                         'pointer at correct starting position')
        self.assertEqual(matrix.current_op, 'a', 'operation is a')

    def test_pointer_ring_y(self):
        code = ['ab', 'dc']
        matrix = CodeMatrix(code)

        self.assertEqual(matrix.pointer, (0, 0),
                         'pointer at correct starting position')
        self.assertEqual(matrix.current_op, 'a', 'operation is a')

        for _ in range(2):
            matrix.update_pointer(Direction.DOWN)

        self.assertEqual(matrix.pointer, (0, 0),
                         'pointer at correct starting position')
        self.assertEqual(matrix.current_op, 'a', 'operation is a')

        for _ in range(2):
            matrix.update_pointer(Direction.UP)

        self.assertEqual(matrix.pointer, (0, 0),
                         'pointer at correct starting position')
        self.assertEqual(matrix.current_op, 'a', 'operation is a')


if __name__ == '__main__':
    unittest.main()
