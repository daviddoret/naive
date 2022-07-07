from unittest import TestCase
import src.naive as naive
import src.naive.type_library as tl


class Test(TestCase):
    def test_flatten(self):
        self.assertEqual(tl.flatten(1), [1])
        self.assertEqual(tl.flatten([1, [2], [[3], [4, 5]]]), [1, 2, 3, 4, 5])
        self.assertEqual(tl.flatten(None), [])

    def test_coerce_binary_value(self):
        self.assertEqual(tl.coerce_binary_value(False), 0)
        self.assertEqual(tl.coerce_binary_value(True), 1)
        self.assertEqual(tl.coerce_binary_value(0), 0)
        self.assertEqual(tl.coerce_binary_value(1), 1)

    def test_coerce_incidence_vector(self):
        v1 = tl.coerce_incidence_vector([1, 0, 1])
        # self.assertTrue(isinstance(ks.coerce_incidence_vector([True, False]), ks.IncidenceVector))

    def test_coerce_binary_matrix(self):
        m1 = [[1, 1, 1], [1, 0, 1]]
        m2 = tl.coerce_binary_matrix(m1)
        self.assertIsInstance(m2, tl.BinaryMatrix)
        with self.assertRaises(ValueError):
            tl.coerce_binary_matrix([[1, 2, 3], [4, 5]])

    def test_coerce_binary_square_matrix(self):
        m1 = [[1, 1, 1], [1, 0, 1], [0, 0, 0]]
        m2 = tl.coerce_binary_square_matrix(m1)
        self.assertIsInstance(m2, tl.BinarySquareMatrix)
        with self.assertRaises(IndexError):
            tl.coerce_binary_square_matrix([[1, 2, 3], [4, 5]])

    def test_binary_vector_equal(self):
        o1 = [0, 1, 0, 1, 1, 0, 0, 0, 0]
        o2 = [0, 1, 0, 1, 0, 0, 0, 0, 0]
        o3 = [0, 1, 0, 1, 1, 0, 0, 0, 0]
        self.assertTrue(tl.bv_equal_bv(o1, o3))
        self.assertFalse(tl.bv_equal_bv(o1, o2))
        self.assertFalse(tl.bv_equal_bv(o2, o3))


class TestBinaryVector(TestCase):

    def test_new(self):
        self.assertFalse(tl.BN(), None)
        self.assertEqual(tl.BN(), [])
        self.assertEqual(tl.BN(None), [])
        self.assertEqual(tl.BN([]), [])
        self.assertEqual(tl.BN([0]), [0])
        self.assertEqual(tl.BN([1]), [1])
        self.assertEqual(tl.BN([1, 0]), [1, 0])
        self.assertEqual(tl.BN(size=3), [0, 0, 0])
        self.assertEqual(tl.BN(size=5), [0, 0, 0, 0, 0])
        self.assertEqual(tl.BN(size=3, default_value=1), [1, 1, 1])
        self.assertEqual(tl.BN(size=5, default_value=1), [1, 1, 1, 1, 1])


class TestSet(TestCase):

    def test_init(self):
        self.assertFalse(tl.FS(), None)
        self.assertEqual(tl.FS(), [])
        self.assertFalse(tl.FS(None) is None)
        self.assertEqual(tl.FS([]), [])
        self.assertEqual(tl.FS([0]), ['0'])
        self.assertEqual(tl.FS(['e1']), ['e1'])
        self.assertEqual(tl.FS(['red', 'green', 'blue']), ['red', 'green', 'blue'])
        self.assertEqual(tl.FS(size=3), ['e₁', 'e₂', 'e₃'])
        self.assertEqual(tl.FS(size=5), ['e₁', 'e₂', 'e₃', 'e₄', 'e₅'])
        self.assertEqual(tl.FS(size=2, prefix='x'), ['x₁', 'x₂'])
        self.assertEqual(tl.FS(size=4, prefix='y', init=0), ['y₀', 'y₁', 'y₂', 'y₃'])
