from unittest import TestCase
import src.naive as naive


class Test(TestCase):
    def test_material_equivalence_b_b(self):
        print(naive.iif_b2_b.represent_declaration())
        self.assertTrue(naive.iif_b2_b(naive.bv.falsum, naive.bv.falsum))
        self.assertFalse(naive.iif_b2_b(naive.bv.truth, naive.bv.falsum))
        self.assertFalse(naive.iif_b2_b(naive.bv.falsum, naive.bv.truth))
        self.assertTrue(naive.iif_b2_b(naive.bv.truth, naive.bv.truth))
        self.assertTrue(isinstance(naive.iif_b2_b.represent(), str))
        self.assertTrue(isinstance(naive.iif_b2_b.represent_declaration(), str))
