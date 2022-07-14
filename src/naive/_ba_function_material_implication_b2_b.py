from _ba_class_boolean_value import BooleanValue
from _ba_class_boolean_value_set import bv
from _function_coerce import coerce
from _class_function import Function
from _class_well_known_domain_set import d
import glyphs


def material_implication_b2_b_algorithm(x1: BooleanValue, x2: BooleanValue) -> BooleanValue:
    """The material implication boolean function.

    Bibliography:
        * https://en.wikipedia.org/wiki/Material_conditional

    Args:
        x1 (BooleanValue): A boolean value.
        x2 (BooleanValue): A boolean value.

    Returns:
        BooleanValue: The material_implication of **x1** and **x2**.
    """
    x1 = coerce(x1, BooleanValue)
    x2 = coerce(x2, BooleanValue)
    if x1 == bv.falsum or (x1 == bv.truth and x2 == bv.truth):
        return bv.truth
    else:
        return bv.falsum


material_implication_b2_b = Function(d.b_2, d.b, material_implication_b2_b_algorithm, glyphs.logical_material_implication)


implies_b2_b = material_implication_b2_b
