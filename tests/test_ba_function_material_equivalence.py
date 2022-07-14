from unittest import TestCase
import src.naive as naive


class Test(TestCase):
    def test_material_equivalence_b_b(self):
        print(naive.ba.iif.represent_declaration())
        self.assertTrue(naive.ba.iif(naive.ba.falsum, naive.ba.falsum))
        self.assertFalse(naive.ba.iif(naive.ba.truth, naive.ba.falsum))
        self.assertFalse(naive.ba.iif(naive.ba.falsum, naive.ba.truth))
        self.assertTrue(naive.ba.iif(naive.ba.truth, naive.ba.truth))
        self.assertTrue(isinstance(naive.ba.iif.represent(), str))
        self.assertTrue(isinstance(naive.ba.iif.represent_declaration(), str))
