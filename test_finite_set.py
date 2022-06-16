from unittest import TestCase

import binary_vector
import finite_set


class TestFiniteSet(TestCase):
    def test_finite_set_1(self):
        s1 = finite_set.FiniteSet(['a','a','b','c'])
        print(s1)
        s2 = finite_set.FiniteSet(['a','c','b','b','b'])
        print(s2)
        self.assertEqual(s1, s2)

    def test_finite_set_2(self):
        s1 = finite_set.FiniteSet(['z','a','a','b','c'])
        self.assertEqual(s1[0], 'a')
        self.assertEqual(s1[1], 'b')
        self.assertEqual(s1[2], 'c')
        self.assertEqual(s1[3], 'z')

    def test_finite_set_3(self):
        s1 = finite_set.FiniteSet(['z','a','a','b','c'])
        s2 = finite_set.FiniteSet(['b', 'b', 'c'])
        i = s1.get_incidence_vector(s2)
        self.assertEqual(i[0], 0)
        self.assertEqual(i[1], 1)
        self.assertEqual(i[2], 1)
        self.assertEqual(i[3], 0)

    def test_finite_set_4(self):
        s1 = finite_set.FiniteSet(5)
        self.assertEqual(s1, finite_set.FiniteSet(['e0', 'e1', 'e2', 'e3', 'e4']))
        iv = binary_vector.BinaryVector([0, 1, 1, 0, 1])
        subset = s1.get_subset(iv)
        self.assertEqual(subset, finite_set.FiniteSet(['e1', 'e2', 'e4']))
