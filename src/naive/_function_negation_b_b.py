from _class_boolean_value import BooleanValue
from _class_boolean_value_set import bv
from _function_coerce import coerce
from _class_function import Function
from _class_well_known_domain_set import d
import glyphs


def negation_b_b_algorithm(x: BooleanValue) -> BooleanValue:
    """The negation boolean function.

    Args:
        x (BooleanValue): A boolean value.

    Returns:
        BooleanValue: The negation of **x**.
    """
    x = coerce(x, BooleanValue)
    if x == bv.truth:
        return bv.falsum
    else:
        return bv.truth


negation_b_b = Function(d.b, d.b, negation_b_b_algorithm, glyphs.logical_negation)


not_b_b = negation_b_b
