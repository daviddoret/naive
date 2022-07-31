from unittest import TestCase
import naive

class TestBA1Disjunction(TestCase):
    def test_1(self):
        naive.set_unique_scope()
        b1 = naive.av(codomain=naive.BA1.b, base_name='b', indexes=1)
        b2 = naive.av(codomain=naive.BA1.b, base_name='b', indexes=2)
        psi1 = naive.f(naive.BA1.disjunction, b1, b2)
        self.assertEqual('(b₁ ∨ b₂)', naive.repr(psi1, naive.RFormats.UTF8))
        self.assertEqual('[b₁, b₂]', str(naive.Core.list_formula_atomic_variables(psi1)))
        # worlds = naive.ba1_language.get_boolean_combinations(psi1.arity)
        sat_i = naive.BA1.satisfaction_index(psi1)
        self.assertEqual('[⊥, ⊤, ⊤, ⊤]', str(sat_i))