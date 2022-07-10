# from collections.abc import Iterable
from _abc_representable import ABCRepresentable
from _function_represent import represent
from _function_subscriptify import subscriptify
from _function_flatten import flatten
import notation


class VariableIndexes(ABCRepresentable):
    """The set of indexes that uniquely identify a variable base name within its scope."""

    def __init__(self, *args):
        self._indexes = []
        for index in flatten(args):
            # TODO: Implement type Index and check it with isinstance(). It was temporarily implemented here as strings.
            self._indexes.append(str(index))

    def __iter__(self):
        return self._indexes.__iter__()

    def represent(self, rformat: str = None, *args, **kwargs) -> str:
        return subscriptify(
            notation.VARIABLE_INDEXES_SEPARATOR.join(
                [represent(index, rformat) for index in self._indexes])
                ,rformat)
