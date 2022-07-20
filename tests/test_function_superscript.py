from unittest import TestCase
import src.naive as naive


class Test(TestCase):
    def test_superscriptify(self):
        self.assertEqual(naive.superscriptify('1234', naive.rformats.UTF8), '¹²³⁴')
        self.assertEqual(naive.superscriptify('1234', naive.rformats.LATEX), r'^{1234}')
        self.assertEqual(naive.superscriptify('1234', naive.rformats.HTML), r'<sup>1234</sup>')
        self.assertEqual(naive.superscriptify('1234', naive.rformats.USASCII), '1234')

