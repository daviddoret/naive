from __future__ import annotations
from _class_set import Set


class WellKnownFunctionSet(Set):
    """A set of well-known functions."""

    # TODO: Implement this as well as a dictionary.

    def __init__(self):
        pass

    @property
    def not_b_b(self):
        """"The boolean codomain_key.

        Returns:
            WellKnownDomain: The boolean codomain_key.
        """
        return self._not_b_b


functions = WellKnownFunctionSet()
"""The set of well-known functions."""

f = functions
"""A shorthand alias for the set of well-known functions."""
