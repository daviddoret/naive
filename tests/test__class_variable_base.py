from unittest import TestCase

import rformats
import src.naive as naive


class TestVariableBase(TestCase):
    def test_init(self):
        base = naive.VariableBase(naive.glyphs.mathbb_n_uppercase)
        self.assertEqual('ℕ', base.get_representation(rformats.UTF8))
        self.assertEqual(r'\mathbb{N}', base.get_representation(rformats.LATEX))
        self.assertEqual('&Nopf;', base.get_representation(rformats.HTML))
        self.assertEqual('N', base.get_representation(rformats.ASCII))

