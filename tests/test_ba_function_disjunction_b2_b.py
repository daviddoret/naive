from unittest import TestCase
import src.naive as naive


class Test(TestCase):
    def test_disjunction_b_b(self):
        print(naive.ba.or_b2_b.represent_declaration())
        self.assertFalse(naive.ba.or_b2_b(naive.ba.falsum, naive.ba.falsum))
        self.assertTrue(naive.ba.or_b2_b(naive.ba.truth, naive.ba.falsum))
        self.assertTrue(naive.ba.or_b2_b(naive.ba.falsum, naive.ba.truth))
        self.assertTrue(naive.ba.or_b2_b(naive.ba.truth, naive.ba.truth))
        self.assertTrue(isinstance(naive.ba.or_b2_b.represent(), str))
        self.assertTrue(isinstance(naive.ba.or_b2_b.represent_declaration(), str))
