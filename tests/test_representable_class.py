from unittest import TestCase

import rformats
import src.naive as naive


class TestRepresentable(TestCase):
    def test_get_representation(self):
        s1 = naive.Representable(utf8='ℕ', latex=r'\mathbb{N}', html='&Nopf;', ascii=b'N')
        self.assertEqual(s1.get_representation(rformats.UTF8), 'ℕ')
        self.assertEqual(s1.get_representation(rformats.LATEX), r'\mathbb{N}')
        self.assertEqual(s1.get_representation(rformats.HTML), '&Nopf;')
        self.assertEqual(s1.get_representation(rformats.ASCII), b'N')

    def test_init(self):
        s1 = naive.Representable(naive.glyphs.mathbb_n_uppercase)
        self.assertEqual(s1.get_representation(rformats.UTF8), 'ℕ')
        self.assertEqual(s1.get_representation(rformats.LATEX), r'\mathbb{N}')
        self.assertEqual(s1.get_representation(rformats.HTML), '&Nopf;')
        self.assertEqual(s1.get_representation(rformats.ASCII), b'N')

        s2 = naive.Representable(utf8='ℕ', latex=r'\mathbb{N}', html='&Nopf;', ascii=b'N')
        self.assertEqual(s2.get_representation(rformats.UTF8), 'ℕ')
        self.assertEqual(s2.get_representation(rformats.LATEX), r'\mathbb{N}')
        self.assertEqual(s2.get_representation(rformats.HTML), '&Nopf;')
        self.assertEqual(s2.get_representation(rformats.ASCII), b'N')
