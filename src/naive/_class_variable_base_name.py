from __future__ import annotations
import typing
from _abc_representable import ABCRepresentable
from _class_persisting_representable import PersistingRepresentable
from _function_coerce_from_kwargs import coerce_from_kwargs
import keywords


class VariableBaseName(PersistingRepresentable):
    """A variable base_name is the first component of a variable name.

    Kwargs:
        source_representable (None, CoercibleVariableBaseName): A source_representable object for the variable.
    """

    def __init__(self, source=None, **kwargs):
        # TODO: Assure that the source_representable is a word or glyph. We don't want an indexed variable or other inadequate construction to be used a variable base_name.
        # TODO: If source_representable is None, implement an automatic naming scheme, e.g. x1, x2, x3, ...
        super().__init__(source, **kwargs)


"""Safe types for type coercion."""
CoercibleVariableBaseName = typing.TypeVar(
    'CoercibleVariableBaseName',
    VariableBaseName,
    str
)
