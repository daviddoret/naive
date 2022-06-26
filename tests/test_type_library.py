from unittest import TestCase
import naive.type_library as tl


class Test(TestCase):
    def test_flatten(self):
        self.assertEqual(tl.flatten(1), [1])
        self.assertEqual(tl.flatten(1, [2], [[3], [4, 5]]), [1, 2, 3, 4, 5])
        self.assertEqual(tl.flatten(None), [])
