from _function_superscriptify import superscriptify
import keywords
from _class_persisting_representable import PersistingRepresentable


class VariableExponent(PersistingRepresentable):
    """A variable exponent.

    A variable exponent is an ambiguous notation.
    A variable exponent is distinct from an exponentiation.
    A variable exponent means n-ary cartesian cross product.
    For instance, 𝔹⁴ means (𝔹 × 𝔹 × 𝔹 × 𝔹) and not 𝔹 to the 4th exponent."""

    def __init__(self, source = None, **kwargs):
        super().__init__(source, **kwargs)
        # exponent = kwargs[keywords.variable_exponent]  # TODO: Implement type coercion.
        # self._exponent = exponent

    #def represent(self, rformat: str = None, *args, **kwargs) -> str:
    #    return superscriptify(self.represent(rformat), rformat)
