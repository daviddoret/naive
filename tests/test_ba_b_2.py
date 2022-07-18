from unittest import TestCase
import src.naive as naive


class Test(TestCase):
    def test_ba_b_2(self):
        self.assertEqual(naive.ba1.b_2.dimensions, 2)
