from _ba_class_boolean_value import BooleanValue
from _ba_class_boolean_value_set import bv
from _function_coerce import coerce
from _class_function import Function
from _class_well_known_domain_set import d
import glyphs


def material_equivalence_algorithm(x1: BooleanValue, x2: BooleanValue) -> BooleanValue:
    """The material equivalence boolean function.

    Bibliography:
        * https://en.wikipedia.org/wiki/If_and_only_if

    Args:
        x1 (BooleanValue): A boolean value.
        x2 (BooleanValue): A boolean value.

    Returns:
        BooleanValue: The material_equivalence of **x1** and **x2**.
    """
    x1 = coerce(x1, BooleanValue)
    x2 = coerce(x2, BooleanValue)
    if x1 == x2:
        return bv.truth
    else:
        return bv.falsum


material_equivalence = Function(d.b_2, d.b, material_equivalence_algorithm, glyphs.logical_material_equivalence)


iif = material_equivalence
