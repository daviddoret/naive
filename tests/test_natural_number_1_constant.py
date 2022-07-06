from unittest import TestCase
import src.naive as naive


class TestNaturalNumber1(TestCase):
    def test_1(self):
        self.assertEqual(int(naive.NN1(1)), 1)
        self.assertEqual(int(naive.NN1(5)), 5)
        self.assertEqual(int(naive.NN1(123456)), 123456)

