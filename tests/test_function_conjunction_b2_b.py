from unittest import TestCase
import src.naive as naive


class Test(TestCase):
    def test_conjunction_b_b(self):
        self.assertFalse(naive.and_b2_b(naive.bv.falsum, naive.bv.falsum))
        self.assertFalse(naive.and_b2_b(naive.bv.truth, naive.bv.falsum))
        self.assertFalse(naive.and_b2_b(naive.bv.falsum, naive.bv.truth))
        self.assertTrue(naive.and_b2_b(naive.bv.truth, naive.bv.truth))
        self.assertTrue(isinstance(naive.and_b2_b.represent(), str))
        self.assertTrue(isinstance(naive.and_b2_b.represent_declaration(), str))
