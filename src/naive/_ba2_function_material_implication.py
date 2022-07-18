from _function_coerce import coerce
import glyphs
import boolean_algebra_1 as ba1

# TODO: Create a BA2 enriched with all non-primary boolean functions.

def material_implication_algorithm(x1: ba1.BooleanValue, x2: ba1.BooleanValue) -> ba1.BooleanValue:
    """The material implication boolean function.

    Bibliography:
        * https://en.wikipedia.org/wiki/Material_conditional

    Args:
        x1 (BooleanValue): A boolean value.
        x2 (BooleanValue): A boolean value.

    Returns:
        BooleanValue: The material_implication of **x1** and **x2**.
    """
    x1 = coerce(x1, ba1.BooleanValue)
    x2 = coerce(x2, ba1.BooleanValue)
    if x1 == ba1.falsum or (x1 == ba1.truth and x2 == ba1.truth):
        return ba1.truth
    else:
        return ba1.falsum


material_implication = ba1.BooleanFunction(
    arity=2,
    domain=ba1.b_2,
    algorithm=material_implication_algorithm,
    base_name=glyphs.logical_material_implication)

implies = material_implication
