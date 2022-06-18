from unittest import TestCase
import kripke_structure as ks
import numpy as np
import logging

logging.basicConfig(level=logging.DEBUG)


class Test(TestCase):
    def test_coerce_binary_value(self):
        self.assertEqual(ks.coerce_binary_value(False), 0)
        self.assertEqual(ks.coerce_binary_value(True), 1)
        self.assertEqual(ks.coerce_binary_value(0), 0)
        self.assertEqual(ks.coerce_binary_value(1), 1)
        self.assertEqual(ks.coerce_binary_value('0'), 0)
        self.assertEqual(ks.coerce_binary_value('1'), 1)
        self.assertEqual(ks.coerce_binary_value(-5), 0)
        self.assertEqual(ks.coerce_binary_value(17), 1)

    def test_coerce_incidence_vector(self):
        v1 = ks.coerce_incidence_vector([1, 0, 1])
        # self.assertTrue(isinstance(ks.coerce_incidence_vector([True, False]), ks.IncidenceVector))

    def test_coerce_binary_matrix(self):
        m1 = [[1, 1, 1], [1, 0, 1], [0, 0, 0]]
        m2 = ks.coerce_binary_matrix(m1)
        self.assertIsInstance(m2, ks.BinaryMatrix)
        with self.assertRaises(IndexError):
            ks.coerce_binary_matrix([[1, 2, 3], [4, 5]])

    def test_eq(self):
        o1 = [0, 1, 0, 1, 1, 0, 0, 0, 0]
        o2 = [0, 1, 0, 1, 0, 0, 0, 0, 0]
        o3 = [0, 1, 0, 1, 1, 0, 0, 0, 0]
        self.assertTrue(ks.equals(o1, o3))
        self.assertFalse(ks.equals(o1, o2))
        self.assertFalse(ks.equals(o2, o3))

    def test_coerce_set(self):
        s1 = ['e1', 'e2', 'e3']
        s2 = ks.coerce_set(s1)
        self.assertIsInstance(s2, ks.Set)
        s3 = [1, 2, 3]
        s4 = ks.coerce_set(s3)
        self.assertIsInstance(s4, ks.Set)

    def test_coerce_specialized(self):
        x1 = ['e1', 'e2', 'e3']
        x2 = ks.coerce_specialized(x1)
        self.assertIsInstance(x2, ks.Set)
        x3 = [0, 1, 0, 1, 1, 0, 0, 0, 0]
        x4 = ks.coerce_specialized(x3)
        self.assertIsInstance(x4, ks.BinaryVector)
        self.assertIsInstance(x4, ks.IncidenceVector)

    def test_flatten(self):
        self.assertTrue(ks.flatten([1, [2, [3, 4, [5]]]]), [1, 2, 3, 4, 5])

    def test_get_zero_binary_vector(self):
        self.assertTrue(ks.equals(ks.get_zero_binary_vector(1), [0]))
        self.assertTrue(ks.equals(ks.get_zero_binary_vector(2), [0, 0]))
        self.assertTrue(ks.equals(ks.get_zero_binary_vector(3), [0, 0, 0]))

        self.assertFalse(ks.equals(ks.get_zero_binary_vector(2), [0]))
        self.assertFalse(ks.equals(ks.get_zero_binary_vector(3), [0, 0]))
        self.assertFalse(ks.equals(ks.get_zero_binary_vector(1), [0, 0, 0]))

    def test_get_one_binary_vector(self):
        self.assertTrue(ks.equals(ks.get_one_binary_vector(1), [1]))
        self.assertTrue(ks.equals(ks.get_one_binary_vector(2), [1, 1]))
        self.assertTrue(ks.equals(ks.get_one_binary_vector(3), [1, 1, 1]))

        self.assertFalse(ks.equals(ks.get_one_binary_vector(2), [1]))
        self.assertFalse(ks.equals(ks.get_one_binary_vector(3), [1, 1]))
        self.assertFalse(ks.equals(ks.get_one_binary_vector(1), [1, 1, 1]))
