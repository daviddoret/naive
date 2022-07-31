from unittest import TestCase

import naive


class TestSA1ElementOf(TestCase):
    def test_sa1_element_of_1(self):
        # Bypass the formula construction to test directly the system algorithm.
        naive.set_unique_scope()
        v1 = [2, 5, 8]
        s1 = naive.SA1.declare_finite_set(base_name='S', indexes=1, elements=[1, 2, 3])
        s2 = naive.SA1.declare_finite_set(base_name='S', indexes=2, elements=[2, 3, 4])
        s3 = naive.SA1.declare_finite_set(base_name='S', indexes=3, elements=[5, 6, 7])
        v2 = [s1, s2, s3]
        v3 = naive.SA1.element_of_algorithm(v1, v2)
        self.assertEqual('[⊤, ⊥, ⊥]', str(v3))

    def test_sa1_element_of_2(self):
        # TODO: COME BACK AND FINALIZE THIS TEST ONCE WE HAVE ABSTRACT FINITE SET TO WORK WITH
        b1 = naive.av(codomain=naive.BA1.b, base_name='b', indexes=1)
        S1 = naive.av(codomain=naive.BA1.bn, base_name='S', indexes=1)
        psi1 = naive.f(naive.SA1.element_of, v1, v2)
        self.assertEqual('(v₁ ∈ b₂)', naive.repr(psi1, naive.RFormats.UTF8))
        self.assertEqual('[b₁, b₂]', str(naive.Core.list_formula_atomic_variables(psi1)))
        # worlds = naive.ba1_language.get_boolean_combinations(psi1.arity)
        sat_i = naive.BA1.satisfaction_index(psi1)
        self.assertEqual('[⊥, ⊥, ⊥, ⊤]', str(sat_i))