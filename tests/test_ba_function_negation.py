from unittest import TestCase
import src.naive as naive


class Test(TestCase):
    def test_negation_b_b(self):
        n = naive.ba1.negation(naive.ba1.falsum)
        self.assertTrue(naive.ba1.negation(naive.ba1.falsum))
        self.assertFalse(naive.ba1.negation(naive.ba1.truth))
