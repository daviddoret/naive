from unittest import TestCase
import naive.binary_algebra as ba
import logging

logging.basicConfig(level=logging.DEBUG)


class Test(TestCase):

    def test_eq(self):
        o1 = [0, 1, 0, 1, 1, 0, 0, 0, 0]
        o2 = [0, 1, 0, 1, 0, 0, 0, 0, 0]
        o3 = [0, 1, 0, 1, 1, 0, 0, 0, 0]
        self.assertTrue(ba.equal(o1, o3))
        self.assertFalse(ba.equal(o1, o2))
        self.assertFalse(ba.equal(o2, o3))

    def test_get_zero_binary_vector(self):
        self.assertTrue(ba.equal(ba.get_zero_binary_vector(1), [0]))
        self.assertTrue(ba.equal(ba.get_zero_binary_vector(2), [0, 0]))
        self.assertTrue(ba.equal(ba.get_zero_binary_vector(3), [0, 0, 0]))

        self.assertFalse(ba.equal(ba.get_zero_binary_vector(2), [0]))
        self.assertFalse(ba.equal(ba.get_zero_binary_vector(3), [0, 0]))
        self.assertFalse(ba.equal(ba.get_zero_binary_vector(1), [0, 0, 0]))

    def test_get_one_binary_vector(self):
        self.assertTrue(ba.equal(ba.get_one_binary_vector(1), [1]))
        self.assertTrue(ba.equal(ba.get_one_binary_vector(2), [1, 1]))
        self.assertTrue(ba.equal(ba.get_one_binary_vector(3), [1, 1, 1]))

        self.assertFalse(ba.equal(ba.get_one_binary_vector(2), [1]))
        self.assertFalse(ba.equal(ba.get_one_binary_vector(3), [1, 1]))
        self.assertFalse(ba.equal(ba.get_one_binary_vector(1), [1, 1, 1]))

    def test_get_minima(self):
        v1 = [0, 1, 0, 1, 0, 0, 1, 1]
        v2 = [1, 1, 0, 0, 0, 0, 1, 1]
        v3 = ba.get_minima(v1, v2)
        self.assertTrue(ba.equal(v3, [0, 1, 0, 0, 0, 0, 1, 1]))

    def test_get_maxima(self):
        v1 = [0, 1, 0, 1, 0, 0, 1, 1]
        v2 = [1, 1, 0, 0, 0, 0, 1, 1]
        v3 = ba.get_maxima(v1, v2)
        self.assertTrue(ba.equal(v3, [1, 1, 0, 1, 0, 0, 1, 1]))

    def test_get_logical_not(self):
        self.assertTrue(ba.equal(ba.get_logical_not([0, 0, 1]), [1, 1, 0]))
        self.assertTrue(ba.equal(ba.get_logical_not([0]), [1]))
        self.assertTrue(ba.equal(ba.get_logical_not([1, 1, 1, 1, 1]), [0, 0, 0, 0, 0]))
        self.assertTrue(ba.equal(ba.get_logical_not([0, 0, 0, 0, 0]), [1, 1, 1, 1, 1]))


