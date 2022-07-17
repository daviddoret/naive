from _ba_class_boolean_value import BooleanValue
from _ba_class_boolean_domain import b
from _ba_data_boolean_domain_2 import b_2
from _function_coerce import coerce
from _ba_class_function import BooleanFunction
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
        return b.truth
    else:
        return b.falsum


material_equivalence = BooleanFunction(
    arity=2,
    domain=b_2,
    algorithm=material_equivalence_algorithm,
    base_name=glyphs.logical_material_equivalence)

iif = material_equivalence
