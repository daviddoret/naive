from _ba_class_boolean_value import BooleanValue
from _ba_class_boolean_domain import b
from _ba_data_boolean_domain_2 import b_2
from _function_coerce import coerce
from _class_function import Function
import glyphs


def disjunction_algorithm(x1: BooleanValue, x2: BooleanValue) -> BooleanValue:
    """The disjunction boolean function.

    Args:
        x1 (BooleanValue): A boolean value.
        x2 (BooleanValue): A boolean value.

    Returns:
        BooleanValue: The disjunction of **x1** and **x2**.
    """
    x1 = coerce(x1, BooleanValue)
    x2 = coerce(x2, BooleanValue)
    if x1 == b.truth or x2 == b.truth:
        return b.truth
    else:
        return b.falsum


disjunction = Function(b_2, b, disjunction_algorithm, glyphs.logical_disjunction)


lor = disjunction
"""An alias for **disjunction**. 'or' being a reserved word in python, the name 'lor' is used instead."""