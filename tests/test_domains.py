from unittest import TestCase
import src.naive as naive


class Test(TestCase):
    def test_domains(self):
        self.assertEqual(naive.domains.b.get_representation(naive.rformats.UTF8), '𝔹')
        self.assertEqual(naive.domains.n0.get_representation(naive.rformats.UTF8), 'ℕ₀')
        self.assertEqual(naive.domains.n1.get_representation(naive.rformats.UTF8), 'ℕ₁')
        self.assertEqual(naive.domains.z.get_representation(naive.rformats.UTF8), 'ℤ')
