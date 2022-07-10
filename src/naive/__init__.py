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
from _class_variable import Variable
from _class_variable_base import VariableBase, CoercibleVariableBase
from _class_variable_indexes import VariableIndexes
from _exception_coercion_error import CoercionError
from _exception_coercion_warning import CoercionWarning
from _function_coerce import coerce
from _function_flatten import flatten
from _function_represent import represent
from _function_subscriptify import subscriptify
from _function_superscriptify import superscriptify


# NAIVE MODULE IMPORTATION
import rformats
import glyphs
import notation
import domains


# LOGGING
logging.info('Naive Package: __init__.py: execution completed.')
