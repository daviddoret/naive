from __future__ import annotations
import typing

# Naive imports
import log
import core
from _function_flatten import flatten
from _function_superscriptify import superscriptify


_SCOPE_BA1 = 'sys_ba1'
_LANGUAGE_BA1 = 'ba1_language'

# Dirty little trick to overcome circular references
# between algorithm function definitions,
# and system function definitions.
# These global variables are overwritten at the end
# of this module.
truth = None
falsum = None

# Algorithms.
def falsum_algorithm(vector_size: int = 1) -> typing.List[core.SystemFunction]:
    """The vectorized falsum boolean function.

    Returns:
        BooleanConstant: The boolean falsum.
    """
    global falsum
    return [falsum] * vector_size

def truth_algorithm(vector_size: int = 1) -> typing.List[core.SystemFunction]:
    """The vectorized truth boolean function.

    Returns:
        BooleanConstant: The boolean truth.
    """
    global truth
    return [truth] * vector_size

def negation_algorithm(v: typing.List[core.SystemFunction]) -> typing.List[core.SystemFunction]:
    """The vectorized negation boolean function.

    Args:
        v (typing.List[BooleanConstant]): A vector of boolean constants.

    Returns:
        typing.List[BooleanConstant]: A vector of the negation of **x**.
    """
    global truth
    global falsum
    # v = coerce(v, BooleanConstant)  # TODO: Consider support for list coercion.
    v = flatten(v)  # If scalar, convert to list.
    return [falsum if e == truth else truth for e in v]

def conjunction_algorithm(
        v1: typing.List[core.SystemFunction],
        v2: typing.List[core.SystemFunction]) -> \
        typing.List[core.SystemFunction]:
    """The vectorized conjunction boolean function.

    Args:
        v1 (typing.List[BooleanConstant]): A vector of boolean constants.
        v2 (typing.List[BooleanConstant]): A vector of boolean constants.

    Returns:
        typing.List[BooleanConstant]: The vector of the conjunction of **v1** and **v2**.
    """
    global truth
    global falsum
    # v1 = coerce(v1, BooleanConstant)  # TODO: Consider support for list coercion.
    # v2 = coerce(v2, BooleanConstant)  # TODO: Consider support for list coercion.
    v1 = flatten(v1)  # If scalar, convert to list.
    v2 = flatten(v2)  # If scalar, convert to list.
    return [truth if (b1 == truth and b2 == truth) else falsum for b1, b2 in zip(v1, v2)]

def disjunction_algorithm(
        v1: typing.List[core.SystemFunction],
        v2: typing.List[core.SystemFunction]) -> \
        typing.List[core.SystemFunction]:
    """The vectorized disjunction boolean function.

    Args:
        v1 (typing.List[BooleanConstant]): A vector of boolean constants.
        v2 (typing.List[BooleanConstant]): A vector of boolean constants.

    Returns:
        typing.List[BooleanConstant]: The vector of the disjunction of **v1** and **v2**.
    """
    global truth
    global falsum
    # v1 = coerce(v1, BooleanConstant)  # TODO: Consider support for list coercion.
    # v2 = coerce(v2, BooleanConstant)  # TODO: Consider support for list coercion.
    v1 = flatten(v1)  # If scalar, convert to list.
    v2 = flatten(v2)  # If scalar, convert to list.
    return [truth if (b1 == truth or b2 == truth) else falsum for b1, b2 in zip(v1, v2)]

# Scope.
ba1_scope = core.Scope(
    scope_key=_SCOPE_BA1, structure_key=core._STRUCTURE_SCOPE, language_key=_LANGUAGE_BA1, base_key='ba1_language',
    utf8='ba1_language', latex=r'\text{ba1_language}', html='ba1_language', usascii='ba1_language')

# Language.
ba1_language = core.Language(
    scope_key=_SCOPE_BA1, structure_key=core._STRUCTURE_LANGUAGE, language_key=_LANGUAGE_BA1,
    base_key='ba1_language',
    utf8='ba1_language', latex=r'\text{ba1_language}', html='ba1_language', usascii='ba1_language')

# Domains.
b = core.Domain(
    scope_key=_SCOPE_BA1, structure_key=core._STRUCTURE_DOMAIN, language_key=_LANGUAGE_BA1, base_key='b',
    utf8='𝔹', latex=r'\mathbb{B}', html='&Bopf;', usascii='B')
