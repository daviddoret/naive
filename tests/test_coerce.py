from unittest import TestCase
import src.naive as naive


class Test(TestCase):
    def test_coerce(self):
        self.assertEqual(naive.coerce(5, int), 5)
        self.assertEqual(naive.coerce('hello world', str), 'hello world')


