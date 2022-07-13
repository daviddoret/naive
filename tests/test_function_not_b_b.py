from unittest import TestCase
import src.naive as naive


class Test(TestCase):
    def test_not_b_b(self):
        self.assertTrue(naive.not_b_b(naive.bv.falsum))
        self.assertFalse(naive.not_b_b(naive.bv.truth))
