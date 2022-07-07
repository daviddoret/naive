from _class_variable_base import VariableBase
from _class_variable_indexes import VariableIndexes
from _abc_representable import ABCRepresentable
from _function_get_representation import get_representation
from _function_subscriptify import subscriptify
import rformats


class Variable(ABCRepresentable):
    """A mathematical object that may be defined from a defining object.

    The representation of a variable is composed of the variable base,
    conditionally followed by variable indexes.
    """

    def __init__(self, base: VariableBase, indexes: (None, VariableIndexes), *args, **kwargs):
        # TODO: Implement type coercion
        self._base = base
        self._indexes = indexes

        super().__init__(base, indexes, *args, **kwargs)

    def get_representation(self, rformat: str = None, *args, **kwargs) -> str:
        if rformat is None:
            rformat = rformats.DEFAULT
        # TODO: Minor bug: only digits are currently supported by subscript().
        return get_representation(self._base, rformat) + get_representation(self._indexes, rformat)



