from unittest import TestCase
import src.naive as naive


class Test(TestCase):
    def test_bv(self):
        self.assertEqual(naive.bv.falsum, False)
        self.assertEqual(naive.bv.f, False)
        self.assertEqual(naive.bv.truth, True)
        self.assertEqual(naive.bv.t, True)
        self.assertEqual(naive.bv.falsum.represent(naive.rformats.UTF8), '⊥')
        self.assertEqual(naive.bv.f.represent(naive.rformats.UTF8), '⊥')
        self.assertEqual(naive.bv.truth.represent(naive.rformats.UTF8), '⊤')
        self.assertEqual(naive.bv.t.represent(naive.rformats.UTF8), '⊤')
        self.assertEqual(naive.bv.f, naive.bv.f)
        self.assertEqual(naive.bv.t, naive.bv.t)
        self.assertNotEqual(naive.bv.t, naive.bv.f)
        self.assertNotEqual(naive.bv.f, naive.bv.t)
        self.assertTrue(naive.bv.truth)
        self.assertTrue(naive.bv.t)
        self.assertFalse(naive.bv.falsum)
        self.assertFalse(naive.bv.f)
