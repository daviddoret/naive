from unittest import TestCase
import src.naive as naive


class Test(TestCase):
    def test_subscriptify(self):
        self.assertEqual(naive.subscriptify('1234', naive.rformats.UTF8), '₁₂₃₄')
        self.assertEqual(naive.subscriptify('1234', naive.rformats.LATEX), r'_{1234}')
        self.assertEqual(naive.subscriptify('1234', naive.rformats.HTML), r'<sub>1234</sub>')
        self.assertEqual(naive.subscriptify('1234', naive.rformats.USASCII), '1234')


