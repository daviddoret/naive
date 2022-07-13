# from collections.abc import Iterable
from _abc_representable import ABCRepresentable
from _function_represent import represent
from _function_superscriptify import superscriptify
from _function_flatten import flatten
import notation


class VariablePower(ABCRepresentable):
    """The set of powers that uniquely identify a variable base_name name within its scope."""

    def __init__(self, power):
        self._power = power

    def represent(self, rformat: str = None, *args, **kwargs) -> str:
        return superscriptify(self._power, rformat)
