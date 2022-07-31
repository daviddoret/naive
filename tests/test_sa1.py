from unittest import TestCase
import naive


class TestSA1(TestCase):

    def test_sa1_1(self):
        naive.set_unique_scope()
        s1 = naive.SA1.declare_finite_set(elements=[1, 2, 3])

    def test_sa1_2(self):
        naive.set_unique_scope()
        s1 = naive.SA1.declare_finite_set(base_name='S', indexes=1, elements=[1, 2, 3])
        s2 = naive.SA1.declare_finite_set(base_name='S', indexes=2, elements=[3, 4, 5])
        s3 = naive.SA1.declare_finite_set(base_name='S', indexes=3, elements=[5, 6, 1])

