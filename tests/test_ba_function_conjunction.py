from unittest import TestCase

import rformats
import src.naive as naive


class Test(TestCase):
    def test_2_conjunction(self):
        b1 = naive.ba1.BooleanAtomicVariable(base_name='b', indexes=1)
        b2 = naive.ba1.BooleanAtomicVariable(base_name='b', indexes=2)
        psi1 = naive.ba1.BooleanFormula(
            symbol = naive.ba1.conjunction
            ,arguments = [b1, b2]
        )
        print(psi1)
        self.assertEqual('b₁ ∧ b₂', psi1.represent(rformats.UTF8))
        self.assertEqual('[b₁, b₂]', str(psi1.list_formula_atomic_variables()))
        # worlds = naive.ba1_language.get_boolean_combinations(psi1.arity)
        sat_i = naive.ba1.satisfaction_index(psi1)
        self.assertEqual('[⊥, ⊥, ⊥, ⊤]', str(sat_i))
