from unittest import TestCase
import src.naive as naive


class TestVariableIndexes(TestCase):
    def test_get_representation(self):
        indexes = naive.VariableIndexes([1, 2, 3])
        #self.assertEqual('₁,₂,₃', indexes.represent(naive.rformats.UTF8))
        #self.assertEqual(r'_{1,2,3}', indexes.represent(naive.rformats.LATEX))
        #self.assertEqual(r'<sub>1,2,3</sub>', indexes.represent(naive.rformats.HTML))
        #self.assertEqual('1,2,3', indexes.represent(naive.rformats.ASCII))
        self.assertEqual('1,2,3', indexes.represent(naive.rformats.UTF8))
        self.assertEqual('1,2,3', indexes.represent(naive.rformats.LATEX))
        self.assertEqual('1,2,3', indexes.represent(naive.rformats.HTML))
        self.assertEqual('1,2,3', indexes.represent(naive.rformats.ASCII))

