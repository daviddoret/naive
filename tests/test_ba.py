from unittest import TestCase
import src.naive as naive


class Test(TestCase):
    def test_ba(self):
        self.assertEqual(naive.ba1.falsum, False)
        self.assertEqual(naive.ba1.f, False)
        self.assertEqual(naive.ba1.truth, True)
        self.assertEqual(naive.ba1.t, True)
        self.assertEqual(naive.ba1.falsum.represent(naive.rformats.UTF8), '⊥')
        self.assertEqual(naive.ba1.f.represent(naive.rformats.UTF8), '⊥')
        self.assertEqual(naive.ba1.truth.represent(naive.rformats.UTF8), '⊤')
        self.assertEqual(naive.ba1.t.represent(naive.rformats.UTF8), '⊤')
        self.assertEqual(naive.ba1.f, naive.ba1.f)
        self.assertEqual(naive.ba1.t, naive.ba1.t)
        self.assertNotEqual(naive.ba1.t, naive.ba1.f)
        self.assertNotEqual(naive.ba1.f, naive.ba1.t)
        self.assertTrue(naive.ba1.truth)
        self.assertTrue(naive.ba1.t)
        self.assertFalse(naive.ba1.falsum)
        self.assertFalse(naive.ba1.f)
