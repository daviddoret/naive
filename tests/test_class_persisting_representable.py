from unittest import TestCase
import src.naive as naive


class TestRepresentable(TestCase):
    def test_get_representation(self):
        s1 = naive.PersistingRepresentable(utf8='ℕ', latex=r'\mathbb{N}', html='&Nopf;', usascii='N')
        self.assertEqual(s1.represent(naive.rformats.UTF8), 'ℕ')
        self.assertEqual(s1.represent(naive.rformats.LATEX), r'\mathbb{N}')
        self.assertEqual(s1.represent(naive.rformats.HTML), '&Nopf;')
        self.assertEqual(s1.represent(naive.rformats.USASCII), 'N')

    def test_init(self):
        s1 = naive.PersistingRepresentable(naive.glyphs.mathbb_n_uppercase)
        self.assertEqual(s1.represent(naive.rformats.UTF8), 'ℕ')
        self.assertEqual(s1.represent(naive.rformats.LATEX), r'\mathbb{N}')
        self.assertEqual(s1.represent(naive.rformats.HTML), '&Nopf;')
        self.assertEqual(s1.represent(naive.rformats.USASCII), 'N')

        s2 = naive.PersistingRepresentable(utf8='ℕ', latex=r'\mathbb{N}', html='&Nopf;', usascii='N')
        self.assertEqual(s2.represent(naive.rformats.UTF8), 'ℕ')
        self.assertEqual(s2.represent(naive.rformats.LATEX), r'\mathbb{N}')
        self.assertEqual(s2.represent(naive.rformats.HTML), '&Nopf;')
        self.assertEqual(s2.represent(naive.rformats.USASCII), 'N')
