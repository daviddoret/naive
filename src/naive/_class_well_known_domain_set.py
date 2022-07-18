from __future__ import annotations
import typing

from _class_persisting_representable import PersistingRepresentable, CoerciblePersistingRepresentable
from _class_well_known_domain import WellKnownDomain
from _class_set import Set
from _abc_representable import ABCRepresentable
from _function_coerce import coerce
import glyphs
import log
import boolean_algebra_1
import keywords


class WellKnownDomainSet(Set):
    """A set of function domains or codomains.

    A function domain or codomain is a set.
    But mathematical functions are most frequently defined from a subset of well-known domains and codomains.
    It thus seems reasonable to expose a set of well-know domains and codomains to facilitate the manipulation of functions.
    """
    # TODO: Implement this as well as a dictionary.

    def __init__(self, **kwargs):
        kwargs[keywords.set_dimensions] = 1  # Forces the set dimensions property.
        super().__init__(**kwargs)
        self._b = boolean_algebra_1.b  # WellKnownDomain(glyphs.mathbb_b_uppercase)
        self._b_2 = boolean_algebra_1.b_2  # WellKnownDomain(glyphs.mathbb_b_uppercase, exponent=2, dimensions=2)
        self._n0 = WellKnownDomain(base_name=glyphs.mathbb_n_uppercase, indexes=0, dimensions=1)
        self._n1 = WellKnownDomain(base_name=glyphs.mathbb_n_uppercase, indexes=1, dimensions=1)
        self._z = WellKnownDomain(base_name=glyphs.mathbb_z_uppercase, dimensions=1)

    @property
    def b(self):
        """"The boolean domain.

        Returns:
            WellKnownDomain: The boolean domain.
        """
        return self._b

    @property
    def b_2(self):
        """"The boolean domain squared.

        Returns:
            WellKnownDomain: The boolean domain squared.
        """
        return self._b_2

    @property
    def n0(self):
        """The natural numbers' domain, 0 inclusive.

        Returns:
            WellKnownDomain: The natural numbers' domain, 0 inclusive.
        """
        return self._n0

    @property
    def n1(self):
        """The natural numbers' domain, 0 exclusive.

        Returns:
            WellKnownDomain: The natural numbers' domain, 0 exclusive.
        """
        return self._n1

    @property
    def z(self):
        """The integer numbers domain.

        Returns:
            WellKnownDomain: The integer numbers domain.
        """
        return self._z


domains = WellKnownDomainSet()
"""The set of well-known function domains."""


d = domains
"""A shorthand alias for the set of well-known function domains."""
