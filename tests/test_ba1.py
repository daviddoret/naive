from unittest import TestCase
import src.naive as naive


class Test(TestCase):
    def test_ba1(self):
        self.assertEqual(naive.ba1.falsum.represent(naive.rformats.UTF8), '⊥')
        self.assertEqual(naive.ba1.truth.represent(naive.rformats.UTF8), '⊤')
