from _function_coerce import coerce
import glyphs
import boolean_algebra_1 as ba1

# TODO: Create a BA2 enriched with all non-primary boolean functions.


def material_equivalence_algorithm(x1: ba1.BooleanValue, x2: ba1.BooleanValue) -> ba1.BooleanValue:
    """The material equivalence boolean function.

    Bibliography:
        * https://en.wikipedia.org/wiki/If_and_only_if

    Args:
        x1 (BooleanValue): A boolean value.
        x2 (BooleanValue): A boolean value.

    Returns:
        BooleanValue: The material_equivalence of **x1** and **x2**.
    """
    x1 = coerce(x1, ba1.BooleanValue)
    x2 = coerce(x2, ba1.BooleanValue)
    if x1 == x2:
        return ba1.truth
    else:
        return ba1.falsum


material_equivalence = ba1.BooleanFunction(
    arity=2,
    domain=ba1.b_2,
    algorithm=material_equivalence_algorithm,
    base_name=glyphs.logical_material_equivalence)

iif = material_equivalence
