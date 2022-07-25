from unittest import TestCase

import naive


class Test(TestCase):
    def test_clean_key(self):
        naive.set_unique_scope()
        self.assertEqual('abcd', naive.Utils.clean_mnemonic_key('abcd'))
        self.assertEqual('abcd', naive.Utils.clean_mnemonic_key('a⊤b¬ c 𝔹 ⟼φΦd'))


class TestConcept(TestCase):
    def test_init(self):
        naive.set_unique_scope()
        c1 = naive.Core.Concept(
            scope_key='scopetest', facet_key='facet_test', language_key='language_test', base_key='test1',
            utf8='test1', latex=r'\text{test}_{1}', html=r'test<sub>1</sub>', usascii='test1')
        self.assertEqual('scopetest.facet_test.language_test.test1', c1.qualified_key)
        self.assertEqual(c1, naive.Core.Concept.get_concept_from_qualified_key(c1.qualified_key))
        self.assertEqual(c1, naive.Core.Concept.get_concept_from_decomposed_key(
            scope_key=c1.scope_key, facet_key=c1.facet_key, language_key=c1.language, base_key=c1.base_key))


class TestFunction(TestCase):
    def test_init(self):
        naive.set_unique_scope()
        f1 = naive.Core.SystemFunction(
            scope_key='scope_test', facet_key='facet_test', language_key='language_test', base_key='test_1',
            codomain='domain_test', category=naive.Core.SystemFunction.SYSTEM_CONSTANT, algorithm=naive.BA1.falsum_algorithm,
            utf8='test₁', latex=r'\text{test}_{1}', html=r'test<sub>1</sub>', usascii='test1',
            domain='domain_test', arity=17, python_value='test python value'
        )
        self.assertEqual('scope_test.facet_test.language_test.test_1', f1.qualified_key)
        self.assertEqual(f1, naive.Core.Concept.get_concept_from_qualified_key(f1.qualified_key))
        self.assertEqual(f1, naive.Core.Concept.get_concept_from_decomposed_key(
            scope_key=f1.scope_key, facet_key=f1.facet_key, language_key=f1.language, base_key=f1.base_key))


