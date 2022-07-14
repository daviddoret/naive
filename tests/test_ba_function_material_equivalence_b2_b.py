from unittest import TestCase
import src.naive as naive


class Test(TestCase):
    def test_material_equivalence_b_b(self):
        print(naive.ba.iif_b2_b.represent_declaration())
        self.assertTrue(naive.ba.iif_b2_b(naive.ba.falsum, naive.ba.falsum))
        self.assertFalse(naive.ba.iif_b2_b(naive.ba.truth, naive.ba.falsum))
        self.assertFalse(naive.ba.iif_b2_b(naive.ba.falsum, naive.ba.truth))
        self.assertTrue(naive.ba.iif_b2_b(naive.ba.truth, naive.ba.truth))
        self.assertTrue(isinstance(naive.ba.iif_b2_b.represent(), str))
        self.assertTrue(isinstance(naive.ba.iif_b2_b.represent_declaration(), str))
