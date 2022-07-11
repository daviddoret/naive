from __future__ import annotations
import typing

import bv
import glyphs
from _class_persisting_representable import PersistingRepresentable, CoerciblePersistingRepresentable
from _abc_representable import ABCRepresentable
from _function_coerce import coerce


class BooleanValue(PersistingRepresentable):

    def __new__(cls, pythonic_value: bool):
        pythonic_value = coerce(pythonic_value, bool)
        try:
            # Try to reuse the singleton if it was already initialized.
            if pythonic_value:
                return bv.truth
            else:
                return bv.falsum
        except Exception:
            # The singleton wasn't initialized, thus initialize it.
            return super(BooleanValue, cls).__new__(cls)

    def __init__(self, pythonic_value: bool):
        """Initializes the boolean value and stores its representations in available formats.        """
        pythonic_value = coerce(pythonic_value, bool)
        self._inner_value = pythonic_value
        glyph = glyphs.standard_truth if pythonic_value else glyphs.standard_falsum
        super().__init__(glyph)

    def __bool__(self):
        """Provides support for implicit and explicit (i.e. ``bool(x)``) conversions to :std:doc:type:`bool`.

        Returns:
            bool: a pythonic bool-equivalent object.
        """
        return self._inner_value

    def __eq__(self, other: CoercibleBooleanValue) -> bool:
        """Provides explicit support for equality.

        Even though all python objects are implicitly convertible to bool (calling :std:doc:meth:`__bool__`),
        we want the equality operator to rather approach mathematical equality.
        Hence, we explicitly convert **other** to **BinaryNumber** which issues warnings and raises exceptions as necessary.

        Args:
            other(CoercibleBinaryNumber): A compatible boolean object.

        Returns:
            bool: The truth value of the equality operator.
        """
        other = coerce(other, BooleanValue)
        result = bool(self) == bool(other)  # Explicit conversion is superfluous but clearer
        return result


"""A shorthand alias for class :class:`BinaryValue`."""
BV = BooleanValue

"""Supported types for coercion to class :class:`BinaryValue`."""
CoercibleBooleanValue = typing.TypeVar(
    'CoercibleBooleanValue',
    BooleanValue,
    bool,
    int,
    str # TODO Implement coercion of well known representations.
)
