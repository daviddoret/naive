from unittest import TestCase
import logging
import naive.type_library as tl
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
        s_prime_set = ['e1', 'e2', 'e3']
        coerced_s_prime_set = sa.coerce_subset_or_iv(s_prime_set, s)
        self.assertTrue(sa.is_instance(coerced_s_prime_set, sa.Set))
        self.assertTrue(sa.is_instance(coerced_s_prime_set, sa.StateSet))
        self.assertTrue(all(isinstance(y, str) for y in coerced_s_prime_set))
        self.assertTrue(sa.equal(s_prime_set, coerced_s_prime_set, s))
        s_prime_iv = [0, 1, 0, 1, 1, 0, 0, 0, 0]
        coerced_s_prime_iv = sa.coerce_subset_or_iv(s_prime_iv, s)
        self.assertIsInstance(coerced_s_prime_iv, sa.IncidenceVector)
        self.assertTrue(sa.is_instance(coerced_s_prime_iv, sa.IncidenceVector))
        self.assertTrue(sa.equal(s_prime_iv, coerced_s_prime_iv))

    def test_get_set_from_range(self):
        self.assertTrue(ks.equal(ks.get_set_from_range(3), ['e0', 'e1', 'e2']))
        self.assertTrue(ks.equal(ks.get_set_from_range(3, 'x', 1), ['x1', 'x2', 'x3']))
        self.assertFalse(ks.equal(ks.get_set_from_range(3, 'x', 1), ['x0', 'x1', 'x2']))

    def test_get_state_set(self):
        print(ks.get_state_set(3))
        self.assertTrue(ks.equal(ks.get_state_set(3), ['s0', 's1', 's2']))
        self.assertFalse(ks.equal(ks.get_state_set(3), ['s1', 's2', 's3']))

    def test_get_set(self):
        s = ks.get_state_set(12)
        s_prime_iv = [0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0]
        s_prime_set = ks.get_set(s_prime_iv, s)
        print(f's_prime_set: {s_prime_set}')
        correct_set = ['s02', 's04', 's05']
        self.assertTrue(ks.equal(s_prime_set, correct_set))
        correct_set_set = ks.get_set(correct_set, s)
        self.assertTrue(ks.equal(correct_set_set, correct_set))

    def test_get_incidence_vector(self):
        s = ks.get_state_set(12)
        s_prime_set = ['s02', 's04', 's05']
        s_prime_iv = ks.get_incidence_vector(s_prime_set, s)
        correct_iv = [0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0]
        self.assertTrue(ks.equal(s_prime_iv, correct_iv))
        correct_iv_iv = ks.get_incidence_vector(correct_iv, s)
        self.assertTrue(ks.equal(correct_iv_iv, correct_iv))

    def test_cardinality(self):
        s = ks.coerce_set(['a', 'b', 'c', 'd', 'e'])
        self.assertEqual(ks.set_cardinality(s), 5)
        v = ks.coerce_binary_vector([1, 0, 1, 0, 0])
        self.assertEqual(ks.set_cardinality(v), 5)
        iv = ks.coerce_incidence_vector(v, s)
        self.assertEqual(ks.set_cardinality(iv), 5)

    def test_coerce_subset(self):
        s = ['a', 'b', 'c', 'd', 'e']
        self.assertEqual(ks.coerce_subset(['a', 'b'], s), ['a', 'b'])
        self.assertEqual(ks.coerce_subset(['a', 'z', 'b'], s), ['a', 'b'])


