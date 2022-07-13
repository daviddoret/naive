from __future__ import annotations
import typing

from _class_persisting_representable import PersistingRepresentable, CoerciblePersistingRepresentable
from _class_boolean_value import BooleanValue
from _abc_representable import ABCRepresentable
from _function_coerce import coerce
import glyphs
import log


class BooleanValueSet:
    # TODO: Implement this as well as a dictionary.
    # TODO: Then, reuse that structure for NN0, NN1, etc.

    def __init__(self):
        self._falsum = BooleanValue(False)
        self._truth = BooleanValue(True)

    @property
    def falsum(self):
        """BooleanValue: The falsum boolean value."""
        return self._falsum

    @property
    def truth(self):
        """BooleanValue: The truth boolean value."""
        return self._truth

    @property
    def f(self):
        """BooleanValue: A shorthand for the falsum boolean value."""
        return self.falsum

    @property
    def t(self):
        """BooleanValue: A shorthand for the truth boolean value."""
        return self.truth


boolean_values = BooleanValueSet()
"""The set of boolean values."""


bv = boolean_values
"""A shorthand alias for the set of boolean values."""
