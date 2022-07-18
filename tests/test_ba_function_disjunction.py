from unittest import TestCase
import src.naive as naive


class Test(TestCase):
    def test_disjunction_b_b(self):
        print(naive.ba1.lor.represent_declaration())
        self.assertFalse(naive.ba1.lor(naive.ba1.falsum, naive.ba1.falsum))
        self.assertTrue(naive.ba1.lor(naive.ba1.truth, naive.ba1.falsum))
        self.assertTrue(naive.ba1.lor(naive.ba1.falsum, naive.ba1.truth))
        self.assertTrue(naive.ba1.lor(naive.ba1.truth, naive.ba1.truth))
        self.assertTrue(isinstance(naive.ba1.lor.represent(), str))
        self.assertTrue(isinstance(naive.ba1.lor.represent_declaration(), str))
