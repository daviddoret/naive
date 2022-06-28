from unittest import TestCase
import logging
import naive.type_library as tl
import naive.binary_algebra as ba
import naive.set_algebra as sa

logging.basicConfig(level=logging.DEBUG)


class Test(TestCase):

    def test_equal(self):
        s1 = ['e1', 'e2', 'e3']
        s2 = tl.coerce_set(s1)
        self.assertTrue(sa.equal(s1, s2))
        s3 = ['e1', 'e2', 'e4']
        self.assertFalse(sa.equal(s1, s3))
        s4 = ['e1', 'e2']
        self.assertFalse(sa.equal(s1, s4))

    def test_coerce_set(self):
        s1 = ['e1', 'e2', 'e3']
        s2 = tl.coerce_set(s1)
        self.assertEqual(s1, s2)
        s3 = [1, 2, 3]
        s4 = tl.coerce_set(s3)
        self.assertEqual(['1', '2', '3'], s4)

    def test_coerce_subset_or_iv(self):
        s = sa.get_state_set(9)
        s_prime_set = ['s1', 's2', 's3']
        coerced_s_prime_set = tl.coerce_subset_or_iv(s_prime_set, s)
        self.assertTrue(tl.is_instance(coerced_s_prime_set, tl.Set))
        self.assertTrue(tl.is_instance(coerced_s_prime_set, tl.StateSet))
        self.assertTrue(all(isinstance(y, str) for y in coerced_s_prime_set))
        self.assertTrue(sa.equal(s_prime_set, coerced_s_prime_set))
        s_prime_iv = [0, 1, 0, 1, 1, 0, 0, 0, 0]
        coerced_s_prime_iv = tl.coerce_subset_or_iv(s_prime_iv, s)
        self.assertIsInstance(coerced_s_prime_iv, tl.IncidenceVector)
        self.assertTrue(tl.is_instance(coerced_s_prime_iv, tl.IncidenceVector))
        self.assertTrue(tl.binary_vector_equal(s_prime_iv, coerced_s_prime_iv))

    def test_get_set_from_range(self):
        self.assertTrue(sa.equal(sa.get_set_from_range(3), ['e0', 'e1', 'e2']))
        self.assertTrue(sa.equal(sa.get_set_from_range(3, 'x', 1), ['x1', 'x2', 'x3']))
        self.assertFalse(sa.equal(sa.get_set_from_range(3, 'x', 1), ['x0', 'x1', 'x2']))

    def test_get_state_set(self):
        print(sa.get_state_set(3))
        self.assertTrue(sa.equal(sa.get_state_set(3), ['s0', 's1', 's2']))
        self.assertFalse(sa.equal(sa.get_state_set(3), ['s1', 's2', 's3']))

    def test_get_set(self):
        s = sa.get_state_set(12)
        s_prime_iv = [0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0]
        s_prime_set = sa.get_set(s_prime_iv, s)
        print(f's_prime_set: {s_prime_set}')
        correct_set = ['s02', 's04', 's05']
        self.assertTrue(sa.equal(s_prime_set, correct_set))
        correct_set_set = sa.get_set(correct_set, s)
        self.assertTrue(sa.equal(correct_set_set, correct_set))

    def test_get_incidence_vector(self):
        s = sa.get_state_set(12)
        s_prime_set = ['s02', 's04', 's05']
        s_prime_iv = sa.get_incidence_vector(s_prime_set, s)
        correct_iv = [0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0]
        self.assertTrue(tl.binary_vector_equal(s_prime_iv, correct_iv))
        correct_iv_iv = sa.get_incidence_vector(correct_iv, s)
        self.assertTrue(tl.binary_vector_equal(correct_iv_iv, correct_iv))

    def test_cardinality(self):
        s = tl.coerce_set(['a', 'b', 'c', 'd', 'e'])
        self.assertEqual(sa.set_cardinality(s), 5)
        v = tl.coerce_binary_vector([1, 0, 1, 0, 0])
        self.assertEqual(sa.set_cardinality(v), 5)
        iv = tl.coerce_incidence_vector(v, s)
        self.assertEqual(sa.set_cardinality(iv), 5)

    def test_coerce_subset(self):
        s = ['a', 'b', 'c', 'd', 'e']
        self.assertEqual(tl.coerce_subset(['a', 'b'], s), ['a', 'b'])
        self.assertEqual(tl.coerce_subset(['a', 'z', 'b'], s), ['a', 'b'])


