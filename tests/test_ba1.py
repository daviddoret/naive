from unittest import TestCase
import src.naive as naive


class Test(TestCase):
    def test_ba1(self):
        self.assertEqual(naive.ba1.falsum.represent(naive.rformats.UTF8), '⊥')
        self.assertEqual(naive.ba1.truth.represent(naive.rformats.UTF8), '⊤')

    def test_b_variable_declaration(self):
        x = naive.core.v(naive.ba1.b, 'x')
        self.assertEqual('x', x.represent(naive.rformats.UTF8))
        y = naive.core.v(naive.ba1.b, 'y')
        self.assertEqual('y', y.represent(naive.rformats.UTF8))
        z = naive.core.v(naive.ba1.b, 'z')
        self.assertEqual('z', z.represent(naive.rformats.UTF8))

    def test_get_bn_domains(self):
        self.assertEqual('𝔹', naive.ba1.get_bn_domain(1).represent(naive.rformats.UTF8))
        self.assertEqual('𝔹²', naive.ba1.get_bn_domain(2).represent(naive.rformats.UTF8))
        self.assertEqual('𝔹³', naive.ba1.get_bn_domain(3).represent(naive.rformats.UTF8))
        self.assertEqual('𝔹⁴', naive.ba1.get_bn_domain(4).represent(naive.rformats.UTF8))
        self.assertEqual('𝔹²³⁴', naive.ba1.get_bn_domain(234).represent(naive.rformats.UTF8))

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

    def test_atomic_variable_as_formula(self):
        x = naive.core.v(naive.ba1.b, 'x')
        y = naive.core.v(naive.ba1.b, 'y')

        phi1 = naive.core.f(naive.ba1.negation, x)
        phi2 = naive.core.f(naive.ba1.conjunction, x, y)


