from _class_boolean_value import BooleanValue
from _class_boolean_value_set import bv
from _function_coerce import coerce
from _class_function import Function
from _class_well_known_domain_set import d
import glyphs


def disjunction_b2_b_algorithm(x1: BooleanValue, x2: BooleanValue) -> BooleanValue:
    """The disjunction boolean function.

    Args:
        x1 (BooleanValue): A boolean value.
        x2 (BooleanValue): A boolean value.

    Returns:
        BooleanValue: The disjunction of **x1** and **x2**.
    """
    x1 = coerce(x1, BooleanValue)
    x2 = coerce(x2, BooleanValue)
    if x1 == bv.truth or x2 == bv.truth:
        return bv.truth
    else:
        return bv.falsum


disjunction_b2_b = Function(d.b_2, d.b, disjunction_b2_b_algorithm, glyphs.logical_disjunction)


or_b2_b = disjunction_b2_b
