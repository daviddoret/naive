from unittest import TestCase
import src.naive as naive


class Test(TestCase):
    def test_conjunction(self):
        self.assertFalse(naive.ba1.land(naive.ba1.falsum, naive.ba1.falsum))
        self.assertFalse(naive.ba1.land(naive.ba1.truth, naive.ba1.falsum))
        self.assertFalse(naive.ba1.land(naive.ba1.falsum, naive.ba1.truth))
        self.assertTrue(naive.ba1.land(naive.ba1.truth, naive.ba1.truth))
        self.assertTrue(isinstance(naive.ba1.land.represent(), str))
        self.assertTrue(isinstance(naive.ba1.land.represent_declaration(), str))
