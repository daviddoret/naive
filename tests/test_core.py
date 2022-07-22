from unittest import TestCase

import src.naive as naive


class Test(TestCase):
    def test_clean_key(self):
        self.assertEqual('abcd', naive.core.clean_mnemonic_key('abcd'))
        self.assertEqual('abcd', naive.core.clean_mnemonic_key('a⊤b¬ c 𝔹 ⟼φΦd'))


class TestConcept(TestCase):
    def test_init(self):
        c1 = naive.core.Concept(
            scope_key='scopetest', structure_key='structuretest', language_key='languagetest', base_key='test1',
            utf8='test1', latex=r'\text{test}_{1}', html=r'test<sub>1</sub>', usascii='test1')
        self.assertEqual('scopetest.structuretest.languagetest.test1', c1.qualified_key)
        self.assertEqual(c1, naive.core.Concept.get_concept_from_qualified_key(c1.qualified_key))
        self.assertEqual(c1, naive.core.Concept.get_concept_from_decomposed_key(
            scope_key=c1.scope_key, structure_key=c1.structure_key, language_key=c1.language, base_key=c1.base_key))


class TestFunction(TestCase):
    def test_init(self):
        f1 = naive.core.AtomicFunction(
            scope_key='scope_test', structure_key='structure_test', language_key='language_test', base_key='test_1',
            codomain='domain_test', category=naive.core.AtomicFunction.CONSTANT,
            utf8='test₁', latex=r'\text{test}_{1}', html=r'test<sub>1</sub>', usascii='test1',
            domain='domain_test', arity=17, python_value='test python value'
        )
        self.assertEqual('scope_test.structure_test.language_test.test_1', f1.qualified_key)
        self.assertEqual(f1, naive.core.Concept.get_concept_from_qualified_key(f1.qualified_key))
        self.assertEqual(f1, naive.core.Concept.get_concept_from_decomposed_key(
            scope_key=f1.scope_key, structure_key=f1.structure_key, language_key=f1.language, base_key=f1.base_key))


class Test(TestCase):
    def test_set_default_scope(self):
        self.assertEqual('scope1', naive.core.get_default_scope())
        naive.core.set_default_scope('new scope')
        self.assertEqual('newscope', naive.core.get_default_scope())
        naive.core.set_default_scope('scope1')
        self.assertEqual('scope1', naive.core.get_default_scope())
