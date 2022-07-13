from unittest import TestCase
import src.naive as naive


class TestVariable(TestCase):
    def test_get_representation_1(self):
        base = naive.VariableBaseName(naive.glyphs.standard_x_lowercase)
        indexes = naive.VariableIndexes(1, 2, 3)
        variable = naive.Variable(base, indexes)
        self.assertEqual(variable.represent(naive.rformats.UTF8), 'x₁,₂,₃')
        self.assertEqual(variable.represent(naive.rformats.LATEX), 'x_{1,2,3}')
        self.assertEqual(variable.represent(naive.rformats.HTML), 'x<sub>1,2,3</sub>')
        self.assertEqual(variable.represent(naive.rformats.ASCII), 'x1,2,3')

    def test_get_representation_2(self):
        self.assertEqual(naive.Variable('x').represent(naive.rformats.UTF8), 'x')
        self.assertEqual(naive.Variable('y', 1).represent(naive.rformats.UTF8), 'y₁')
        self.assertEqual(naive.Variable('z', 2, 3).represent(naive.rformats.UTF8), 'z₂,₃')
