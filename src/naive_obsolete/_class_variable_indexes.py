# from collections.abc import Iterable
from _abc_representable import ABCRepresentable
from _function_represent import represent
from _function_subscriptify import subscriptify
from _function_flatten import flatten
from _function_coerce_from_kwargs import coerce_from_kwargs
from _function_coerce import coerce
import notation
import keywords


class VariableIndexes(ABCRepresentable):
    """The set of indexes that uniquely identify a variable base_name name within its scope_key."""

    def __init__(self, source=None, **kwargs):
        indexes = kwargs.get(keywords.variable_indexes) if keywords.variable_indexes in kwargs else None
        self._indexes = []
        indexes = flatten(source, indexes)
        if len(indexes) != 0:
            for index in indexes:
                # TODO: Implement type Index and check it with isinstance(). It was temporarily implemented here as strings.
                self._indexes.append(str(index))
        else:
            self._indexes = None

    def __iter__(self):
        return self._indexes.__iter__()

    def represent(self, rformat: str = None, **kwargs) -> str:
        rformat = coerce(rformat, str)
        #return subscriptify(
        #    '' if self._indexes is None else notation.VARIABLE_INDEXES_SEPARATOR.join(
        #        [represent(indexes, rformat) for indexes in self._indexes])
        #        ,rformat)
        return '' if self._indexes is None else notation.VARIABLE_INDEXES_SEPARATOR.join(
                [represent(index, rformat) for index in self._indexes])
