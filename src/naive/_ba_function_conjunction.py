from _ba_class_boolean_value import BooleanValue
from _ba_class_boolean_domain import b
from _ba_data_boolean_domain_2 import b_2
from _function_coerce import coerce
from _class_function import Function
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
    if x1 == b.truth and x2 == b.truth:
        return b.truth
    else:
        return b.falsum


conjunction = Function(b_2, b, conjunction_algorithm, glyphs.logical_conjunction)


land = conjunction
"""An alias for **conjunction**. 'and' being a reserved word in python, the name 'land' is used instead."""
