# BIBLIOGRAPHY
#   * https://realpython.com/python-modules-packages/


# LOGGING
import logging
logging.info('Naive Package: __init__.py: Initialization started')


# PACKAGE VERSION
import importlib.metadata
try:
    __version__ = importlib.metadata.version('naive')
except:
    __version__ = '1.1.1'  # Initial version for the first build.


# NAIVE OBJECT IMPORTATION
from _abc_representable import ABCRepresentable
from _class_glyph import Glyph
from _class_persisting_representable import PersistingRepresentable
from _class_symbol import Symbol
from _class_variable import Variable
from _class_variable_base import VariableBase
from _class_variable_indexes import VariableIndexes
from _exception_coercion_error import CoercionError
from _exception_coercion_warning import CoercionWarning
from _function_coerce import coerce
from _function_flatten import flatten
from _function_get_representation import get_representation
from _function_subscriptify import subscriptify
from _function_superscriptify import superscriptify


# NAIVE MODULE IMPORTATION
import rformats
import glyphs
import notation


# LOGGING
logging.info('Naive Package: __init__.py: Initialization completed')
