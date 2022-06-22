from unittest import TestCase
from _trashcan import binary_vector
import state


class TestBinaryVector(TestCase):
    def test_binary_vector_1(self):
        v = binary_vector.BinaryVector([1, 0, 1, 1])
        self.assertEqual(v[0], 1)
        self.assertEqual(v[1], 0)
        self.assertEqual(v[2], 1)
        self.assertEqual(v[3], 1)
        v2 = binary_vector.BinaryVector(v.to_bool_numpy_array())
        self.assertEqual(v, v2)
        v3 = binary_vector.BinaryVector(v.to_int_numpy_array())
        self.assertEqual(v, v3)
        v4 = v.copy()
        self.assertEqual(v, v4)

    def test_binary_vector_2(self):
        self.assertEqual(binary_vector.BinaryVector([1, 1, 0, 1]), binary_vector.BinaryVector([1, 1, 0, 1]))
        self.assertEqual(binary_vector.BinaryVector([1, 1, 0, 1]), [1, 1, 0, 1])
        self.assertEqual(binary_vector.BinaryVector([1, 1, 0, 1]), [True, True, False, True])

    def test_binary_vector_3(self):
        self.assertNotEqual(binary_vector.BinaryVector([1, 1, 0, 1]), binary_vector.BinaryVector([1, 0, 1, 1]))
        self.assertNotEqual(binary_vector.BinaryVector([1, 1, 0, 1]), [1, 0, 1, 1])
        self.assertNotEqual(binary_vector.BinaryVector([1, 1, 0, 1]), [True, False, True, True])

    def test_get_complement(self):
        v1 = binary_vector.BinaryVector([0, 1, 1, 0, 0, 1])
        v2 = v1.get_inverse()
        self.assertEqual(v2, [1, 0, 0, 1, 1, 0])
        v3 = v2.get_inverse()
        self.assertEqual(v1, v3)

    def test_get_union(self):
        v1 = binary_vector.BinaryVector([0, 1, 1, 0, 0, 1])
        v2 = binary_vector.BinaryVector([0, 0, 1, 1, 0, 0])
        v3 = v1.get_maximum(v2)
        self.assertEqual(v3, [0, 1, 1, 1, 0, 1])

    def test_get_intersection(self):
        v1 = binary_vector.BinaryVector([0, 1, 1, 0, 0, 1])
        v2 = binary_vector.BinaryVector([0, 1, 1, 1, 0, 0])
        v3 = binary_vector.get_minima(v1, v2)
        self.assertEqual(v3, [0, 1, 1, 0, 0, 0])

    def test_check_masking(self):
        v1 = binary_vector.BinaryVector([0, 1, 1, 0, 0, 1])
        v2 = binary_vector.BinaryVector([0, 1, 1, 1, 0, 0])
        v3 = binary_vector.BinaryVector([0, 1, 1, 0, 0, 0])
        self.assertTrue(v1.check_masking(v1))
        self.assertFalse(v1.check_masking(v2))
        self.assertTrue(v1.check_masking(v3))
        self.assertFalse(v2.check_masking(v1))
        self.assertTrue(v2.check_masking(v2))
        self.assertTrue(v2.check_masking(v3))
        self.assertFalse(v3.check_masking(v1))
        self.assertFalse(v3.check_masking(v2))
        self.assertTrue(v3.check_masking(v3))


class Test(TestCase):
    def test_get_minima(self):
        v1 = binary_vector.BinaryVector([1, 0, 1, 0, 0, 1, 0])
        v2 = binary_vector.BinaryVector([0, 1, 1, 0, 0, 1, 0])
        v3 = binary_vector.get_minima(v1, v2)
        self.assertEqual(v3, [0, 0, 1, 0, 0, 1, 0])

        v4 = state.IV([1, 0, 1, 0, 0, 1, 0])
        v5 = state.IV([0, 1, 1, 0, 0, 1, 0])
        v6 = binary_vector.get_minima(v4, v5)
        self.assertEqual(v6, [0, 0, 1, 0, 0, 1, 0])