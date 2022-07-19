from unittest import TestCase
import src.naive as naive


class Test(TestCase):

    def test_1_negation(self):
        b1 = naive.ba1.BooleanAtomicVariable(base_name='b', indexes=1)
        psi1 = naive.ba1.BooleanFormula(
            symbol = naive.ba1.negation
            ,arguments = [b1]
        )
        print(psi1)
        self.assertEqual('¬b₁', psi1.represent(naive.rformats.UTF8))
        self.assertEqual('[b₁]', str(psi1.list_atomic_variables()))
        # worlds = naive.ba1.get_boolean_combinations(psi1.arity)
        sat_i = naive.ba1.satisfaction_index(psi1)
        self.assertEqual('[⊤, ⊥]', str(sat_i))