from unittest import TestCase
import state
from _trashcan import output


class TestStateSpace(TestCase):
    def test_space_1(self):
        s = state.StateSet(5)
        self.assertEqual(len(s), 5)
        s2 = s[2]
        self.assertEqual(s2, 's2')
        S1 = state.StateSet(['s0', 's1', 's2'])
        S2 = state.StateSet(12)
        output.output_math(S1.to_latex_math_v())
        output.output_math(S2.to_latex_math_h())

    def test_space_2(self):
        """Equality Tests"""
        self.assertEqual(state.StateSet(['s0', 's1', 's2']), state.StateSet(['s2', 's1', 's0']))
        self.assertNotEqual(state.StateSet(['s0', 's1', 's2']), state.StateSet(['s0', 's1']))
        self.assertNotEqual(state.StateSet(['s0', 's1']), state.StateSet(['s1', 's2']))

    def test_space_3(self):
        """Get element index"""
        s1 = state.StateSet(5)
        print(s1)
        self.assertEqual(s1.index('s0'), 0)
        self.assertEqual(s1.index('s1'), 1)
        self.assertEqual(s1.index('s2'), 2)
        self.assertEqual(s1.index('s3'), 3)
        self.assertEqual(s1.index('s4'), 4)
        s2 = state.StateSet(n=3, index_start=1, prefix='S')
        print(s2)
        self.assertEqual(s2.index('S1'), 0)
        self.assertEqual(s2.index('S2'), 1)
        self.assertEqual(s2.index('S3'), 2)
        s3 = state.StateSet(['Apple', 'Orange', 'Banana'])
        print(s3)
        self.assertEqual(s3.index('Apple'), 0)
        self.assertEqual(s3.index('Banana'), 1)
        self.assertEqual(s3.index('Orange'), 2)

    def test_get_iv(self):
        self.assertEqual(1, 1)
        s1 = state.StateSet(5)
        self.assertEqual(state.get_iv(s1, [0, 0, 0, 1, 1]), [0, 0, 0, 1, 1])
