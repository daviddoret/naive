from unittest import TestCase
import src.naive as naive


class Test(TestCase):
    def test_negation_b_b(self):
        self.assertTrue(naive.ba.negation_b_b(naive.ba.falsum))
        self.assertFalse(naive.ba.negation_b_b(naive.ba.truth))
