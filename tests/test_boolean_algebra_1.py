from unittest import TestCase
import src.naive as naive


class TestBooleanAtomicVariable(TestCase):
    def test_1(self):
        b1 = naive.ba1.BooleanAtomicVariable(base_name='b', indexes=1)
        print(b1)
        self.assertEqual('b₁', b1.represent(naive.rformats.UTF8))


class TestBooleanFormula(TestCase):








    def test_4_complex(self):
        b1 = naive.ba1.BooleanAtomicVariable(base_name='b', indexes=1)
        b2 = naive.ba1.BooleanAtomicVariable(base_name='b', indexes=2)
        b3 = naive.ba1.BooleanAtomicVariable(base_name='b', indexes=3)
        psi1 = naive.ba1.BooleanFormula(
            symbol = naive.ba1.conjunction
            ,arguments = [b1, b2]
        )
        psi2 = naive.ba1.BooleanFormula(
            symbol = naive.ba1.disjunction
            ,arguments = [b3, b1]
        )
        psi3 = naive.ba1.BooleanFormula(
            symbol = naive.ba1.conjunction
            ,arguments = [psi1, psi2]
        )
        print(psi3.list_atomic_variables())
        self.assertEqual('[b₁, b₂, b₃]', str(psi3.list_atomic_variables()))
        worlds = naive.ba1.get_boolean_combinations(psi3.arity)
        print(worlds)
        sat_i = naive.ba1.satisfaction_index(psi3)
        print(sat_i)
        self.assertEqual('[⊥, ⊥, ⊥, ⊤, ⊥, ⊥, ⊥, ⊤]', str(sat_i))