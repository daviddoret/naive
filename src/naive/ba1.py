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
    utf8='⊤', latex=r'\top', html='&top;', usascii='truth', tokens=['⊤', 'truth', 'true', 't', '1'],
    codomain=b, arity=0, python_value=True)
falsum = core.Function(
    scope_key=_SCOPE_BA1, structure_key=core._STRUCTURE_FUNCTION, language_key=_LANGUAGE_BA1, base_key='falsum',
    utf8='⊥', latex=r'\bot', html='&perp;', usascii='falsum', tokens=['⊥', 'falsum', 'false', 'f', '0'],
    codomain=b, arity=0, python_value=False)
negation = core.Function(
    scope_key=_SCOPE_BA1, structure_key=core._STRUCTURE_FUNCTION, language_key=_LANGUAGE_BA1, base_key='negation',
    utf8='¬', latex=r'\lnot', html='&not;', usascii='not', tokens=['¬', 'not', 'lnot'],
    codomain=b, domain=b, arity=1)
conjunction = core.Function(
    scope_key=_SCOPE_BA1, structure_key=core._STRUCTURE_FUNCTION, language_key=_LANGUAGE_BA1, base_key='conjunction',
    utf8='∧', latex=r'\land', html='&and;', usascii='and', tokens=['∧', 'and', 'land'],
    codomain=b2, domain=b, arity=2)
disjunction = core.Function(
    scope_key=_SCOPE_BA1, structure_key=core._STRUCTURE_FUNCTION, language_key=_LANGUAGE_BA1, base_key='disjunction',
    utf8='∨', latex=r'\lor', html='&or;', usascii='or', tokens=['∨', 'or', 'lor'],
    codomain=b2, domain=b, arity=2)


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
