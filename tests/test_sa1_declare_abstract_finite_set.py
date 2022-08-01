from unittest import TestCase
import naive


class TestSA1DeclareAbstractElements(TestCase):
    def test_default_names(self):
        naive.set_unique_scope()
        s1 = naive.SA1.declare_abstract_set(3)
        self.assertEqual('s₁', str(s1.elements[0]))
        self.assertEqual('s₂', str(s1.elements[1]))
        self.assertEqual('s₃', str(s1.elements[2]))
        self.assertEqual('S', str(s1))

    def test_custom_names(self):
        naive.set_unique_scope()
        x1 = naive.SA1.declare_abstract_set(3, base_name='X', element_base_name='x')
        self.assertEqual('x₁', str(x1.elements[0]))
        self.assertEqual('x₂', str(x1.elements[1]))
        self.assertEqual('x₃', str(x1.elements[2]))
        self.assertEqual('X', str(x1))

    def test_default_names(self):
        naive.set_unique_scope()

        s1 = naive.SA1.declare_abstract_set(4, indexes=1)
        self.assertEqual('s₁', str(s1.elements[0]))
        self.assertEqual('s₂', str(s1.elements[1]))
        self.assertEqual('s₃', str(s1.elements[2]))
        self.assertEqual('s₄', str(s1.elements[3]))
        self.assertEqual('S₁', str(s1))

        s2 = naive.SA1.declare_abstract_set(2, indexes=2)
        self.assertEqual('s₁', str(s2.elements[0]))
        self.assertEqual('s₂', str(s2.elements[1]))
        self.assertEqual('S₂', str(s2))