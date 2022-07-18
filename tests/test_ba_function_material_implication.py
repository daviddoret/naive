from unittest import TestCase
import src.naive as naive


class Test(TestCase):
    def test_material_implication_b_b(self):
        print(naive.ba1.implies.represent_declaration())
        self.assertTrue(naive.ba1.implies(naive.ba1.falsum, naive.ba1.falsum))
        self.assertFalse(naive.ba1.implies(naive.ba1.truth, naive.ba1.falsum))
        self.assertTrue(naive.ba1.implies(naive.ba1.falsum, naive.ba1.truth))
        self.assertTrue(naive.ba1.implies(naive.ba1.truth, naive.ba1.truth))
        self.assertTrue(isinstance(naive.ba1.implies.represent(), str))
        self.assertTrue(isinstance(naive.ba1.implies.represent_declaration(), str))
