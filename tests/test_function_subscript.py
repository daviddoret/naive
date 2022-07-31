from unittest import TestCase
import naive


class TestSubscripify(TestCase):
    def test_subscriptify(self):
        self.assertEqual(naive.Repr.subscriptify('1234', naive.RFormats.UTF8), '₁₂₃₄')
        self.assertEqual(naive.Repr.subscriptify('1234', naive.RFormats.LATEX), r'_{1234}')
        self.assertEqual(naive.Repr.subscriptify('1234', naive.RFormats.HTML), r'<sub>1234</sub>')
        self.assertEqual(naive.Repr.subscriptify('1234', naive.RFormats.USASCII), '1234')


