from __future__ import annotations

# BIBLIOGRAPHY
#   * https://realpython.com/python-modules-packages/


# LOGGING
import logging
logging.info('Naive Package: __init__.py: starting execution...')


# PACKAGE VERSION
import importlib.metadata
try:
    __version__ = importlib.metadata.version('naive')
except:
    __version__ = '1.1.1'  # Initial version for the first build.
logging.info(f'__version__: {__version__}')


# NAIVE OBJECT IMPORTATION
from _abc_representable import ABCRepresentable
from _class_glyph import Glyph
from _class_persisting_representable import PersistingRepresentable, CoerciblePersistingRepresentable
from _class_symbol import Symbol
from _class_function_base_name import FunctionBaseName, CoercibleFunctionBaseName
from _class_function_indexes import FunctionIndexes
from _class_function import Function, F
from _class_variable import Variable
from _class_variable_base_name import VariableBaseName, CoercibleVariableBaseName
from _class_variable_indexes import VariableIndexes
from _class_variable_exponent import VariableExponent
from _class_well_known_domain import WellKnownDomain
from _class_well_known_domain_set import *
from _exception_naive_error import NaiveError
from _exception_naive_warning import NaiveWarning
from _function_coerce import coerce
from _function_flatten import flatten
from _function_represent import represent
from _function_subscriptify import subscriptify
from _function_superscriptify import superscriptify
import boolean_algebra_1
ba1 = boolean_algebra_1  # Use a reference for shorthand aliases to avoid duplicate copies of global variables.


# NAIVE MODULE IMPORTATION
import rformats
import glyphs
import notation
import log


# LOGGING
logging.info('Naive Package: __init__.py: execution completed.')
