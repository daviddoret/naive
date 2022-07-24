from unittest import TestCase

import rformats
import src.naive as naive


class Test(TestCase):

    def test_basic_atomic_variable_declaration(self):
        b1 = naive.core.av(naive.ba1.b, base_name='b', indexes=1)
        self.assertEqual('b₁', b1.represent(naive.rformats.UTF8))

    def test_representation_of_truth_and_falsum(self):
        self.assertEqual(naive.ba1.truth.represent(naive.rformats.UTF8), '⊤')
        self.assertEqual(naive.ba1.falsum.represent(naive.rformats.UTF8), '⊥')

    def test_b_variable_declaration(self):
        x = naive.core.av(naive.ba1.b, 'x')
        self.assertEqual('x', x.represent(naive.rformats.UTF8))
        y = naive.core.av(naive.ba1.b, 'y')
        self.assertEqual('y', y.represent(naive.rformats.UTF8))
        z = naive.core.av(naive.ba1.b, 'z')
        self.assertEqual('z', z.represent(naive.rformats.UTF8))

    def test_representation_of_domains_and_b_tuple_domains(self):

        self.assertEqual('𝔹', naive.ba1.b.represent(naive.rformats.UTF8))
        self.assertEqual('𝔹²', naive.ba1.b2.represent(naive.rformats.UTF8))

        self.assertEqual('𝔹', naive.ba1.get_bn_domain(1).represent(naive.rformats.UTF8))
        self.assertEqual('𝔹²', naive.ba1.get_bn_domain(2).represent(naive.rformats.UTF8))
        self.assertEqual('𝔹³', naive.ba1.get_bn_domain(3).represent(naive.rformats.UTF8))
        self.assertEqual('𝔹⁴', naive.ba1.get_bn_domain(4).represent(naive.rformats.UTF8))
        self.assertEqual('𝔹²³⁴', naive.ba1.get_bn_domain(234).represent(naive.rformats.UTF8))

    def test_formula_representation(self):
        phi1 = naive.core.f(naive.ba1.truth)
        self.assertEqual('⊤', phi1.represent(naive.rformats.UTF8))

        phi2 = naive.core.f(naive.ba1.falsum)
        self.assertEqual('⊥', phi2.represent(naive.rformats.UTF8))

        phi3 = naive.core.f(naive.ba1.negation, phi1)
        self.assertEqual('¬⊤', phi3.represent(naive.rformats.UTF8))

        phi4 = naive.core.f(naive.ba1.conjunction, phi1, phi2)
        self.assertEqual('(⊤ ∧ ⊥)', phi4.represent(naive.rformats.UTF8))

        phi5 = naive.core.f(naive.ba1.disjunction, phi1, phi2)
        self.assertEqual('(⊤ ∨ ⊥)', phi5.represent(naive.rformats.UTF8))

    def test_atomic_variable_as_formula(self):
        x = naive.core.av(naive.ba1.b, 'x')
        y = naive.core.av(naive.ba1.b, 'y')

        phi1 = naive.core.f(naive.ba1.negation, x)
        self.assertEqual('¬x', phi1.represent(naive.rformats.UTF8))

        phi2 = naive.core.f(naive.ba1.conjunction, x, y)
        self.assertEqual('(x ∧ y)', phi2.represent(naive.rformats.UTF8))

    def test_formula_composition(self):
        z = naive.core.av(naive.ba1.b, 'z')
        x = naive.core.av(naive.ba1.b, 'x')
        y = naive.core.av(naive.ba1.b, 'y')

        phi1 = naive.core.f(naive.ba1.negation, x)
        self.assertEqual('¬x', phi1.represent(naive.rformats.UTF8))
        self.assertEqual('[x]', str(phi1.list_atomic_variables()))

        phi2 = naive.core.f(naive.ba1.conjunction, phi1, y)
        self.assertEqual('(¬x ∧ y)', phi2.represent(naive.rformats.UTF8))
        print(phi2.list_atomic_variables())
        self.assertEqual('[x, y]', str(phi2.list_atomic_variables()))

        phi3 = naive.core.f(naive.ba1.disjunction, phi2, phi1)
        self.assertEqual('((¬x ∧ y) ∨ ¬x)', phi3.represent(naive.rformats.UTF8))
        print(phi3.list_atomic_variables())
        self.assertEqual('[x, y]', str(phi3.list_atomic_variables()))

    def test_complex_programmatic_construction_and_satisfaction_set(self):
        # naive.log.set_debug_level()
        b3 = naive.core.av(codomain=naive.ba1.b, base_name='b', indexes=3)
        b1 = naive.core.av(codomain=naive.ba1.b, base_name='b', indexes=1)
        b2 = naive.core.av(codomain=naive.ba1.b, base_name='b', indexes=2)
        psi1 = naive.core.f(naive.ba1.conjunction, b1, b2)
        psi2 = naive.core.f(naive.ba1.disjunction, b3, b1)
        psi3 = naive.core.f(naive.ba1.conjunction, psi1, psi2)
        self.assertEqual('[b₁, b₂, b₃]', str(psi3.list_atomic_variables()))
        #worlds = naive.ba1.get_boolean_combinations(psi3.arity)
        #print(worlds)
        sat_i = naive.ba1.satisfaction_index(psi3)
        print(sat_i)
        self.assertEqual('[⊥, ⊥, ⊥, ⊤, ⊥, ⊥, ⊥, ⊤]', str(sat_i))

    def test_parsing_code(self):
        code_1 = r'(((⊤ ∨ b1) ∧ (⊥ ∧ ¬⊥)) ∧ ¬b2)'
        parsed_formula_1 = naive.parsing.parse_string_utf8(code_1)
        self.assertEqual(code_1, parsed_formula_1.represent(rformats.UTF8))

        code_1_extra_parenthesis = r'(((((((⊤ ∨ ((((b1))))))) ∧ (⊥ ∧ ¬⊥)))) ∧ ¬b2)'
        parsed_formula_1_extra_parenthesis = naive.parsing.parse_string_utf8(code_1_extra_parenthesis)
        self.assertEqual(code_1, parsed_formula_1_extra_parenthesis.represent(rformats.UTF8))

        code_2 = r'¬⊥'
        parsed_formula_2 = naive.parsing.parse_string_utf8(code_2)
        self.assertEqual(code_2, parsed_formula_2.represent(rformats.UTF8))

        code_3 = r'⊥'
        parsed_formula_3 = naive.parsing.parse_string_utf8(code_3)
        self.assertEqual(code_3, parsed_formula_3.represent(rformats.UTF8))

        code_4 = r'b₇₃'
        parsed_formula_4 = naive.parsing.parse_string_utf8(code_4)
        self.assertEqual(code_4, parsed_formula_4.represent(rformats.UTF8))

        code_5 = r'(p ∨ q)'
        parsed_formula_5 = naive.parsing.parse_string_utf8(code_5)
        self.assertEqual(code_5, parsed_formula_5.represent(rformats.UTF8))
