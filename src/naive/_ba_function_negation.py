from _ba_class_boolean_value import BooleanValue
from _ba_class_boolean_domain import b
from _function_coerce import coerce
from _ba_class_function import BooleanFunction
import glyphs


def negation_algorithm(x: BooleanValue) -> BooleanValue:
    """The negation boolean function.

    Args:
        x (BooleanValue): A boolean value.

    Returns:
        BooleanValue: The negation of **x**.
    """
    x = coerce(x, BooleanValue)
    if x == b.truth:
        return b.falsum
    else:
        return b.truth


negation = BooleanFunction(
    arity=1,
    domain=b,
    algorithm=negation_algorithm,
    base_name=glyphs.logical_negation)
"""The negation boolean function.

Args:
    x (BooleanValue): A boolean value.

Returns:
    BooleanValue: The negation of **x**.
"""

lnot = negation
"""An alias for **negation**. 'not' being a reserved word in python, the name 'lnot' is used instead."""