class Test_User_Scope(TestCase):
    def test_set_default_scope(self):
        naive.set_unique_scope()
        #self.assertEqual('scope_1', naive.get_default_scope())
        naive.set_default_scope('newscope')
        self.assertEqual('newscope', naive.get_default_scope())
        naive.set_default_scope('scope_1')
        self.assertEqual('scope_1', naive.get_default_scope())


    def test_basic_atomic_variable_declaration(self):
        naive.set_unique_scope()
        b1 = naive.av(naive.BA1.b, base_name='b', indexes=1)
        self.assertEqual('b₁', b1.represent(naive.RFormats.UTF8))

    def test_representation_of_truth_and_falsum(self):
        naive.set_unique_scope()
        self.assertEqual(naive.BA1.truth.represent(naive.RFormats.UTF8), '⊤')
        self.assertEqual(naive.BA1.falsum.represent(naive.RFormats.UTF8), '⊥')

    def test_b_variable_declaration(self):
        naive.set_unique_scope()
        x = naive.av(naive.BA1.b, 'x')
        self.assertEqual('x', x.represent(naive.RFormats.UTF8))
        y = naive.av(naive.BA1.b, 'y')
        self.assertEqual('y', y.represent(naive.RFormats.UTF8))
        z = naive.av(naive.BA1.b, 'z')
        self.assertEqual('z', z.represent(naive.RFormats.UTF8))

    def test_representation_of_domains_and_b_tuple_domains(self):
        naive.set_unique_scope()
        self.assertEqual('𝔹', naive.BA1.b.represent(naive.RFormats.UTF8))
        self.assertEqual('𝔹²', naive.BA1.b2.represent(naive.RFormats.UTF8))

        self.assertEqual('𝔹', naive.BA1.get_bn_domain(1).represent(naive.RFormats.UTF8))
        self.assertEqual('𝔹²', naive.BA1.get_bn_domain(2).represent(naive.RFormats.UTF8))
        self.assertEqual('𝔹³', naive.BA1.get_bn_domain(3).represent(naive.RFormats.UTF8))
        self.assertEqual('𝔹⁴', naive.BA1.get_bn_domain(4).represent(naive.RFormats.UTF8))
        self.assertEqual('𝔹²³⁴', naive.BA1.get_bn_domain(234).represent(naive.RFormats.UTF8))

    def test_formula_representation(self):
        naive.set_unique_scope()
        naive.Log.set_debug_level()
        naive.USE_PRINT_FOR_INFO = False
        naive.set_default_scope('test_formula_representation')

        phi1 = naive.f(naive.BA1.truth)
        self.assertEqual('⊤', phi1.represent(naive.RFormats.UTF8))

        phi2 = naive.f(naive.BA1.falsum)
        self.assertEqual('⊥', phi2.represent(naive.RFormats.UTF8))

        phi3 = naive.f(naive.BA1.negation, phi1)
        self.assertEqual('¬⊤', phi3.represent(naive.RFormats.UTF8))

        phi4 = naive.f(naive.BA1.conjunction, phi1, phi2)
        self.assertEqual('(⊤ ∧ ⊥)', phi4.represent(naive.RFormats.UTF8))

        phi5 = naive.f(naive.BA1.disjunction, phi1, phi2)
        self.assertEqual('(⊤ ∨ ⊥)', phi5.represent(naive.RFormats.UTF8))

    def test_atomic_variable_as_formula(self):
        naive.set_unique_scope()
        x = naive.av(naive.BA1.b, 'x')
        y = naive.av(naive.BA1.b, 'y')

        phi1 = naive.f(naive.BA1.negation, x)
        self.assertEqual('¬x', phi1.represent(naive.RFormats.UTF8))

        phi2 = naive.f(naive.BA1.conjunction, x, y)
        self.assertEqual('(x ∧ y)', phi2.represent(naive.RFormats.UTF8))

    def test_formula_composition(self):
        naive.set_unique_scope()
        z = naive.av(naive.BA1.b, 'z')
        x = naive.av(naive.BA1.b, 'x')
        y = naive.av(naive.BA1.b, 'y')

        phi1 = naive.f(naive.BA1.negation, x)
        self.assertEqual('¬x', phi1.represent(naive.RFormats.UTF8))
        self.assertEqual('[x]', str(phi1.list_atomic_variables()))

        phi2 = naive.f(naive.BA1.conjunction, phi1, y)
        self.assertEqual('(¬x ∧ y)', phi2.represent(naive.RFormats.UTF8))
        print(phi2.list_atomic_variables())
        self.assertEqual('[x, y]', str(phi2.list_atomic_variables()))

        phi3 = naive.f(naive.BA1.disjunction, phi2, phi1)
        self.assertEqual('((¬x ∧ y) ∨ ¬x)', phi3.represent(naive.RFormats.UTF8))
        print(phi3.list_atomic_variables())
        self.assertEqual('[x, y]', str(phi3.list_atomic_variables()))

    def test_complex_programmatic_construction_and_satisfaction_set(self):
        naive.set_unique_scope()
        # naive.log.set_debug_level()
        naive.set_default_scope('test_complex_programmatic_construction_and_satisfaction_set')
        b3 = naive.av(codomain=naive.BA1.b, base_name='b', indexes=3)
        b1 = naive.av(codomain=naive.BA1.b, base_name='b', indexes=1)
        b2 = naive.av(codomain=naive.BA1.b, base_name='b', indexes=2)
        psi1 = naive.f(naive.BA1.conjunction, b1, b2)
        psi2 = naive.f(naive.BA1.disjunction, b3, b1)
        psi3 = naive.f(naive.BA1.conjunction, psi1, psi2)
        self.assertEqual('[b₁, b₂, b₃]', str(psi3.list_atomic_variables()))
        # worlds = naive.BA1.get_boolean_combinations(psi3.arity)
        # print(worlds)
        sat_i = naive.BA1.satisfaction_index(psi3)
        print(sat_i)
        self.assertEqual('[⊥, ⊥, ⊥, ⊤, ⊥, ⊥, ⊥, ⊤]', str(sat_i))

    def test_parsing_code(self):
        naive.set_unique_scope()
        code_1 = r'(((⊤ ∨ b1) ∧ (⊥ ∧ ¬⊥)) ∧ ¬b2)'
        parsed_formula_1 = naive.parse_string_utf8(code_1)
        self.assertEqual(code_1, parsed_formula_1.represent(naive.RFormats.UTF8))
        g = naive.Repr.convert_formula_to_graphviz_digraph(parsed_formula_1)
        g.render('test', format='svg', view=True)

        code_1_extra_parenthesis = r'(((((((⊤ ∨ ((((b1))))))) ∧ (⊥ ∧ ¬⊥)))) ∧ ¬b2)'
        parsed_formula_1_extra_parenthesis = naive.parse_string_utf8(code_1_extra_parenthesis)
        self.assertEqual(code_1, parsed_formula_1_extra_parenthesis.represent(naive.RFormats.UTF8))

    def test_parsing_code_2(self):
        naive.set_unique_scope()
        code_2 = r'¬⊥'
        parsed_formula_2 = naive.parse_string_utf8(code_2)
        self.assertEqual(code_2, parsed_formula_2.represent(naive.RFormats.UTF8))
        g = naive.Repr.convert_formula_to_graphviz_digraph(parsed_formula_2)
        g.render('test', format='svg', view=True)

    def test_parsing_code_3(self):
        naive.set_unique_scope()
        code_3 = r'⊥'
        parsed_formula_3 = naive.parse_string_utf8(code_3)
        self.assertEqual(code_3, parsed_formula_3.represent(naive.RFormats.UTF8))
        g = naive.Repr.convert_formula_to_graphviz_digraph(parsed_formula_3)
        g.render('test', format='svg', view=True)

    def test_parsing_code_4(self):
        naive.set_unique_scope()
        code_4 = r'b₇₃'
        parsed_formula_4 = naive.parse_string_utf8(code_4)
        self.assertEqual(code_4, parsed_formula_4.represent(naive.RFormats.UTF8))
        g = naive.Repr.convert_formula_to_graphviz_digraph(parsed_formula_4)
        g.render('test', format='svg', view=True)

    def test_parsing_code_5(self):
        naive.set_unique_scope()
        from PIL import Image
        import graphviz
        code_5 = r'(p ∨ q)'
        parsed_formula_5 = naive.parse_string_utf8(code_5)
        self.assertEqual(code_5, parsed_formula_5.represent(naive.RFormats.UTF8))
        g = naive.Repr.convert_formula_to_graphviz_digraph(parsed_formula_5)
        g.render('test', format='svg', view=True)

    def test_dot(self):
        naive.set_unique_scope()
        naive.set_default_scope('test_dot')
        code_5 = r'(p ∨ q)'
        parsed_formula_5 = naive.parse_string_utf8(code_5)
        self.assertEqual(code_5, parsed_formula_5.represent(naive.RFormats.UTF8))
        print(naive.Repr.convert_formula_to_dot(parsed_formula_5))

