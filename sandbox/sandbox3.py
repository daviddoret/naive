import logging
import log
import src.naive as naive
from src.naive.boolean_algebra_1 import *


x1 = naive.Variable('x', 1)
x2 = naive.Variable('x', 2)
x3 = naive.Variable('x', 3)
args = [x1, x2, x3]

variable_list = ', '.join(map(lambda a: a.represent(), args))
print(variable_list)