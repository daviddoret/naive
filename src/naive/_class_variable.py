from _class_variable_base import VariableBase
from _class_variable_indexes import VariableIndexes
from _abc_representable import ABCRepresentable
from _function_represent import represent
from _function_coerce import coerce
from _function_flatten import flatten
import rformats


class Variable(ABCRepresentable):
    """A mathematical variable object.

     A variable is defined as an element that may be defined by a defining object.

    The representation of a variable is composed of a variable base,
    conditionally followed by variable indexes.
    """

    def __init__(self, base: VariableBase, *args):
        """Initializes a variable.

        Args:
            base (VariableBase): The variable base (cf. class :class:´VariableBase´).
            *args: Variable length list of index elements (cf. class :class:´VariableIndexes´).
        """
        # TODO: Implement type coercion
        self._base = coerce(base, VariableBase)
        f = flatten(*args)
        if f is not None and f != [None]:
            self._indexes = coerce(f, VariableIndexes)
        else:
            self._indexes = None

        super().__init__(base, *args)

    def represent(self, rformat: str = None, *args, **kwargs) -> str:
        if rformat is None:
            rformat = rformats.DEFAULT
        # TODO: Minor bug: only digits are currently supported by subscript().
        return represent(self._base, rformat) + \
               represent(self._indexes, rformat)
