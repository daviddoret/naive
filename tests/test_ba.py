from unittest import TestCase
import src.naive as naive


class Test(TestCase):
    def test_ba(self):
        self.assertEqual(naive.ba.falsum, False)
        self.assertEqual(naive.ba.f, False)
        self.assertEqual(naive.ba.truth, True)
        self.assertEqual(naive.ba.t, True)
        self.assertEqual(naive.ba.falsum.represent(naive.rformats.UTF8), '⊥')
        self.assertEqual(naive.ba.f.represent(naive.rformats.UTF8), '⊥')
        self.assertEqual(naive.ba.truth.represent(naive.rformats.UTF8), '⊤')
        self.assertEqual(naive.ba.t.represent(naive.rformats.UTF8), '⊤')
        self.assertEqual(naive.ba.f, naive.ba.f)
        self.assertEqual(naive.ba.t, naive.ba.t)
        self.assertNotEqual(naive.ba.t, naive.ba.f)
        self.assertNotEqual(naive.ba.f, naive.ba.t)
        self.assertTrue(naive.ba.truth)
        self.assertTrue(naive.ba.t)
        self.assertFalse(naive.ba.falsum)
        self.assertFalse(naive.ba.f)
