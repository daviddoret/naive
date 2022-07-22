from __future__ import annotations
import log
import core



_SCOPE_BA1 = 'ba1'

_LANGUAGE_BA1 = 'ba1'

# Language.
ba1 = core.Language(
    scope_key=_SCOPE_BA1, structure_key=core._STRUCTURE_LANGUAGE, language_key=_LANGUAGE_BA1, base_key='ba1',
    utf8='ba1', latex=r'\text{ba1}', html='ba1', usascii='ba1')

# Domains.
b = core.Domain(
    scope_key=_SCOPE_BA1, structure_key=core._STRUCTURE_DOMAIN, language_key=_LANGUAGE_BA1, base_key='b',
    utf8='𝔹', latex=r'\mathbb{B}', html='&Bopf;', usascii='B')
b2 = core.Domain(
    scope_key=_SCOPE_BA1, structure_key=core._STRUCTURE_DOMAIN, language_key=_LANGUAGE_BA1, base_key='b2',
    utf8='𝔹²', latex=r'\mathbb{B}^{2}', html=r'&Bopf;<sup>2</sup>', usascii='B2')

# Functions.
truth = core.Function(
    scope_key=_SCOPE_BA1, structure_key=core._STRUCTURE_FUNCTION, language_key=_LANGUAGE_BA1, base_key='truth',
    codomain=b, category=core.FUNCTION, subcategory=core.CONSTANT,
    utf8='⊤', latex=r'\top', html='&top;', usascii='truth', tokens=['⊤', 'truth', 'true', 't', '1'],
    arity=0, python_value=True)
falsum = core.Function(
    scope_key=_SCOPE_BA1, structure_key=core._STRUCTURE_FUNCTION, language_key=_LANGUAGE_BA1, base_key='falsum',
    codomain=b, category=core.FUNCTION, subcategory=core.CONSTANT,
    utf8='⊥', latex=r'\bot', html='&perp;', usascii='falsum', tokens=['⊥', 'falsum', 'false', 'f', '0'],
    arity=0, python_value=False)
negation = core.Function(
    scope_key=_SCOPE_BA1, structure_key=core._STRUCTURE_FUNCTION, language_key=_LANGUAGE_BA1, base_key='negation',
    codomain=b, category=core.FUNCTION, subcategory=core.UNARY_OPERATOR,
    utf8='¬', latex=r'\lnot', html='&not;', usascii='not', tokens=['¬', 'not', 'lnot'],
    domain=b, arity=1)
conjunction = core.Function(
    scope_key=_SCOPE_BA1, structure_key=core._STRUCTURE_FUNCTION, language_key=_LANGUAGE_BA1, base_key='conjunction',
    codomain=b, category=core.FUNCTION, subcategory=core.BINARY_OPERATOR,
    utf8='∧', latex=r'\land', html='&and;', usascii='and', tokens=['∧', 'and', 'land'],
    domain=b, arity=2)
disjunction = core.Function(
    scope_key=_SCOPE_BA1, structure_key=core._STRUCTURE_FUNCTION, language_key=_LANGUAGE_BA1, base_key='disjunction',
    codomain=b, category=core.FUNCTION, subcategory=core.BINARY_OPERATOR,
    utf8='∨', latex=r'\lor', html='&or;', usascii='or', tokens=['∨', 'or', 'lor'],
    domain=b, arity=2)


def b(token):
    global falsum
    global truth
    token = str(token)
    if token in falsum.tokens:
        return falsum
    elif token in truth.tokens:
        return truth
    else:
        log.error('Unrecognized token')


def constant(token):
    return b(token)


def function(token):
    token = str(token)
    if token in falsum.tokens:
        return falsum
    elif token in truth.tokens:
        return truth
    else:
        log.error('Unrecognized token')
