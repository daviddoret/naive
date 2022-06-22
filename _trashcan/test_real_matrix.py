from unittest import TestCase
import real_matrix
import output


class TestRealMatrix(TestCase):
    def test_real_matrix_1(self):
        m1 = real_matrix.RealMatrix([[1, 0.1, 0], [1, 1, 0], [1, 3724, 1]])
        self.assertEqual(m1[2,1], 3724)
        self.assertTrue(m1.check_consistency())
        output.output_math(m1.to_latex_math())
        print(m1.to_bool_numpy_array())
        print(m1.to_int_numpy_array())
        print(m1.to_float_numpy_array())
        m2 = m1.copy()
        print(m2[1, 1])
        self.assertEqual(m2[1, 1], 1)
        output.output_math(m2.to_latex_math())
        self.assertEqual(m1, m2)
        print(real_matrix.RealMatrix(m2))
        print(real_matrix.RealMatrix([[0, 0.1], [1.1, 7.77777]]))
        m_bad = real_matrix.RealMatrix([[1, 2, 3], [4, 5, 6]])
        self.assertFalse(m_bad.check_consistency())