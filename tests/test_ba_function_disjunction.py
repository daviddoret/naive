from unittest import TestCase
import src.naive as naive


class Test(TestCase):
    def test_disjunction_b_b(self):
        print(naive.ba.lor.represent_declaration())
        self.assertFalse(naive.ba.lor(naive.ba.falsum, naive.ba.falsum))
        self.assertTrue(naive.ba.lor(naive.ba.truth, naive.ba.falsum))
        self.assertTrue(naive.ba.lor(naive.ba.falsum, naive.ba.truth))
        self.assertTrue(naive.ba.lor(naive.ba.truth, naive.ba.truth))
        self.assertTrue(isinstance(naive.ba.lor.represent(), str))
        self.assertTrue(isinstance(naive.ba.lor.represent_declaration(), str))
