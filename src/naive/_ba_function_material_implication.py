from _ba_class_boolean_value import BooleanValue
from _ba_class_boolean_domain import b
from _ba_data_boolean_domain_2 import b_2
from _function_coerce import coerce
from _class_function import Function
import glyphs


def material_implication_algorithm(x1: BooleanValue, x2: BooleanValue) -> BooleanValue:
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
    if x1 == b.falsum or (x1 == b.truth and x2 == b.truth):
        return b.truth
    else:
        return b.falsum


material_implication = Function(b_2, b, material_implication_algorithm, glyphs.logical_material_implication)


implies = material_implication
