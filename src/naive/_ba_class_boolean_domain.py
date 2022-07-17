from __future__ import annotations
import typing

from _class_persisting_representable import PersistingRepresentable, CoerciblePersistingRepresentable
from _ba_class_boolean_value import BooleanValue
from _abc_representable import ABCRepresentable
from _function_coerce import coerce
from _class_well_known_domain import WellKnownDomain
from _class_variable import Variable,VariableIndexes,VariableExponent,VariableBaseName
import glyphs
import log


class BooleanDomain(WellKnownDomain):
    # TODO: Enrich the Set class as a python dictionary and adapt this class.
    """A Boolean domain is a set consisting of exactly two elements whose interpretations include false and true.

    Bibliography:
        * https://en.wikipedia.org/wiki/Boolean_domain
    """

    def __init__(self):
        variable_base_name = glyphs.mathbb_b_uppercase
        super().__init__(base_name=variable_base_name)
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


boolean_domain = BooleanDomain()
"""The Boolean domain is the set consisting of exactly two elements whose interpretations include false and true.

Bibliography:
    * https://en.wikipedia.org/wiki/Boolean_domain
"""


b = boolean_domain
"""A shorthand alias for the Boolean domain.

The Boolean domain is the set consisting of exactly two elements whose interpretations include false and true.

Bibliography:
    * https://en.wikipedia.org/wiki/Boolean_domain
"""

truth = boolean_domain.truth
falsum = boolean_domain.falsum
t = boolean_domain.t
f = boolean_domain.f
