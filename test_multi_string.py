from unittest import TestCase
import mstr


class TestMultiFormatString(TestCase):
    def test_multi_string_1(self):
        s1 = mstr.MStr('hello world')
        self.assertEqual(s1, 'hello world')
        print(s1.latex_math)
        self.assertEqual(s1.latex_math, f'\\text{{hello world}}')
        s2 = mstr.MStr('x2', f'x^2')
        self.assertEqual(s2, 'x2')
        self.assertEqual(s2.latex_math, 'x^2')
        self.assertNotEqual(s1, s2)
        self.assertNotEqual(s1.unicode, s2.unicode)
        self.assertNotEqual(s1.latex_math, s2.latex_math)



