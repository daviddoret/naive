from __future__ import absolute_import
import warnings
from src.naive.coercion_error import CoercionError


class VariableBaseName(str):
    """The base name of a mathematical variable is that variable's name without its indexes, if any.

    Todo:
        * Implement finer support for unicode mathematical alphabetical symbols from this reference https://en.wikipedia.org/wiki/Mathematical_Alphanumeric_Symbols
    """
    def __new__(cls, base_name: str):
        """Assure that the variable base name is clean from undesirable characters.

        Args:
            base_name (str): A string that may not be clean from undesirable characters.

        Returns:
            cls: A base name that is clean from undesirable characters.
        """
        if base_name is None:
            raise CoercionError('A variable base name cannot be None')
        base_name = str(base_name)
        sanitized_base_name = ''.join([c for c in str(base_name) if c.isalpha()])
        if len(base_name) != len(sanitized_base_name):
            warnings.warn(f'The sanitization of variable base name "{base_name}" resulted in new base name "".')
        if len(sanitized_base_name) == 0:
            raise CoercionError('A variable base name cannot be an empty string')
        return super().__new__(cls, sanitized_base_name)