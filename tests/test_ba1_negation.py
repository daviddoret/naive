from unittest import TestCase
import naive


class TestBA1Negation(TestCase):

    def test_ba1_negation(self):
        b1 = naive.av(codomain=naive.BA1.b, base_name='b', indexes=1)
        psi1 = naive.f(naive.BA1.negation, b1)
        print(psi1)
        self.assertEqual('¬b₁', naive.repr(psi1, naive.RFormats.UTF8))
        self.assertEqual('[b₁]', str(naive.Core.list_formula_atomic_variables(psi1)))
        # worlds = naive.ba1_language.get_boolean_combinations(psi1.arity)
        sat_i = naive.BA1.satisfaction_index(psi1)
        self.assertEqual('[⊤, ⊥]', str(sat_i))

