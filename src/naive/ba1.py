from __future__ import annotations
import log
import core
import typing
from _function_flatten import flatten

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
            return core.Concept.get_concept_from_decomposed_key(scope_key=scope_key, structure_key=core.structure_key,
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
    scope_key=_SCOPE_BA1, structure_key=core._STRUCTURE_FUNCTION, language_key=_LANGUAGE_BA1, base_key='conjunction',
    codomain=b, category=core.SystemFunction.SYSTEM_BINARY_OPERATOR, algorithm=conjunction_algorithm,
    utf8='∧', latex=r'\land', html='&and;', usascii='and', tokens=['∧', 'and', 'land'],
    domain=b, arity=2)
disjunction = core.SystemFunction(
    scope_key=_SCOPE_BA1, structure_key=core._STRUCTURE_FUNCTION, language_key=_LANGUAGE_BA1, base_key='disjunction',
    codomain=b, category=core.SystemFunction.SYSTEM_BINARY_OPERATOR, algorithm=disjunction_algorithm,
    utf8='∨', latex=r'\lor', html='&or;', usascii='or', tokens=['∨', 'or', 'lor'],
    domain=b, arity=2)


def get_boolean_combinations_column(n, c):
    """
    Bibliography:
        * https://stackoverflow.com/questions/9945720/python-extracting-bits-from-a-byte
    """
    # TODO: Assure endianness consistency.
    return [(truth if (integer_value & 1 << c != 0) else falsum) for integer_value in range(0, 2 ** n)]


def satisfaction_index(phi: core.Formula, variables_list=None):
    """Compute the **satisfaction indexes** (:math:`\text{sat}_I`) of a Boolean formula (:math:`\phi`).

    Alias:
    **sat_i**

    Definition:
    Let :math:`\phi` be a Boolean formula.
    :math:`\text{sat}_I \colon= ` the truth value of :math:`\phi` in all possible worlds.

    Args:
        phi (BooleanFormula): The Boolean formula :math:`\phi` .
    """
    # Retrieve the computed results
    # TODO: Check that all formula are Boolean formula. Otherwise, the formula
    #   may not return a Boolean value, forbidding the computation of a satisfaction set.
    if variables_list is None:
        variables_list = phi.list_atomic_variables()
    variables_number = len(variables_list)
    arguments_number = phi.arity
    argument_vectors = [None] * arguments_number
    log.debug(arguments_number=arguments_number)
    for argument_index in range(0, arguments_number):
        argument = phi.arguments[argument_index]
        log.debug(
            argument=argument,
            argument_index=argument_index,
            argument_type=type(argument),
            argument_codomain=argument.codomain,
            argument_is_system_function_call=argument.is_system_function_call)
        if isinstance(argument, core.Formula) and \
                argument.is_system_function_call and \
                argument.codomain == b:
            # This argument is a Boolean Formula.
            log.debug('This argument is a Boolean Formula')
            # Recursively compute the satisfaction set of that formula,
            # restricting the variables list to the subset of necessary variables.
            vector = satisfaction_index(argument, variables_list=variables_list)
            argument_vectors[argument_index] = vector
        elif isinstance(argument, core.Formula) and \
                argument.category == core.Formula.ATOMIC_VARIABLE and \
                argument.codomain == b:
            # This argument is a Boolean atomic proposition.
            log.debug('This argument is a Boolean atomic proposition')
            # We want to retrieve its values from the corresponding bit combinations column.
            # But we need the vector to be relative to variables_list.
            # Thus we must first find the position of this atomic variable,
            # in the variables_list.
            atomic_variable_index = variables_list.index(argument)
            vector = get_boolean_combinations_column(variables_number, atomic_variable_index)
            log.debug(vector=vector)
            argument_vectors[argument_index] = vector
        else:
            log.error('Unexpected type', argument=argument, t=type(argument), category=argument.category,
                      codomain=argument.codomain)
    log.debug(argument_vectors=argument_vectors)
    output_vector = None
    log.debug(phi=phi, arity=phi.arity, system_function=phi.system_function)
    match phi.arity:
        case 0:
            output_vector = phi.system_function.algorithm(vector_size=2 ** variables_number)
        case 1:
            output_vector = phi.system_function.algorithm(argument_vectors[0])
        case 2:
            output_vector = phi.system_function.algorithm(argument_vectors[0], argument_vectors[1])
        case _:
            log.error('Arity > 2 are not yet supported, sorry')
    log.debug(output_vector=output_vector)
    return output_vector
