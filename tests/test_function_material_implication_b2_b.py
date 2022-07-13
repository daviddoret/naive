from unittest import TestCase
import src.naive as naive


class Test(TestCase):
    def test_material_implication_b_b(self):
        print(naive.implies_b2_b.represent_declaration())
        self.assertTrue(naive.implies_b2_b(naive.bv.falsum, naive.bv.falsum))
        self.assertFalse(naive.implies_b2_b(naive.bv.truth, naive.bv.falsum))
        self.assertTrue(naive.implies_b2_b(naive.bv.falsum, naive.bv.truth))
        self.assertTrue(naive.implies_b2_b(naive.bv.truth, naive.bv.truth))
        self.assertTrue(isinstance(naive.implies_b2_b.represent(), str))
        self.assertTrue(isinstance(naive.implies_b2_b.represent_declaration(), str))
