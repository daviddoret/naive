from __future__ import annotations
from abc import ABC, abstractmethod
import src.naive.notation as settings
import src.naive.variable as variable
import src.naive.coerce as coerce
import src.naive.domain_library as domain


class VariableDefinition(ABC):
    """An abstract class for anything that may be used as variable value content, e.g. a constant, an binary_unknown value, or a formula."""

    @property
    @abstractmethod
    def domain(self) -> domain.Domain:
        pass


class Constant(VariableDefinition):
    """An abstract class for constant value contents."""
    pass


class BinaryUnknown(VariableDefinition):
    """A special value for binary_unknown values.

    Todo:
        * Consider implementing this as a singleton."""

    def __str__(self):
        return settings.UNKNOWN_NOTATION

    @property
    def domain(self) -> domain.Domain:
        return domain.domains.b


"""The 'binary_unknown value' special constant."""
binary_unknown = BinaryUnknown()
