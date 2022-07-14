from _ba_class_boolean_value import BooleanValue
from _ba_class_boolean_value_set import bv
from _function_coerce import coerce
from _class_function import Function
from _class_well_known_domain_set import d
import glyphs


def conjunction_algorithm(x1: BooleanValue, x2: BooleanValue) -> BooleanValue:
    """The conjunction boolean function.

    Args:
        x1 (BooleanValue): A boolean value.
        x2 (BooleanValue): A boolean value.

    Returns:
        BooleanValue: The conjunction of **x1** and **x2**.
    """
    x1 = coerce(x1, BooleanValue)
    x2 = coerce(x2, BooleanValue)
    if x1 == bv.truth and x2 == bv.truth:
        return bv.truth
    else:
        return bv.falsum


conjunction = Function(d.b_2, d.b, conjunction_algorithm, glyphs.logical_conjunction)


land = conjunction
"""An alias for **conjunction**. 'and' being a reserved word in python, the name 'land' is used instead."""
