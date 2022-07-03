from unittest import TestCase
import os
import sys
print(sys.path)
import src.naive as naive

class TestVariableBaseName(TestCase):
    def test_1(self):
        self.assertEqual(str(naive.VariableBaseName('a')), 'a')
        self.assertEqual(str(naive.VariableBaseName('x')), 'x')
        self.assertEqual(str(naive.VariableBaseName('Y')), 'Y')
        self.assertEqual(str(naive.VariableBaseName('a1')), 'a')
        self.assertEqual(str(naive.VariableBaseName(' x ')), 'x')
        self.assertEqual(str(naive.VariableBaseName(' 𝛳 ')), '𝛳')
        self.assertEqual(str(naive.VariableBaseName('𝔹')), '𝔹')
        self.assertEqual(str(naive.VariableBaseName('𝟇')), '𝟇')
        self.assertEqual(str(naive.VariableBaseName('𝚺')), '𝚺')
