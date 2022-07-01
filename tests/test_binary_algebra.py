from unittest import TestCase
import src.naive.type_library as tl
import src.naive.binary_algebra as ba
import logging

logging.basicConfig(level=logging.DEBUG)


class Test(TestCase):


    def test_get_zero_binary_vector(self):
        self.assertTrue(tl.bv_equal_bv(ba.get_zero_binary_vector(1), [0]))
        self.assertTrue(tl.bv_equal_bv(ba.get_zero_binary_vector(2), [0, 0]))
        self.assertTrue(tl.bv_equal_bv(ba.get_zero_binary_vector(3), [0, 0, 0]))

        self.assertFalse(tl.bv_equal_bv(ba.get_zero_binary_vector(2), [0]))
        self.assertFalse(tl.bv_equal_bv(ba.get_zero_binary_vector(3), [0, 0]))
        self.assertFalse(tl.bv_equal_bv(ba.get_zero_binary_vector(1), [0, 0, 0]))

    def test_get_one_binary_vector(self):
        self.assertTrue(tl.bv_equal_bv(ba.get_one_binary_vector(1), [1]))
        self.assertTrue(tl.bv_equal_bv(ba.get_one_binary_vector(2), [1, 1]))
        self.assertTrue(tl.bv_equal_bv(ba.get_one_binary_vector(3), [1, 1, 1]))

        self.assertFalse(tl.bv_equal_bv(ba.get_one_binary_vector(2), [1]))
        self.assertFalse(tl.bv_equal_bv(ba.get_one_binary_vector(3), [1, 1]))
        self.assertFalse(tl.bv_equal_bv(ba.get_one_binary_vector(1), [1, 1, 1]))

    def test_get_minima(self):
        v1 = [0, 1, 0, 1, 0, 0, 1, 1]
        v2 = [1, 1, 0, 0, 0, 0, 1, 1]
        v3 = ba.get_minima(v1, v2)
        self.assertTrue(tl.bv_equal_bv(v3, [0, 1, 0, 0, 0, 0, 1, 1]))

    def test_get_maxima(self):
        v1 = [0, 1, 0, 1, 0, 0, 1, 1]
        v2 = [1, 1, 0, 0, 0, 0, 1, 1]
        v3 = ba.get_maxima(v1, v2)
        self.assertTrue(tl.bv_equal_bv(v3, [1, 1, 0, 1, 0, 0, 1, 1]))

    def test_get_logical_not(self):
        v = ba.get_logical_not([])
        t = tl.is_instance(v, tl.BinaryVector)
        self.assertEqual(tl.BV([]), ba.get_logical_not([]))
        self.assertEqual(tl.BV([1, 1, 0]), ba.get_logical_not([0, 0, 1]))
        self.assertEqual(tl.BV([0, 0, 1]), ba.get_logical_not([1, 1, 0]))
        self.assertEqual(tl.BV([1, 1, 1]), ba.get_logical_not([0, 0, 0]))
        self.assertEqual(tl.BV([0, 0, 0]), ba.get_logical_not([1, 1, 1]))
        self.assertEqual(tl.BV([0]), ba.get_logical_not([1]))
        self.assertEqual(tl.BV([1]), ba.get_logical_not([0]))
        self.assertEqual(tl.BV([0, 0, 1, 1, 1, 0]), ba.get_logical_not([1, 1, 0, 0, 0, 1]))
        self.assertEqual(tl.BV([1, 1, 0, 0, 0, 1]), ba.get_logical_not([0, 0, 1, 1, 1, 0]))
        # Note that the not Python operator cannot be overridden
        # internally, Python will call not(first) != second
        # for this reason, we must expressly use the binary_vector_equal function
        # and cannot use the native equality
        # Source: https://stackoverflow.com/questions/39754808/overriding-not-operator-in-python
        self.assertFalse(tl.bv_equal_bv(tl.BV([]), None))
        self.assertFalse(tl.bv_equal_bv(tl.BV([0]), None))
        self.assertFalse(tl.bv_equal_bv(tl.BV([0, 1]), None))



