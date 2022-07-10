from unittest import TestCase

import rformats
import src.naive as naive


class TestVariableBase(TestCase):
    def test_init(self):
        base = naive.VariableBase(naive.glyphs.mathbb_n_uppercase)
        self.assertEqual('ℕ', base.represent(rformats.UTF8))
        self.assertEqual(r'\mathbb{N}', base.represent(rformats.LATEX))
        self.assertEqual('&Nopf;', base.represent(rformats.HTML))
        self.assertEqual('N', base.represent(rformats.ASCII))

