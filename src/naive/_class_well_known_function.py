from __future__ import annotations
import typing

from _class_well_known_domain_set import d
from _class_function import Function
from _class_set import Set
from _function_coerce import coerce
from _function_not_b_b import not_b_b
import glyphs
import log


class WellKnownFunctionSet(Set):
    """A set of well-known functions."""

    # TODO: Implement this as well as a dictionary.

    def __init__(self):
        pass

    @property
    def not_b_b(self):
        """"The boolean domain.

        Returns:
            WellKnownDomain: The boolean domain.
        """
        return self._not_b_b


functions = WellKnownFunctionSet()
"""The set of well-known functions."""

f = functions
"""A shorthand alias for the set of well-known functions."""
