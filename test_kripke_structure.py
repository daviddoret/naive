from unittest import TestCase
import kripke_structure as ks
import kripke_samples as ks_samples
import numpy as np
import logging
import collections.abc as abc

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
        m1 = [[1, 1, 1], [1, 0, 1]]
        m2 = ks.coerce_binary_matrix(m1)
        self.assertIsInstance(m2, ks.BinaryMatrix)
        ks.coerce_binary_matrix([[1, 2, 3], [4, 5]])

    def test_coerce_binary_square_matrix(self):
        m1 = [[1, 1, 1], [1, 0, 1], [0, 0, 0]]
        m2 = ks.coerce_binary_square_matrix(m1)
        self.assertIsInstance(m2, ks.BinarySquareMatrix)
        with self.assertRaises(IndexError):
            ks.coerce_binary_square_matrix([[1, 2, 3], [4, 5]])

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
        self.assertEqual(s1, s2)
        s3 = [1, 2, 3]
        s4 = ks.coerce_set(s3)
        self.assertEqual(['1', '2', '3'], s4)

    def test_coerce_specialized(self):
        x1 = ['e1', 'e2', 'e3']
        x2 = ks.coerce_set_or_iv(x1)
        self.assertIsInstance(x2, abc.Iterable)
        self.assertTrue(all(isinstance(y, str) for y in x2))
        x3 = [0, 1, 0, 1, 1, 0, 0, 0, 0]
        x4 = ks.coerce_set_or_iv(x3)
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

    def test_get_set_from_range(self):
        self.assertTrue(ks.equals(ks.get_set_from_range(3), ['e0', 'e1', 'e2']))
        self.assertTrue(ks.equals(ks.get_set_from_range(3, 'x', 1), ['x1', 'x2', 'x3']))
        self.assertFalse(ks.equals(ks.get_set_from_range(3, 'x', 1), ['x0', 'x1', 'x2']))

    def test_get_state_set(self):
        print(ks.get_state_set(3))
        self.assertTrue(ks.equals(ks.get_state_set(3), ['s0', 's1', 's2']))
        self.assertFalse(ks.equals(ks.get_state_set(3), ['s1', 's2', 's3']))

    def test_get_incidence_vector(self):
        superset = ks.get_state_set(12)
        subset = ['s02', 's04', 's05']
        subset_iv = ks.get_incidence_vector(subset, superset)
        correct_iv = [0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0]
        self.assertTrue(ks.equals(subset_iv, correct_iv))
        subset_iv_from_iv = ks.get_incidence_vector(correct_iv, superset)
        self.assertTrue(ks.equals(subset_iv_from_iv, correct_iv))

    def test_cardinality(self):
        s = ks.coerce_set(['a', 'b', 'c', 'd', 'e'])
        self.assertEqual(ks.cardinality(s), 5)
        v = ks.coerce_binary_vector([1, 0, 1, 0, 0])
        self.assertEqual(ks.cardinality(v), 5)
        iv = ks.coerce_incidence_vector(v, s)
        self.assertEqual(ks.cardinality(iv), 5)

    def test_coerce_subset(self):
        s = ['a', 'b', 'c', 'd', 'e']
        self.assertEqual(ks.coerce_subset(['a', 'b'], s), ['a', 'b'])
        self.assertEqual(ks.coerce_subset(['a', 'z', 'b'], s), ['a', 'b'])

    def test_vmin(self):
        v1 = [0, 1, 0, 1, 0, 0, 1, 1]
        v2 = [1, 1, 0, 0, 0, 0, 1, 1]
        v3 = ks.vmin(v1, v2)
        self.assertTrue(ks.equals(v3, [0, 1, 0, 0, 0, 0, 1, 1]))

    def test_tt(self):
        m = ks_samples.get_sample_1()
        print(ks.to_text(m))


class TestKripkeStructure(TestCase):
    m = ks_samples.get_sample_1()
    print(ks.to_text(m))
    print(m.lm)
