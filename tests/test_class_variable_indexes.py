from unittest import TestCase
import src.naive as naive


class TestVariableIndexes(TestCase):
    def test_get_representation(self):
        indexes = naive.VariableIndexes(1, 2, 3)
        self.assertEqual(indexes.represent(naive.rformats.UTF8), '₁,₂,₃')
        self.assertEqual(indexes.represent(naive.rformats.LATEX), r'_{1,2,3}')
        self.assertEqual(indexes.represent(naive.rformats.HTML), r'<sub>1,2,3</sub>')
        self.assertEqual(indexes.represent(naive.rformats.ASCII), '1,2,3')