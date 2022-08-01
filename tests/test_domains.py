from unittest import TestCase
import src.naive as naive


class TestDomains(TestCase):
    """Objective: test the general consistency of domains."""
    def test_domains(self):
        self.assertEqual('𝔹', naive.repr(naive.BA1.b))
        self.assertEqual('𝔹²', naive.repr(naive.BA1.b2))
        self.assertEqual('𝔹³', naive.repr(naive.BA1.get_bn_domain(3)))
        self.assertEqual('𝔹¹²³⁴⁵⁶⁷⁸⁹⁰', naive.repr(naive.BA1.get_bn_domain(1234567890)))
        #self.assertEqual(naive.domains.n0.represent(naive.rformats.UTF8), 'ℕ₀')
        #self.assertEqual(naive.domains.n1.represent(naive.rformats.UTF8), 'ℕ₁')
        #self.assertEqual(naive.domains.z.represent(naive.rformats.UTF8), 'ℤ')
