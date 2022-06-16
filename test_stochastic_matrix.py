from unittest import TestCase
import stochastic_matrix
import output


class TestStochasticMatrix(TestCase):
    def test_stochastic_matrix_1(self):
        p = stochastic_matrix.StochasticMatrix([[.9, .1, 0], [1, .1, 0], [0, .2, .8]])
        self.assertFalse(p.check_consistency())
        p[1,1] = 0
        print(p)
        self.assertTrue(p.check_consistency())
        self.assertEqual(sum(p[0,]), 1)
        output.output_math(p.to_latex_math())
        p2 = p.copy()
        print(p2[1, 1])
        p2[1, 1] = 0
        output.output_math(p2.to_latex_math())
        print(p == p2)
        print(stochastic_matrix.StochasticMatrix(p2))
        print(p)
