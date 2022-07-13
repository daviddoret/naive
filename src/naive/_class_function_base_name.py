from __future__ import annotations
import typing
from _class_persisting_representable import PersistingRepresentable


class FunctionBaseName(PersistingRepresentable):
    """A function base_name name is the first component of a function name."""

    def __init__(self, representable: (None, CoercibleFunctionBaseName) = None, *args, **kwargs):
        # TODO: Assure that the representable is a word or glyph. We don't want an indexed variable or other inadequate construction to be used a variable base_name.
        # TODO: If representable is None, implement an automatic naming scheme, e.g. x1, x2, x3, ...
        super().__init__(representable, *args, **kwargs)


"""Safe types for type coercion."""
CoercibleFunctionBaseName = typing.TypeVar(
    'CoercibleFunctionBaseName',
    FunctionBaseName,
    str
)
