# Headaches with paths
# import sys
# import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# sys.path.append(os.path.dirname(os.path.realpath(__file__)))

# Package Version
#__version__ = '1.1.1'
import importlib.metadata
__version__ = importlib.metadata.version('naive')

# This works fine:
from hello_world import hello_world

import notation

from coercion_error import CoercionError
from coercion_warning import CoercionWarning
from coerce import coerce

from domain_set import DomainSet
from domain_library import Domain
from domain_init import *

#from binary_number import BinaryNumber, BN, CoercibleBinaryNumber
#from natural_number_0 import NaturalNumber0, NN0, CoercibleNaturalNumber0
#from natural_number_1 import NaturalNumber1, NN1, CoercibleNaturalNumber1


# Looks promising to eventually simplify everything
# from naive import *

# References
#   * https://realpython.com/python-modules-packages/