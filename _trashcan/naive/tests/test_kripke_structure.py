from unittest import TestCase
import src.naive.kripke_structure as ks
from src.samples import kripke_samples as ks_samples

import logging

logging.basicConfig(level=logging.DEBUG)


class Test(TestCase):

    def test_tt(self):
        m = ks_samples.get_sample_1()
        print(ks.to_text(m))
        self.assertTrue(tl.bv_equal_bv(ks.sat_tt(m, ['s0', 's2']), ['s0', 's2']))
        print(ks.sat_tt(m))
        self.assertTrue(tl.bv_equal_bv(ks.sat_tt(m), m.s))

    def test_labels(self):
        m = ks_samples.get_sample_1()
        self.assertTrue(tl.bv_equal_bv(ks.get_labels_from_state(m, 's0'), ['red']))
        self.assertTrue(
            tl.bv_equal_bv(ks.get_labels_from_state(m, 's1', output_type=ks.IncidenceVector), [True, True, False]))
        self.assertTrue(tl.bv_equal_bv(ks.get_labels_from_state(m, 's2'), ['green', 'blue']))
        self.assertTrue(
            tl.bv_equal_bv(ks.get_labels_from_state(m, 's3', output_type=ks.IncidenceVector), [False, False, True]))
        self.assertTrue(tl.bv_equal_bv(ks.get_labels_from_state(m, 's4'), ['red', 'green', 'blue']))

    def test_get_states_from_label(self):
        m = ks_samples.get_sample_1()
        self.assertTrue(tl.bv_equal_bv(ks.get_states_from_label(m, None, 'red'), ['s0', 's1', 's4']))
        self.assertTrue(tl.bv_equal_bv(ks.get_states_from_label(m, ['s1', 's4'], 'red'), ['s1', 's4']))
        self.assertTrue(tl.bv_equal_bv(ks.get_states_from_label(m, None, 'green', ks.IncidenceVector), [0, 1, 1, 0, 1]))
        self.assertTrue(
            tl.bv_equal_bv(ks.get_states_from_label(m, [1, 1, 1, 0, 0], 'green', ks.IncidenceVector), [0, 1, 1, 0, 0]))
        self.assertTrue(tl.bv_equal_bv(ks.get_states_from_label(m, None, 'blue'), ['s2', 's3', 's4']))

    def test_a(self):
        m = ks_samples.get_sample_1()
        self.assertTrue(tl.bv_equal_bv(ks.sat_a(m, None, 'red'), ['s0', 's1', 's4']))
        self.assertTrue(tl.bv_equal_bv(ks.sat_a(m, ['s1', 's4'], 'red'), ['s1', 's4']))
        self.assertTrue(tl.bv_equal_bv(ks.sat_a(m, None, 'green', ks.IncidenceVector), [0, 1, 1, 0, 1]))
        self.assertTrue(tl.bv_equal_bv(ks.sat_a(m, [1, 1, 1, 0, 0], 'green', ks.IncidenceVector), [0, 1, 1, 0, 0]))
        self.assertTrue(tl.bv_equal_bv(ks.sat_a(m, None, 'blue'), ['s2', 's3', 's4']))

    def test_get_logical_not(self):
        self.assertTrue(tl.bv_equal_bv(ks.get_logical_not([0, 0, 1]), [1, 1, 0]))
        self.assertTrue(tl.bv_equal_bv(ks.get_logical_not([0]), [1]))
        self.assertTrue(tl.bv_equal_bv(ks.get_logical_not([1, 1, 1, 1, 1]), [0, 0, 0, 0, 0]))
        self.assertTrue(tl.bv_equal_bv(ks.get_logical_not([0, 0, 0, 0, 0]), [1, 1, 1, 1, 1]))

    def test_sat_not_phi(self):
        m = ks_samples.get_sample_1()
        self.assertTrue(tl.bv_equal_bv(ks.sat_not_phi(m, None, [1, 1, 1, 0, 0]), ['s3', 's4']))
        self.assertTrue(tl.bv_equal_bv(ks.sat_not_phi(m, None, [0, 0, 0, 0, 0], output_type=ks.IncidenceVector), [1, 1, 1, 1, 1]))
        self.assertTrue(tl.bv_equal_bv(ks.sat_not_phi(m, None, ['s0', 's2', 's4']), ['s1', 's3']))

    def test_sat_phi_or_psi(self):
        m = ks_samples.get_sample_1()
        self.assertTrue(tl.bv_equal_bv(ks.sat_phi_or_psi(m, None, [1, 1, 1, 0, 0], [0, 1, 1, 1, 0]), ['s0', 's1', 's2', 's3']))
        self.assertTrue(tl.bv_equal_bv(ks.sat_phi_or_psi(m, None, [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], output_type=ks.IncidenceVector), [0, 0, 0, 0, 0]))
        self.assertTrue(tl.bv_equal_bv(ks.sat_phi_or_psi(m, None, ['s0', 's2', 's4'], ['s1', 's2', 's4']), ['s0', 's1', 's2', 's4']))

    def test_sat_phi_and_psi(self):
        m = ks_samples.get_sample_1()
        self.assertTrue(tl.bv_equal_bv(ks.sat_phi_and_psi(m, None, [1, 1, 1, 0, 0], [0, 1, 1, 1, 0]), ['s1', 's2']))
        self.assertTrue(tl.bv_equal_bv(ks.sat_phi_and_psi(m, None, [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], output_type=ks.IncidenceVector), [0, 0, 0, 0, 0]))
        self.assertTrue(tl.bv_equal_bv(ks.sat_phi_and_psi(m, None, ['s0', 's2', 's4'], ['s1', 's2', 's4']), ['s2', 's4']))



class TestKripkeStructure(TestCase):
    m = ks_samples.get_sample_1()
    print(ks.to_text(m))
    print(m.lm)


