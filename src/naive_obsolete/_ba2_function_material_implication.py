from _function_coerce import coerce
import glyphs
import boolean_algebra_1 as ba1

# TODO: Create a BA2 enriched with all non-primary boolean functions.

def material_implication_algorithm(x1: ba1.BooleanConstant, x2: ba1.BooleanConstant) -> ba1.BooleanConstant:
    """The material implication boolean function.

    Bibliography:
        * https://en.wikipedia.org/wiki/Material_conditional

    Args:
        x1 (BooleanConstant): A boolean value.
        x2 (BooleanConstant): A boolean value.

    Returns:
        BooleanConstant: The material_implication of **v1** and **v2**.
    """
    x1 = coerce(x1, ba1.BooleanConstant)
    x2 = coerce(x2, ba1.BooleanConstant)
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
