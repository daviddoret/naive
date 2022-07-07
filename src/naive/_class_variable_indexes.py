from _abc_representable import ABCRepresentable
from _function_get_representation import get_representation
from _function_subscriptify import subscriptify
import notation


class VariableIndexes(ABCRepresentable):
    """The set of indexes that uniquely identify a variable base name within its scope."""

    def __init__(self, *args, **kwargs):
        self._indexes = []
        for index in args:
            # TODO: Implement type Index and check it with isinstance().
            self._indexes.append(index)

    def get_representation(self, rformat: str = None, *args, **kwargs) -> str:
        return subscriptify(
            notation.VARIABLE_INDEXES_SEPARATOR.join(
                [get_representation(index, rformat) for index in self._indexes])
                ,rformat)
