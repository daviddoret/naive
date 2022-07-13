from unittest import TestCase
import src.naive as naive


class Test(TestCase):
    def test_disjunction_b_b(self):
        print(naive.or_b2_b.represent_declaration())
        self.assertFalse(naive.or_b2_b(naive.bv.falsum, naive.bv.falsum))
        self.assertTrue(naive.or_b2_b(naive.bv.truth, naive.bv.falsum))
        self.assertTrue(naive.or_b2_b(naive.bv.falsum, naive.bv.truth))
        self.assertTrue(naive.or_b2_b(naive.bv.truth, naive.bv.truth))
        self.assertTrue(isinstance(naive.or_b2_b.represent(), str))
        self.assertTrue(isinstance(naive.or_b2_b.represent_declaration(), str))
