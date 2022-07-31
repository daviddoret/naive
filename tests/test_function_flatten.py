from unittest import TestCase
import naive


class TestFlatten(TestCase):
    def test_flatten(self):
        self.assertEqual(naive.Utils.flatten(1, 2, 3), [1, 2, 3])
        self.assertEqual(naive.Utils.flatten([1, 2, 3]), [1, 2, 3])
        self.assertEqual(naive.Utils.flatten(1), [1])
        self.assertEqual(naive.Utils.flatten('a', 'b', ['c', 'd']), ['a', 'b', 'c', 'd'])
