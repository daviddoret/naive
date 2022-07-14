from unittest import TestCase
import src.naive as naive


class Test(TestCase):
    def test_conjunction(self):
        self.assertFalse(naive.ba.land(naive.ba.falsum, naive.ba.falsum))
        self.assertFalse(naive.ba.land(naive.ba.truth, naive.ba.falsum))
        self.assertFalse(naive.ba.land(naive.ba.falsum, naive.ba.truth))
        self.assertTrue(naive.ba.land(naive.ba.truth, naive.ba.truth))
        self.assertTrue(isinstance(naive.ba.land.represent(), str))
        self.assertTrue(isinstance(naive.ba.land.represent_declaration(), str))
