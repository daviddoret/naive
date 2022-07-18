from _ba1_class_boolean_value import BooleanValue
from _ba1_class_boolean_domain import b
from _function_coerce import coerce
from _class_function import Function
from _class_well_known_domain_set import d
import glyphs


def _not_b_b(x: BooleanValue) -> BooleanValue:
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


not_b_b = Function(d.b, d.b, _not_b_b, glyphs.logical_negation)
