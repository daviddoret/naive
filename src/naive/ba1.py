from __future__ import annotations
import log
import core



_SCOPE_BA1 = 'sys_ba1'

_LANGUAGE_BA1 = 'ba1_language'

# Scope.
ba1_scope = core.Scope(
    scope_key=_SCOPE_BA1, structure_key=core._STRUCTURE_SCOPE, language_key=_LANGUAGE_BA1, base_key='ba1_language',
    utf8='ba1_language', latex=r'\text{ba1_language}', html='ba1_language', usascii='ba1_language')

# Language.
ba1_language = core.Language(
    scope_key=_SCOPE_BA1, structure_key=core._STRUCTURE_LANGUAGE, language_key=_LANGUAGE_BA1, base_key='ba1_language',
    utf8='ba1_language', latex=r'\text{ba1_language}', html='ba1_language', usascii='ba1_language')

# Domains.
b = core.Domain(
    scope_key=_SCOPE_BA1, structure_key=core._STRUCTURE_DOMAIN, language_key=_LANGUAGE_BA1, base_key='b',
    utf8='𝔹', latex=r'\mathbb{B}', html='&Bopf;', usascii='B')
b2 = core.Domain(
    scope_key=_SCOPE_BA1, structure_key=core._STRUCTURE_DOMAIN, language_key=_LANGUAGE_BA1, base_key='b2',
    utf8='𝔹²', latex=r'\mathbb{B}^{2}', html=r'&Bopf;<sup>2</sup>', usascii='B2')

from _function_superscriptify import superscriptify


def get_bn_domain(n):
    """Returns the n-tuple codomain_key 𝔹ⁿ where n is a natural number > 0.

    Assures the presence of the codomain_key 𝔹ⁿ in the concept database.
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
        scope_key=_SCOPE_BA1
        structure_key=core._STRUCTURE_DOMAIN
        language_key=_LANGUAGE_BA1
        base_key = 'b' + str(n)  # TODO: Check it is an int
        # TODO: Consider implementing a lock to avoid bugs with multithreading when checking the static dictionary
        if core.Concept.check_concept_from_decomposed_key(scope_key=scope_key, structure_key=structure_key, language_key=language_key, base_key=base_key):
            return core.Concept.get_concept_from_decomposed_key(scope_key=scope_key, structure_key=core.structure_key, language_key=language_key, base_key=base_key)
        else:
            return core.Domain(
                scope_key=scope_key, structure_key=structure_key, language_key=language_key, base_key=base_key,
                utf8='𝔹' + superscriptify(n), latex=r'\mathbb{B}^{' + str(n) + r'}', html=r'&Bopf;<sup>' + str(n) + '</sup>', usascii='B' + str(n))

# Functions.
truth = core.SystemFunction(
    scope_key=_SCOPE_BA1, structure_key=core._STRUCTURE_FUNCTION, language_key=_LANGUAGE_BA1, base_key='truth',
    codomain=b, category=core.SystemFunction.SYSTEM_CONSTANT,
    utf8='⊤', latex=r'\top', html='&top;', usascii='truth', tokens=['⊤', 'truth', 'true', 't', '1'],
    arity=0, python_value=True)
falsum = core.SystemFunction(
    scope_key=_SCOPE_BA1, structure_key=core._STRUCTURE_FUNCTION, language_key=_LANGUAGE_BA1, base_key='falsum',
    codomain=b, category=core.SystemFunction.SYSTEM_CONSTANT,
    utf8='⊥', latex=r'\bot', html='&perp;', usascii='falsum', tokens=['⊥', 'falsum', 'false', 'f', '0'],
    arity=0, python_value=False)
negation = core.SystemFunction(
    scope_key=_SCOPE_BA1, structure_key=core._STRUCTURE_FUNCTION, language_key=_LANGUAGE_BA1, base_key='negation',
    codomain=b, category=core.SystemFunction.SYSTEM_UNARY_OPERATOR,
    utf8='¬', latex=r'\lnot', html='&not;', usascii='not', tokens=['¬', 'not', 'lnot'],
    domain=b, arity=1)
conjunction = core.SystemFunction(
    scope_key=_SCOPE_BA1, structure_key=core._STRUCTURE_FUNCTION, language_key=_LANGUAGE_BA1, base_key='conjunction',
    codomain=b, category=core.SystemFunction.SYSTEM_BINARY_OPERATOR,
    utf8='∧', latex=r'\land', html='&and;', usascii='and', tokens=['∧', 'and', 'land'],
    domain=b, arity=2)
disjunction = core.SystemFunction(
    scope_key=_SCOPE_BA1, structure_key=core._STRUCTURE_FUNCTION, language_key=_LANGUAGE_BA1, base_key='disjunction',
    codomain=b, category=core.SystemFunction.SYSTEM_BINARY_OPERATOR,
    utf8='∨', latex=r'\lor', html='&or;', usascii='or', tokens=['∨', 'or', 'lor'],
    domain=b, arity=2)

