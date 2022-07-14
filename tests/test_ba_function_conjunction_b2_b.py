from unittest import TestCase
import src.naive as naive


class Test(TestCase):
    def test_conjunction_b_b(self):
        self.assertFalse(naive.ba.and_b2_b(naive.ba.falsum, naive.ba.falsum))
        self.assertFalse(naive.ba.and_b2_b(naive.ba.truth, naive.ba.falsum))
        self.assertFalse(naive.ba.and_b2_b(naive.ba.falsum, naive.ba.truth))
        self.assertTrue(naive.ba.and_b2_b(naive.ba.truth, naive.ba.truth))
        self.assertTrue(isinstance(naive.ba.and_b2_b.represent(), str))
        self.assertTrue(isinstance(naive.ba.and_b2_b.represent_declaration(), str))
