from unittest import TestCase
import src.naive as naive


class Test(TestCase):
    def test_negation_b_b(self):
        self.assertTrue(naive.negation_b_b(naive.bv.falsum))
        self.assertFalse(naive.negation_b_b(naive.bv.truth))
