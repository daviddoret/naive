from unittest import TestCase
import dtmc
import output
import state
import atom
import stochastic_matrix

class TestDTMC(TestCase):

    def test_dtmc_1(self):
        m = dtmc.DTMC(
            s= ['S1', 'S2', 'S3'],
            p= [[0.0, 0.5, 0.5], [0.9, 0.1, 0.0], [0.0, 0.1, 0.9]],
            ap= ['Red', 'Green', 'Blue']
        )
        output.output(m)
        output.output(m.get_steadystate_probability_distribution())
        self.assertTrue(m.check_consistency())

    def test_dtmc_2(self):
        m = dtmc.DTMC(
            s= ['S1', 'S2', 'S3'],
            p= [[.1, .8, .1], [.7, .1, .2], [.3, .3, .4]],
            ap= ['Red', 'Green', 'Blue']
        )
        output.output(m)
        output.output(m.get_steadystate_probability_distribution())
        self.assertTrue(m.check_consistency())

    def test_dtmc_3(self):
        m = dtmc.DTMC(
            s=['s1', 's2', 's3', 's4', 's5', 's6'],
            p=[
                    [0.0, 0.1, 0.9, 0.0, 0.0, 0.0],
                    [0.4, 0.0, 0.6, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.1, 0.1, 0.5, 0.3],
                    [0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.7, 0.3]
                ],
            ap=None)
        output.output(m)
        output.output(m.get_steadystate_probability_distribution())
        self.assertTrue(m.check_consistency())


