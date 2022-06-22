from unittest import TestCase

import const
import output
import samples
import lts
import state


class TestLTS(TestCase):

    def test_lts_1(self):
        output.set_verbosity_limit(const.NONE)
        m = samples.get_lts_sample_1()

        self.assertTrue(m.check_consistency())
        self.assertEqual(m.get_s_set_from_a(0), ['Fox'])
        self.assertEqual(m.get_s_set_from_a(1), ['Apple', 'Banana'])
        self.assertEqual(m.get_s_iv_from_a(0), [False, False, True])
        self.assertEqual(m.get_s_iv_from_a(1), [True, True, False])

        self.assertTrue(m.check_consistency())
        self.assertEqual(m.get_a_from_s(0), ['Vegetal'])
        self.assertEqual(m.get_a_from_s(1), ['Vegetal'])
        self.assertEqual(m.get_a_from_s(2), ['Animal'])
        self.assertEqual(m.get_a_iv_from_s(0), [False, True])
        self.assertEqual(m.get_a_iv_from_s(1), [False, True])
        self.assertEqual(m.get_a_iv_from_s(2), [True, False])

    def test_lts_state_formula_1(self):
        output.set_verbosity_limit(const.NONE)
        m = samples.get_lts_sample_1()

        # TT
        phi1 = lts.TT()
        self.assertTrue(lts.Sat(m, 'Apple', phi1).check_s())

        # A
        phi2 = lts.A('Vegetal')
        self.assertTrue(lts.Sat(m, 'Apple', phi2).check_s())

        phi3 = lts.A('Animal')
        self.assertFalse(lts.Sat(m, 'Apple', phi3).check_s())

        # Not
        phi4 = lts.Not(phi2)
        self.assertFalse(lts.Sat(m, 'Apple', phi4).check_s())

        phi5 = lts.Not(phi3)
        self.assertTrue(lts.Sat(m, 'Apple', phi5).check_s())

        phi6 = lts.Not(phi1)
        self.assertFalse(lts.Sat(m, 'Apple', phi6).check_s())

        phi7 = lts.Not(phi5)
        self.assertFalse(lts.Sat(m, 'Apple', phi7).check_s())

        # And
        phi8 = lts.And(phi2, phi5)
        self.assertTrue(lts.Sat(m, 'Apple', phi8).check_s())

        phi9 = lts.And(phi4, phi6)
        self.assertFalse(lts.Sat(m, 'Apple', phi9).check_s())

        # Or
        phi10 = lts.Or('Apple', phi5, phi7)
        self.assertTrue(lts.Sat(m, 'Apple', phi10).check_s())

        phi11 = lts.Or('Apple', phi9, phi7)
        self.assertFalse(lts.Sat(m, 'Apple', phi11).check_s())

    def test_get_s_path_set(self):
        output.set_verbosity_limit(const.DETAILED)

        m = samples.get_lts_sample_2()
        self.assertEqual(m.get_s_path_set('s0'), ['s0', 's1', 's2', 's3', 's4'])
        self.assertEqual(m.get_s_path_set('s1'), ['s1', 's2', 's3', 's4'])
        self.assertEqual(m.get_s_path_set('s2'), ['s2', 's4'])
        self.assertEqual(m.get_s_path_set('s3'), ['s1', 's2', 's3', 's4'])
        self.assertEqual(m.get_s_path_set('s4'), ['s4'])


class Test(TestCase):
    def test_tt(self):
        m = samples.get_lts_sample_2()
        phi = lts.TT()
        self.assertEqual(lts.tt(m, output_type=state.IV), [1, 1, 1, 1, 1])
        self.assertEqual(lts.tt(m, [1, 0, 1, 0, 0], output_type=state.IV), [1, 0, 1, 0, 0])
        self.assertEqual(lts.tt(m), ['s0', 's1', 's2', 's3', 's4'])
        self.assertEqual(lts.tt(m, ['s0', 's2']), ['s0', 's2'])

class TestTT(TestCase):
    def test_get_sat_iv(self):
        m = samples.get_lts_sample_2()
        phi = lts.TT()
        self.assertEqual(phi.compute(m), [1, 1, 1, 1, 1])
        self.assertEqual(phi.compute(m, [1, 0, 1, 0, 0]), [1, 0, 1, 0, 0])
        self.assertEqual(phi.compute(m), ['s0', 's1', 's2', 's3', 's4'])
        self.assertEqual(phi.compute(m, ['s0', 's2']), ['s0', 's2'])
        sat = lts.Sat(m, ['s0', 's3'], phi)
        output.output2(const.RESULT, sat.to_multistring())
        self.assertTrue(sat.check_s())


