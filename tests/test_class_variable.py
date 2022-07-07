from unittest import TestCase

import rformats
import src.naive as naive


class TestVariable(TestCase):
    def test_get_representation(self):
        base = naive.VariableBase(naive.glyphs.standard_x_lowercase)
        indexes = naive.VariableIndexes(1, 2, 3)
        variable = naive.Variable(base, indexes)
        self.assertEqual(variable.get_representation(rformats.UTF8), 'x₁,₂,₃')
        self.assertEqual(variable.get_representation(rformats.LATEX), 'x_{1,2,3}')
        self.assertEqual(variable.get_representation(rformats.HTML), 'x<sub>1,2,3</sub>')
        self.assertEqual(variable.get_representation(rformats.ASCII), 'x1,2,3')
