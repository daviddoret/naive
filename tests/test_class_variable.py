from unittest import TestCase
import src.naive as naive


class TestVariable(TestCase):
    def test_get_representation_1(self):
        base = naive.VariableBaseName(naive.glyphs.standard_x_lowercase)
        indexes = naive.VariableIndexes([1, 2, 3])
        variable = naive.Variable(base, indexes)
        self.assertEqual('v₁,₂,₃', variable.represent(naive.rformats.UTF8))
        self.assertEqual('v_{1,2,3}', variable.represent(naive.rformats.LATEX))
        self.assertEqual('v<sub>1,2,3</sub>', variable.represent(naive.rformats.HTML))
        self.assertEqual('v1,2,3', variable.represent(naive.rformats.ASCII))

    def test_get_representation_2(self):
        self.assertEqual('v', naive.Variable('v').represent(naive.rformats.UTF8))
        self.assertEqual('y₁', naive.Variable('y', 1).represent(naive.rformats.UTF8))
        self.assertEqual('z₂,₃', naive.Variable('z', [2, 3]).represent(naive.rformats.UTF8))
