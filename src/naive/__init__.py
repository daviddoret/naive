from __future__ import absolute_import
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
from src.naive.binary_value import BinaryVariable, BinaryValueInput
from src.naive.clean_math_symbol import clean_math_symbol
from src.naive.coerce import coerce
from src.naive.coercion_error import CoercionError
from src.naive.coercion_warning import CoercionWarning
from src.naive.flatten import flatten
from src.naive.natural_number_0 import NaturalNumber0
from src.naive.natural_number_1 import NaturalNumber1
from src.naive.natural_vector_0 import NaturalVector0
from src.naive.natural_vector_1 import NaturalVector1
from src.naive.subscript import subscript
from src.naive.superscript import superscript
from src.naive.variable_base_name import VariableBaseName

"""A shorthand for NaturalNumber0."""
#BV = BinaryVariable
NN0 = NaturalNumber0
NN1 = NaturalNumber1
NV0 = NaturalVector0
NV1 = NaturalVector1
