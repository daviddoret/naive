from unittest import TestCase
import src.naive as naive


class TestNaturalNumber0(TestCase):
    def test_1(self):
        self.assertEqual(int(naive.NN0(1)), 1)
        self.assertEqual(int(naive.NN0(5)), 5)
        self.assertEqual(int(naive.NN0(123456)), 123456)

