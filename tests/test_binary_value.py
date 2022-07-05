from unittest import TestCase
import src.naive as naive


class TestBinaryValue(TestCase):
    def test_init(self):
        b0 = naive.BC(False)
        self.assertEqual(str(b0), naive.settings.BINARY_VALUE_0_NOTATION)
        b1 = naive.BC(True)
        self.assertEqual(str(b1), naive.settings.BINARY_VALUE_1_NOTATION)
        x = naive.Variable(naive.domains.b, 'x', None, b0)
        self.assertEqual(b0, x.value)
        print(x)
        y = naive.Variable(naive.domains.b, 'y', None, b1)
        self.assertEqual(b1, y.value)
        print(y)
        z = naive.Variable(naive.domains.b, 'z', None, naive.BC(0))
        self.assertEqual(b0, z.value)
        a = naive.Variable(naive.domains.b, 'a', None, naive.BC(1))
        self.assertEqual(b1, a.value)