from unittest import TestCase
import src.naive as naive


class Test(TestCase):
    def test_negation_b_b(self):
        self.assertTrue(naive.ba.negation(naive.ba.falsum))
        self.assertFalse(naive.ba.negation(naive.ba.truth))
