from unittest import TestCase
from src.naive.environment_variable_content import Environment
from src.naive.variable import Variable
from src.naive.binary_constant import BinaryConstant, BC


# class TestEnvironment(TestCase):
#     def test_1(self):
#         b0 = BC(False)
#         b1 = BC(True)
#         env1 = Variable(Environment, 'E1', None, Environment(), None)
#         env1.value.append_variable(Variable(BC, 'x', None, b0))
#         env1.value.append_variable(Variable(BC, 'y', None, b1))
#         env1.value.append_variable(Variable(BC, 'z', None, b0))
#         self.assertEqual(env1.value.get_variable_by_index(0).value, env1.value.get_variable_by_index(2).value)
#         self.assertNotEqual(env1.value.get_variable_by_index(0).value, env1.value.get_variable_by_index(1).value)
#         print(env1.fully_qualified_name)
#         print()
