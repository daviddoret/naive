from unittest import TestCase
import src.naive as naive


class TestSuperscriptify(TestCase):
    def test_superscriptify(self):
        self.assertEqual(naive.Repr.superscriptify('1234', naive.RFormats.UTF8), '¹²³⁴')
        self.assertEqual(naive.Repr.superscriptify('1234', naive.RFormats.LATEX), r'^{1234}')
        self.assertEqual(naive.Repr.superscriptify('1234', naive.RFormats.HTML), r'<sup>1234</sup>')
        self.assertEqual(naive.Repr.superscriptify('1234', naive.RFormats.USASCII), '1234')

