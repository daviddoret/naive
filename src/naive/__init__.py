# Headaches with paths
# import sys
# import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# sys.path.append(os.path.dirname(os.path.realpath(__file__)))

# This works fine:
from hello_world import hello_world
from coercion_error import CoercionError
from coercion_warning import CoercionWarning
from coerce import coerce

# Looks promising to eventually simplify everything
# from naive import *

# Package Version
__version__ = '{version}'

# References
#   * https://realpython.com/python-modules-packages/