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
        with self.assertRaises(ValueError):
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

    def test_coerce_subset_or_iv(self):
        s = ks.get_state_set(9)
        s_prime_set = ['e1', 'e2', 'e3']
        coerced_s_prime_set = ks.coerce_subset_or_iv(s_prime_set, s)
        self.assertTrue(ks.is_instance(coerced_s_prime_set, ks.Set))
        self.assertTrue(ks.is_instance(coerced_s_prime_set, ks.StateSet))
        self.assertTrue(all(isinstance(y, str) for y in coerced_s_prime_set))
        self.assertTrue(ks.equals(s_prime_set, coerced_s_prime_set, s))
        s_prime_iv = [0, 1, 0, 1, 1, 0, 0, 0, 0]
        coerced_s_prime_iv = ks.coerce_subset_or_iv(s_prime_iv, s)
        self.assertIsInstance(coerced_s_prime_iv, ks.IncidenceVector)
        self.assertTrue(ks.is_instance(coerced_s_prime_iv, ks.IncidenceVector))
        self.assertTrue(ks.equals(s_prime_iv, coerced_s_prime_iv))

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

    def test_get_set(self):
        s = ks.get_state_set(12)
        s_prime_iv = [0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0]
        s_prime_set = ks.get_set(s_prime_iv, s)
        print(f's_prime_set: {s_prime_set}')
        correct_set = ['s02', 's04', 's05']
        self.assertTrue(ks.equals(s_prime_set, correct_set))
        correct_set_set = ks.get_set(correct_set, s)
        self.assertTrue(ks.equals(correct_set_set, correct_set))

    def test_get_incidence_vector(self):
        s = ks.get_state_set(12)
        s_prime_set = ['s02', 's04', 's05']
        s_prime_iv = ks.get_incidence_vector(s_prime_set, s)
        correct_iv = [0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0]
        self.assertTrue(ks.equals(s_prime_iv, correct_iv))
        correct_iv_iv = ks.get_incidence_vector(correct_iv, s)
        self.assertTrue(ks.equals(correct_iv_iv, correct_iv))

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
        self.assertTrue(ks.equals(ks.sat_tt(m, ['s0', 's2']), ['s0', 's2']))
        print(ks.sat_tt(m))
        self.assertTrue(ks.equals(ks.sat_tt(m), m.s))

    def test_labels(self):
        m = ks_samples.get_sample_1()
        self.assertTrue(ks.equals(ks.get_labels_from_state(m, 's0'), ['red']))
        self.assertTrue(
            ks.equals(ks.get_labels_from_state(m, 's1', output_type=ks.IncidenceVector), [True, True, False]))
        self.assertTrue(ks.equals(ks.get_labels_from_state(m, 's2'), ['green', 'blue']))
        self.assertTrue(
            ks.equals(ks.get_labels_from_state(m, 's3', output_type=ks.IncidenceVector), [False, False, True]))
        self.assertTrue(ks.equals(ks.get_labels_from_state(m, 's4'), ['red', 'green', 'blue']))

    def test_get_states_from_label(self):
        m = ks_samples.get_sample_1()
        self.assertTrue(ks.equals(ks.get_states_from_label(m, None, 'red'), ['s0', 's1', 's4']))
        self.assertTrue(ks.equals(ks.get_states_from_label(m, ['s1', 's4'], 'red'), ['s1', 's4']))
        self.assertTrue(ks.equals(ks.get_states_from_label(m, None, 'green', ks.IncidenceVector), [0, 1, 1, 0, 1]))
        self.assertTrue(
            ks.equals(ks.get_states_from_label(m, [1, 1, 1, 0, 0], 'green', ks.IncidenceVector), [0, 1, 1, 0, 0]))
        self.assertTrue(ks.equals(ks.get_states_from_label(m, None, 'blue'), ['s2', 's3', 's4']))

    def test_a(self):
        m = ks_samples.get_sample_1()
        self.assertTrue(ks.equals(ks.sat_a(m, None, 'red'), ['s0', 's1', 's4']))
        self.assertTrue(ks.equals(ks.sat_a(m, ['s1', 's4'], 'red'), ['s1', 's4']))
        self.assertTrue(ks.equals(ks.sat_a(m, None, 'green', ks.IncidenceVector), [0, 1, 1, 0, 1]))
        self.assertTrue(ks.equals(ks.sat_a(m, [1, 1, 1, 0, 0], 'green', ks.IncidenceVector), [0, 1, 1, 0, 0]))
        self.assertTrue(ks.equals(ks.sat_a(m, None, 'blue'), ['s2', 's3', 's4']))

    def test_get_logical_not(self):
        self.assertTrue(ks.equals(ks.get_logical_not([0, 0, 1]), [1, 1, 0]))
        self.assertTrue(ks.equals(ks.get_logical_not([0]), [1]))
        self.assertTrue(ks.equals(ks.get_logical_not([1, 1, 1, 1, 1]), [0, 0, 0, 0, 0]))
        self.assertTrue(ks.equals(ks.get_logical_not([0, 0, 0, 0, 0]), [1, 1, 1, 1, 1]))


class TestKripkeStructure(TestCase):
    m = ks_samples.get_sample_1()
    print(ks.to_text(m))
    print(m.lm)


