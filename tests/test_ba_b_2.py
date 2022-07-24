from unittest import TestCase
import naive


class Test(TestCase):
    def test_ba_b2(self):
        self.assertEqual(naive.b2.dimensions, 2)
