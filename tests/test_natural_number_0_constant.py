from unittest import TestCase
import src.naive as naive


class TestNaturalNumber0(TestCase):
    def test_1(self):
        self.assertEqual(int(naive.NN0C(1)), 1)
        self.assertEqual(int(naive.NN0C(5)), 5)
        self.assertEqual(int(naive.NN0C(123456)), 123456)

