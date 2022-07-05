from unittest import TestCase
import src.naive as naive


class TestBinaryValue(TestCase):
    def test_init(self):
        b0 = naive.BinaryConstant(False)
        self.assertEqual(str(b0), naive.settings.BINARY_VALUE_0_NOTATION)
        b1 = naive.BinaryConstant(True)
        self.assertEqual(str(b1), naive.settings.BINARY_VALUE_1_NOTATION)
        x = naive.Variable(naive.BinaryConstant, 'x', None, b0)
        self.assertEqual(b0, x.value)
        print(x)
        y = naive.Variable(naive.BinaryConstant, 'y', None, b1)
        self.assertEqual(b1, y.value)
        print(y)
        z = naive.Variable(naive.BinaryConstant, 'z', None, 0)
        self.assertEqual(b0, z.value)
        a = naive.Variable(naive.BinaryConstant, 'a', None, 1)
        self.assertEqual(b1, a.value)