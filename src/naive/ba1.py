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

