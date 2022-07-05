from __future__ import annotations
import warnings
import typing
import threading
from src.naive.coerce import coerce
from src.naive.coercion_error import CoercionError
from src.naive.coercion_warning import CoercionWarning
import src.naive.variable as variable
import src.naive.domain_library as domain
from src.naive.variable_definition import VariableDefinition
import src.naive.notation as settings


class NTuple(VariableDefinition):
    """An N-Tuple of mathematical variables."""

    """Class attribute for text representation."""
    class_notation = settings.N_TUPLE_DOMAIN_NOTATION

    def __init__(self, *args):
        """Instantiates an **N-Tuple**.

        Args:
            *args: A source object from which to instantiate the **N-Tuple**.

        Returns:
            NTuple: A new N-Tuple of variables.

        """
        self._variables_list_lock = threading.Lock()
        self._variables_list = []

        for v in args:
            self.append_variable(v)

    def append_variable(self, v: variable.Variable) -> None:
        v = coerce(v, variable.Variable)
        with self._variables_list_lock:
            gen = (w for w in self._variables_list if w.name == v.name)
            if next(gen, None) is not None:
                raise IndexError(f'The N-Tuple already contains a variable with named "{v.name}".')
            else:
                self._variables_list.append(v)

    def get_variable_by_position(self, position):
        """Get a variable from its position in the N-Tuple.

        Args:
            position: The position of the variable in the N-Tuple. Position is a 1-based index.

        Returns:
            Variable, None: The variable if there is a variable at this position. None otherwise.
        """
        # TODO: Provide explicit support for position typed as NN1.
        idx = position - 1
        with self._variables_list_lock:
            if idx < 0:
                raise NotImplementedError('Negative positions are not supported, but it may be in the future')
            last_position = len(self._variables_list)
            if position <= last_position:
                return self._variables_list[idx]
            else:
                return None

    def get_variable_by_fully_qualified_name(self, fully_qualified_name):
        with self._variables_list_lock:
            gen = (v for v in self._variables_list if v.qualified_name == fully_qualified_name)
            match = next(gen, None) # Assumption: names are unique in this context.
            if match is None:
                return None
            else:
                return match

    def get_variable_by_name(self, name: str):
        with self._variables_list_lock:
            gen = (v for v in self._variables_list if v.name == name)
            match = next(gen, None) # Assumption: names are unique in this context.
            if match is None:
                return None
            else:
                return match

    # TODO: Implement get_variable_by_indexes (meaning "variable indexes")

    @property
    def domain(self) -> domain.Domain:
        return domain.domains.n_tuple

