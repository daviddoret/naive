from unittest import TestCase
import src.naive as naive


class TestNTuple(TestCase):
    def test_append_variable(self):
        t = naive.NTuple()
        v = naive.Variable(naive.NTuple, 't', None, t, None)
        v.value.append_variable(naive.Variable(naive.NN0C, 'a', None, naive.NN0C(1), None))
        v.value.append_variable(naive.Variable(naive.NN0C, 'b', None, naive.NN0C(0), None))
        v.value.append_variable(naive.Variable(naive.NN1C, 'c', None, naive.NN1C(12), None))
        v.value.append_variable(naive.Variable(naive.BinaryConstant, 'd', None, naive.BinaryConstant(False), None))
        v.value.append_variable(naive.Variable(naive.BinaryConstant, 'e', None, naive.BinaryConstant(True), None))
        print(v.value.get_variable_by_position(1))
        print(v.value.get_variable_by_position(2))
        print(v.value.get_variable_by_position(3))
        print(v.value.get_variable_by_position(4))
        print(v.value.get_variable_by_position(5))
        self.assertEqual(v.value.get_variable_by_position(1).value, 1)
        self.assertEqual(v.value.get_variable_by_position(2).value, 0)
        self.assertEqual(v.value.get_variable_by_position(3).value, 12)
        self.assertEqual(v.value.get_variable_by_position(4).value, False)
        self.assertEqual(v.value.get_variable_by_position(5).value, True)

    def test_get_variable_by_position(self):
        self.fail()

    def test_get_variable_by_fully_qualified_name(self):
        self.fail()

    def test_get_variable_by_name(self):
        self.fail()
