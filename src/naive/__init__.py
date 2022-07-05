from __future__ import absolute_import, annotations
"""naive: TODO: Add short description here"""

# Version of the naive package
__version__ = "0.1.6"

# Source: https://stackoverflow.com/questions/67085041/how-to-specify-version-in-only-one-place-when-using-pyproject
# -toml import importlib.metadata __version__ = importlib.metadata.version("naive")

# from .scope_management import Scope
# from .scope_management import PowerContext
# from .scope_management import UserContext
# from .scope_management import SystemContext
# from .scope_management import contexts

# import hello_world as naive
# import binary_value as naive
# import clean_math_symbol as naive
# import coerce as naive
# import coercion_error as naive
# import coercion_warning as naive
# import flatten as naive
# import natural_number_0 as naive
# import natural_number_1 as naive
# import natural_vector_0 as naive
# import natural_vector_1 as naive
# import subscript as naive
# import superscript as naive
# import variable_base_name as naive
from src.naive.hello_world import hello_world
from src.naive.binary_constant import *
from src.naive.clean_math_symbol import clean_math_symbol
from src.naive.coerce import coerce
from src.naive.coercion_error import CoercionError
from src.naive.coercion_warning import CoercionWarning
from src.naive.flatten import flatten
from src.naive.natural_number_0_constant import NaturalNumber0Constant, NN0C
from src.naive.natural_number_1_constant import NaturalNumber1Constant, NN1C
from src.naive.natural_vector_0 import NaturalVector0
from src.naive.natural_vector_1 import NaturalVector1
from src.naive.n_tuple_variable_content import NTuple
from src.naive.subscript import subscript
from src.naive.superscript import superscript
from src.naive.variable_base_name import VariableBaseName
from src.naive.variable_definition import Constant, binary_unknown
from src.naive.variable_indexes import VariableIndexes
from src.naive.variable import Variable
from src.naive.domain_library import Domain, DomainSet, domains
import src.naive.notation as settings


"""A shorthand for NaturalNumber0."""
#BC = BinaryConstant
NV0 = NaturalVector0
NV1 = NaturalVector1
