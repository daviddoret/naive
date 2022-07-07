from unittest import TestCase
import src.naive as naive


class Test(TestCase):
    def test_flatten(self):
        self.assertEqual(naive.flatten(1, 2, 3), [1, 2, 3])
        self.assertEqual(naive.flatten([1, 2, 3]), [1, 2, 3])
        self.assertEqual(naive.flatten(1), [1])
        self.assertEqual(naive.flatten('a', 'b', ['c', 'd']), ['a', 'b', 'c', 'd'])