class TestA(TestCase):
    def test_get_sat_iv(self):
        m = samples.get_lts_sample_2()
        fa0 = lts.A('a0')
        fa1 = lts.A('a1')
        fa2 = lts.A('a2')
        fa3 = lts.A('a3')
        self.assertEqual(fa0.compute(m), [1, 1, 1, 1, 0])
        self.assertEqual(fa1.compute(m), [1, 1, 1, 0, 1])
        self.assertEqual(fa2.compute(m), [0, 1, 1, 1, 0])
        self.assertEqual(fa3.compute(m), [0, 0, 0, 0, 0])

    def test_get_sat_set(self):
        m = samples.get_lts_sample_2()
        fa0 = lts.A('a0')
        fa1 = lts.A('a1')
        fa2 = lts.A('a2')
        fa3 = lts.A('a3')
        self.assertEqual(fa0.compute(m), ['s0', 's1', 's2', 's3'])
        self.assertEqual(fa1.compute(m), ['s0', 's1', 's2', 's4'])
        self.assertEqual(fa2.compute(m), ['s1', 's2', 's3'])
        self.assertEqual(fa3.compute(m), [])

    def test_sat(self):
        m = samples.get_lts_sample_2()
        fa0 = lts.A('a0')
        fa1 = lts.A('a1')
        fa2 = lts.A('a2')
        fa3 = lts.A('a3')
        self.assertTrue(lts.Sat(m, ['s0', 's1', 's2', 's3'], fa0).check_s())
        self.assertTrue(lts.Sat(m, ['s0', 's1', 's2', 's4'], fa1).check_s())
        self.assertTrue(lts.Sat(m, ['s1', 's2', 's3'], fa2).check_s())
        self.assertTrue(lts.Sat(m, [], fa3).check_s())


class TestNot(TestCase):
    def test_get_sat_iv(self):
        m = samples.get_lts_sample_2()
        phi0 = lts.Not(m, lts.A(m, 'a0'))
        phi1 = lts.Not(m, lts.A(m, 'a1'))
        phi2 = lts.Not(m, lts.A(m, 'a2'))
        phi3 = lts.Not(m, lts.A(m, 'a3'))
        self.assertEqual(phi0.compute(m), [0, 0, 0, 0, 1])
        self.assertEqual(phi1.compute(m), [0, 0, 0, 1, 0])
        self.assertEqual(phi2.compute(m), [1, 0, 0, 0, 1])
        self.assertEqual(phi3.compute(m), [1, 1, 1, 1, 1])

    def test_get_sat_set(self):
        m = samples.get_lts_sample_2()
        phi0 = lts.Not(m, lts.A(m, 'a0'))
        phi1 = lts.Not(m, lts.A(m, 'a1'))
        phi2 = lts.Not(m, lts.A(m, 'a2'))
        phi3 = lts.Not(m, lts.A(m, 'a3'))
        self.assertEqual(phi0.compute(m), ['s4'])
        self.assertEqual(phi1.compute(m), ['s3'])
        self.assertEqual(phi2.compute(m), ['s0', 's4'])
        self.assertEqual(phi3.compute(m), ['s0', 's1', 's2', 's3', 's4'])

    def test_sat(self):
        m = samples.get_lts_sample_2()
        phi0 = lts.Not(lts.A('a0'))
        phi1 = lts.Not(lts.A('a1'))
        phi2 = lts.Not(lts.A('a2'))
        phi3 = lts.Not(lts.A('a3'))
        self.assertTrue(lts.Sat(m, ['s4'], phi0).check_s())
        self.assertTrue(lts.Sat(m, ['s3'], phi1).check_s())
        self.assertTrue(lts.Sat(m, ['s0', 's4'], phi2).check_s())
        self.assertTrue(lts.Sat(m, ['s0', 's1', 's2', 's3', 's4'], phi3).check_s())


class TestOr(TestCase):
    def test_get_sat_iv(self):
        m = samples.get_lts_sample_2()
        phi1 = lts.A('a0')
        psi1 = lts.A('a1')
        phi2 = lts.Or(phi1, psi1)
        self.assertEqual(phi2.compute(), [1, 1, 1, 1, 1])

    def test_get_sat_set(self):
        output.set_verbosity_limit(const.DETAILED)
        m = samples.get_lts_sample_2()
        phi1 = lts.A('a0')
        psi1 = lts.A('a1')
        phi2 = lts.Or(phi1, psi1)
        self.assertEqual(phi2.compute(m), ['s0', 's1', 's2', 's3', 's4'])
        sat1 = lts.Sat(phi2)
        print(sat1)

    def test_sat(self):
        m = samples.get_lts_sample_2()
        phi1 = lts.A('a0')
        psi1 = lts.A('a1')
        phi2 = lts.Or(phi1, psi1)
        self.assertTrue(lts.Sat(m, ['s0', 's1', 's2', 's3', 's4'], phi2).check_s())


class TestAnd(TestCase):
    def test_compute(self):
        m = samples.get_lts_sample_2()
        phi1 = lts.A('a1')
        psi1 = lts.A('a2')
        phi2 = lts.And(phi1, psi1)
        self.assertEqual(phi2.compute(), [0, 1, 1, 0, 0])

    def test_get_sat_set(self):
        m = samples.get_lts_sample_2()
        phi1 = lts.A('a1')
        psi1 = lts.A('a2')
        phi2 = lts.And(phi1, psi1)
        self.assertEqual(phi2.compute(), ['s1', 's2'])

    def test_sat(self):
        m = samples.get_lts_sample_2()
        phi1 = lts.A('a1')
        psi1 = lts.A('a2')
        phi2 = lts.And(phi1, psi1)
        self.assertTrue(lts.Sat(m, ['s1', 's2'], phi2).check_s())



