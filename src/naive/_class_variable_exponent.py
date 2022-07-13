# from collections.abc import Iterable
from _abc_representable import ABCRepresentable
from _function_represent import represent
from _function_superscriptify import superscriptify
from _function_flatten import flatten
import notation


class VariableExponent(ABCRepresentable):
    """A variable exponent.

    A variable exponent is an ambiguous notation.
    A variable exponent is distinct from an exponentiation.
    A variable exponent means n-ary cartesian cross product.
    For instance, 𝔹⁴ means (𝔹 × 𝔹 × 𝔹 × 𝔹) and not 𝔹 to the 4th power."""

    def __init__(self, exponent):
        self._exponent = exponent

    def represent(self, rformat: str = None, *args, **kwargs) -> str:
        return superscriptify(self._exponent, rformat)
