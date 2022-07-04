from unittest import TestCase
import src.naive as naive


class TestBinaryValue(TestCase):
    def test_init(self):
        b0 = naive.BinaryValue(False)
        self.assertEqual(str(b0), naive.settings.BINARY_VALUE_0_NOTATION)
        b1 = naive.BinaryValue(True)
        self.assertEqual(str(b1), naive.settings.BINARY_VALUE_1_NOTATION)
        x = naive.Variable(naive.BinaryValue, 'x', None, b0)
        self.assertEqual(b0, x.value)
        print(x)
        y = naive.Variable(naive.BinaryValue, 'y', None, b1)
        self.assertEqual(b1, y.value)
        print(y)
        z = naive.Variable(naive.BinaryValue, 'z', None, 0)
        self.assertEqual(b0, z.value)
        a = naive.Variable(naive.BinaryValue, 'a', None, 1)
        self.assertEqual(b1, a.value)