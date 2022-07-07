from __future__ import annotations
import warnings
import typing
from src.naive.coerce import coerce
from src.naive.coercion_error import CoercionError
from src.naive.coercion_warning import CoercionWarning
import src.naive.variable as variable
from src.naive.variable_definition import VariableDefinition
import src.naive.notation as settings
import src.naive.variable_base_name as variable_base_name
import src.naive.variable_indexes as variable_indexes

class Environment(VariableDefinition):
    """An root N-Tuple of mathematical variables.

    Todo:
        * This is for future development. The idea is to create environment variables that are t-tuples of variables to store user or other variables.
    """

    """Class attribute for text representation."""
    class_notation = settings.ENVIRONMENT_DOMAIN_NOTATION

    def __init__(self, *args, **kwargs):
        """Instantiates an **Environment**.

        Args:
            *args: A source object from which to instantiate the **N-Tuple**.

        Returns:
            Environment: A new variable environment.

        """
        raise NotImplementedError('Complete implementation first')
        self._variables_list = []
        self._parent_variable = None

        for v in args:
            # Coerce all variables received in input.
            v = coerce(v, variable.Variable)
            # And add them in sequence to the N-Tuple.
            self.append_variable(v)

    def append_variable(self, domain: type,
                        base_name: variable_base_name.CoercibleVariableBaseName,
                        indexes: variable_indexes.VariableIndexes = None,
                        value: VariableDefinition = None,
                        scope: variable.Variable = None
                        ) -> None:

        v = variable.Variable(domain, base_name, indexes, value, scope)
        if v not in self._variables_list:
            self._variables_list.append(v)
        else:
            raise ValueError(f'Variable conflict: could not append {v} to {self}.')

    def get_variable_by_index(self, idx):
        # TODO: This method is not safe. Check position value first and manage index error gracefuly.
        return self._variables_list[idx]

    def get_variable_by_fully_qualified_name(self, fully_qualified_name):
        # TODO: This method is not safe. Check position value first and manage index error gracefuly.
        match = (v for v in self._variables_list if v.qualified_name == fully_qualified_name)
        v = match[0]
        return v

    def get_variable_by_name(self, name: str):
        # TODO: This method is not safe. Check position value first and manage index error gracefuly.
        match = (v for v in self._variables_list if v.name == name)
        v = match[0]
        return v


"""The default user variable scope is an T-Tuple."""
_default_user_environment = None


def get_default_user_environment():
    """Return the default user environment variable."""
    global _default_user_environment
    raise NotImplementedError()
    if _default_user_environment is None:
        base_name = variable_base_name.VariableBaseName(settings.DEFAULT_USER_ENVIRONMENT_BASE_NAME)
        env = Environment()
        _default_user_environment = variable.Variable(Environment, base_name, None, env, None)
        env._parent_variable = _default_user_environment

    return _default_user_environment