b2 = core.Domain(
    scope_key=_SCOPE_BA1, structure_key=core._STRUCTURE_DOMAIN, language_key=_LANGUAGE_BA1, base_key='b2',
    utf8='𝔹²', latex=r'\mathbb{B}^{2}', html=r'&Bopf;<sup>2</sup>', usascii='B2')

def get_bn_domain(n):
    """Returns the n-tuple codomain 𝔹ⁿ where n is a natural number > 0.

    Assures the presence of the codomain 𝔹ⁿ in the concept database.
    """
    if not isinstance(n, int):
        log.error('n must be an int')
    elif n < 1:
        log.error('n must be > 1')
    elif n == 1:
        return b
    elif n == 2:
        return b2
    else:
        scope_key = _SCOPE_BA1
        structure_key = core._STRUCTURE_DOMAIN
        language_key = _LANGUAGE_BA1
        base_key = 'b' + str(n)  # TODO: Check it is an int
        # TODO: Consider implementing a lock to avoid bugs with multithreading when checking the static dictionary
        if core.Concept.check_concept_from_decomposed_key(scope_key=scope_key, structure_key=structure_key,
                                                          language_key=language_key, base_key=base_key):
            return core.Concept.get_concept_from_decomposed_key(scope_key=scope_key,
                                                                structure_key=core.structure_key,
                                                                language_key=language_key, base_key=base_key)
        else:
            return core.Domain(
                scope_key=scope_key, structure_key=structure_key, language_key=language_key, base_key=base_key,
                utf8='𝔹' + superscriptify(n), latex=r'\mathbb{B}^{' + str(n) + r'}',
                html=r'&Bopf;<sup>' + str(n) + '</sup>', usascii='B' + str(n))

# Functions.
truth = core.SystemFunction(
    scope_key=_SCOPE_BA1, structure_key=core._STRUCTURE_FUNCTION, language_key=_LANGUAGE_BA1, base_key='truth',
    codomain=b, category=core.SystemFunction.SYSTEM_CONSTANT, algorithm=truth_algorithm,
    utf8='⊤', latex=r'\top', html='&top;', usascii='truth', tokens=['⊤', 'truth', 'true', 't', '1'],
    arity=0, python_value=True)
falsum = core.SystemFunction(
    scope_key=_SCOPE_BA1, structure_key=core._STRUCTURE_FUNCTION, language_key=_LANGUAGE_BA1, base_key='falsum',
    codomain=b, category=core.SystemFunction.SYSTEM_CONSTANT, algorithm=falsum_algorithm(),
    utf8='⊥', latex=r'\bot', html='&perp;', usascii='falsum', tokens=['⊥', 'falsum', 'false', 'f', '0'],
    arity=0, python_value=False)
negation = core.SystemFunction(
    scope_key=_SCOPE_BA1, structure_key=core._STRUCTURE_FUNCTION, language_key=_LANGUAGE_BA1, base_key='negation',
    codomain=b, category=core.SystemFunction.SYSTEM_UNARY_OPERATOR, algorithm=negation_algorithm,
    utf8='¬', latex=r'\lnot', html='&not;', usascii='not', tokens=['¬', 'not', 'lnot'],
    domain=b, arity=1)
conjunction = core.SystemFunction(
    scope_key=_SCOPE_BA1, structure_key=core._STRUCTURE_FUNCTION, language_key=_LANGUAGE_BA1,
    base_key='conjunction',
    codomain=b, category=core.SystemFunction.SYSTEM_BINARY_OPERATOR, algorithm=conjunction_algorithm,
    utf8='∧', latex=r'\land', html='&and;', usascii='and', tokens=['∧', 'and', 'land'],
    domain=b, arity=2)
disjunction = core.SystemFunction(
    scope_key=_SCOPE_BA1, structure_key=core._STRUCTURE_FUNCTION, language_key=_LANGUAGE_BA1,
    base_key='disjunction',
    codomain=b, category=core.SystemFunction.SYSTEM_BINARY_OPERATOR, algorithm=disjunction_algorithm,
    utf8='∨', latex=r'\lor', html='&or;', usascii='or', tokens=['∨', 'or', 'lor'],
    domain=b, arity=2)
