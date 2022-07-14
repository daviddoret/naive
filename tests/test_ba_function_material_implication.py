from unittest import TestCase
import src.naive as naive


class Test(TestCase):
    def test_material_implication_b_b(self):
        print(naive.ba.implies.represent_declaration())
        self.assertTrue(naive.ba.implies(naive.ba.falsum, naive.ba.falsum))
        self.assertFalse(naive.ba.implies(naive.ba.truth, naive.ba.falsum))
        self.assertTrue(naive.ba.implies(naive.ba.falsum, naive.ba.truth))
        self.assertTrue(naive.ba.implies(naive.ba.truth, naive.ba.truth))
        self.assertTrue(isinstance(naive.ba.implies.represent(), str))
        self.assertTrue(isinstance(naive.ba.implies.represent_declaration(), str))
