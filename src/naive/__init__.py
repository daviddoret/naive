"""naive: TODO: Add short description here"""

# Version of the naive package
__version__ = "0.1.5"

# Source: https://stackoverflow.com/questions/67085041/how-to-specify-version-in-only-one-place-when-using-pyproject-toml
#import importlib.metadata
#__version__ = importlib.metadata.version("naive")

from .binary_value import BinaryValue
from .binary_value import BinaryValueInput
from .clean_math_variable import clean_math_variable
from .coerce import coerce
from .coercion_error import CoercionError
from .coercion_warning import CoercionWarning
from .natural_number_0 import NaturalNumber0
from .subscript import subscript
from .superscript import superscript

"""A shorthand for NaturalNumber0."""
BV = BinaryValue
NN0 = NaturalNumber0
