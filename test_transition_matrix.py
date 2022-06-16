from unittest import TestCase
import transition_matrix
import samples


class TestTransitionMatrix(TestCase):
    def test_get_immediate_successors_iv(self):
        t = samples.get_transition_matrix_sample_1()
        self.assertEqual(t.get_immediate_successors_iv(0), [0, 1, 0, 0, 0])
        self.assertEqual(t.get_immediate_successors_iv(1), [0, 0, 1, 1, 0])
        self.assertEqual(t.get_immediate_successors_iv(2), [0, 0, 0, 0, 1])
        self.assertEqual(t.get_immediate_successors_iv(3), [0, 1, 1, 1, 0])
        self.assertEqual(t.get_immediate_successors_iv(4), [0, 0, 0, 0, 1])

    def test_get_s_path_set_iv(self):
        t = samples.get_transition_matrix_sample_1()
        print(t.get_s_path_set_iv(0))
