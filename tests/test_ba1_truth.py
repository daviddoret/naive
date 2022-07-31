from unittest import TestCase
import naive


class TestBA1Truth(TestCase):

    def test_ba1_truth(self):
        self.assertEqual('⊤', str(naive.BA1.truth))

        # Truth is a 0-ary function, test it as a formula.
        psi1 = naive.f(naive.BA1.truth)
        print(psi1)
        self.assertEqual('⊤', naive.repr(psi1, naive.RFormats.UTF8))

        # Being a 0-ary function, its argument list is always empty.
        self.assertEqual('[]', str(naive.Core.list_formula_atomic_variables(psi1)))

        # Being a constant, its satisfaction index contains only its constant value.
        sat_i = naive.BA1.satisfaction_index(psi1)
        self.assertEqual('[⊤]', str(sat_i))

