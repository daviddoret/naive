from _abc_representable import ABCRepresentable
import notation


class VariableIndexes(ABCRepresentable):
    """The set of indexes that uniquely identify a variable base name within its scope."""

    def __init__(self, *args, **kwargs):
        self._indexes = []
        for index in args:
            # TODO: Implement type Index and check it with isinstance().
            self._indexes.append(index)

    @property
    def utf8(self) -> str:
        return notation.VARIABLE_INDEXES_SEPARATOR.join([index.utf8 for index in self._indexes])

    @property
    def latex(self) -> str:
        return notation.VARIABLE_INDEXES_SEPARATOR.join([index.latex for index in self._indexes])

    @property
    def html(self) -> str:
        return notation.VARIABLE_INDEXES_SEPARATOR.join([index.html for index in self._indexes])

    @property
    def ascii(self) -> str:
        return notation.VARIABLE_INDEXES_SEPARATOR.join([index.ascii for index in self._indexes])

