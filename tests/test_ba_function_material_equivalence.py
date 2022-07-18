from unittest import TestCase
import src.naive as naive


class Test(TestCase):
    def test_material_equivalence_b_b(self):
        print(naive.ba1.iif.represent_declaration())
        self.assertTrue(naive.ba1.iif(naive.ba1.falsum, naive.ba1.falsum))
        self.assertFalse(naive.ba1.iif(naive.ba1.truth, naive.ba1.falsum))
        self.assertFalse(naive.ba1.iif(naive.ba1.falsum, naive.ba1.truth))
        self.assertTrue(naive.ba1.iif(naive.ba1.truth, naive.ba1.truth))
        self.assertTrue(isinstance(naive.ba1.iif.represent(), str))
        self.assertTrue(isinstance(naive.ba1.iif.represent_declaration(), str))
