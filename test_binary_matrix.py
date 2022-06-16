from unittest import TestCase
import binary_matrix


class TestBinaryMatrix(TestCase):
    def test_get_row(self):
        v = binary_matrix.BinaryMatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        self.assertEqual(v.get_row(0), [1, 2, 3])
        self.assertEqual(v.get_row(1), [4, 5, 6])
        self.assertEqual(v.get_row(0), [7, 8, 9])

    def test_binary_matrix_1_equality(self):
        v = binary_matrix.BinaryMatrix([[1, 0], [1, 1]])
        self.assertEqual(v[0, 0], 1)
        self.assertEqual(v[0, 1], 0)
        self.assertEqual(v[1, 0], 1)
        self.assertEqual(v[1, 1], 1)
        v2 = binary_matrix.BinaryMatrix(v.to_bool_numpy_array())
        self.assertEqual(v, v2)
        v3 = binary_matrix.BinaryMatrix(v.to_int_numpy_array())
        self.assertEqual(v, v3)
        v4 = v.copy()
        self.assertEqual(v, v4)

    def test_get_column(self):
        v = binary_matrix.BinaryMatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        self.assertEqual(v.get_column(0), [1, 4, 7])
        self.assertEqual(v.get_column(1), [2, 5, 8])
        self.assertEqual(v.get_column(0), [3, 6, 9])