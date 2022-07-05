from unittest import TestCase
import src.naive as naive


class TestVariable(TestCase):
    def test_1(self):
        x = naive.Variable(naive.NN0C, 'x')
        print(x)


