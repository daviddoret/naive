from unittest import TestCase
import atom


class TestLabelSpace(TestCase):
    def test_atom_1_init(self):
        l1 = atom.AtomSet(n=5)
        self.assertEqual(len(l1), 5)
        self.assertEqual(str(l1[3]), 'a3')
        l2 = atom.AtomSet(['lx', 'ly', 'lz'])
        self.assertEqual(str(l2[1]), 'ly')
        l3 = atom.AtomSet(5)
        self.assertEqual(l3, l1)
        self.assertNotEqual(l3, l2)

    def test_atom_2_eq(self):
        """Equality Tests"""
        self.assertEqual(atom.AtomSet(['l0', 'l1', 'l2']), atom.AtomSet(['l2', 'l1', 'l0']))
        self.assertNotEqual(atom.AtomSet(['l0', 'l1', 'l2']), atom.AtomSet(['l0', 'l1']))
        self.assertNotEqual(atom.AtomSet(['l0', 'l1']), atom.AtomSet(['l1', 'l2']))

    def test_atom_3_index(self):
        """Get element index"""
        l1 = atom.AtomSet(5)
        print(l1)
        self.assertEqual(l1.index('a0'), 0)
        self.assertEqual(l1.index('a1'), 1)
        self.assertEqual(l1.index('a2'), 2)
        self.assertEqual(l1.index('a3'), 3)
        self.assertEqual(l1.index('a4'), 4)
        l2 = atom.AtomSet(n=3, index_start=1, prefix='L')
        print(l2)
        self.assertEqual(l2.index('L1'), 0)
        self.assertEqual(l2.index('L2'), 1)
        self.assertEqual(l2.index('L3'), 2)
        l3 = atom.AtomSet(['Red', 'Green', 'Blue'])
        print(l3)
        self.assertEqual(l3.index('Red'), 2)
        self.assertEqual(l3.index('Green'), 1)
        self.assertEqual(l3.index('Blue'), 0)

    def test_atom_4_index_by_key(self):
        """Get element index"""
        l1 = atom.AtomSet(5)
        print(l1)
        self.assertEqual(l1['a0'], 'a0')
        self.assertEqual(l1['a1'], 'a1')
        self.assertEqual(l1['a2'], 'a2')
        self.assertEqual(l1['a3'], 'a3')
        self.assertEqual(l1['a4'], 'a4')

    def test_atom_5_index_by_position(self):
        """Get element index"""
        l1 = atom.AtomSet(5)
        print(l1)
        self.assertEqual(l1[0], 'a0')
        self.assertEqual(l1[1], 'a1')
        self.assertEqual(l1[2], 'a2')
        self.assertEqual(l1[3], 'a3')
        self.assertEqual(l1[4], 'a4')
