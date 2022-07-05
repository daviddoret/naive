from unittest import TestCase
import src.naive as naive


class TestDomains(TestCase):
    def test_common_domains(self):
        self.assertEqual(naive.domains.b, naive.notation.BINARY_NUMBER_DOMAIN_NOTATION)
        self.assertEqual(naive.domains.n0, naive.notation.NATURAL_NUMBER_0_DOMAIN_NOTATION)
        self.assertEqual(naive.domains.n1, naive.notation.NATURAL_NUMBER_1_DOMAIN_NOTATION)
        print(naive.domains.b)
        print(naive.domains.n0)
        print(naive.domains.n1)
