from unittest import TestCase
import src.naive as naive


class Test(TestCase):
    def test_ba1(self):
        self.assertEqual(naive.ba1.falsum.represent(naive.rformats.UTF8), '⊥')
        self.assertEqual(naive.ba1.truth.represent(naive.rformats.UTF8), '⊤')

    def test_b_variable_declaration(self):
        x = naive.core.v('x', naive.ba1.b)
        y = naive.core.v('y', naive.ba1.b)
        z = naive.core.v('z', naive.ba1.b)

    def test_formula(self):
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




