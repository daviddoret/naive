import logging

import flit

import log
import src.naive as naive
from src.naive.boolean_algebra_1 import *

log.logger.setLevel(logging.DEBUG)

b1 = BooleanAtomicVariable(base_name='b', indexes=1)
b2 = BooleanAtomicVariable(base_name='b', indexes=2)
b3 = BooleanAtomicVariable(base_name='b', indexes=3)
psi1 = BooleanFormula(
    symbol=conjunction
    , arguments=[b1, b2]
)
psi2 = BooleanFormula(
    symbol=disjunction
    , arguments=[b3, b1]
)
psi3 = BooleanFormula(
    symbol=conjunction
    , arguments=[psi1, psi2]
)


def get_bool_combinations(n):
    """
    Bibliography:
        * https://stackoverflow.com/questions/9945720/python-extracting-bits-from-a-byte
    """
    # TODO: Assure endianness consistency.
    return [[(integer_value & 1 << bit_position != 0) for bit_position in range(0, n)] for integer_value in
            range(0, 2 ** n)]


def get_bool_combinations_column(n, c):
    """
    Bibliography:
        * https://stackoverflow.com/questions/9945720/python-extracting-bits-from-a-byte
    """
    # TODO: Assure endianness consistency.
    return [(integer_value & 1 << c != 0) for integer_value in range(0, 2 ** n)]


def get_boolean_combinations(n):
    """
    Bibliography:
        * https://stackoverflow.com/questions/9945720/python-extracting-bits-from-a-byte
    """
    # TODO: Assure endianness consistency.
    return [[(truth if (integer_value & 1 << bit_position != 0) else falsum) for bit_position in range(0, n)] for
            integer_value in range(0, 2 ** n)]


def get_boolean_combinations_column(n, c):
    """
    Bibliography:
        * https://stackoverflow.com/questions/9945720/python-extracting-bits-from-a-byte
    """
    # TODO: Assure endianness consistency.
    return [(truth if (integer_value & 1 << c != 0) else falsum) for integer_value in range(0, 2 ** n)]


def execute_formula_exhaustively(f: BooleanFormula):
    # Retrieve the set of variables present in the phi.
    variables_list = f.list_atomic_variables()
    log.debug(variables_list=str(variables_list))
    # Retrieve the number of variables in the set.
    variables_number = len(variables_list)
    log.debug(variables_number=variables_number)
    # Populate an initial execution table with all combinations of variable values.
    # Note: this table is not necessary because bit values may be computed on the fly.
    # TODO: Assure endianness consistency, otherwise the table may be flipped on some systems.
    execution_table = get_boolean_combinations(variables_number)
    log.debug(execution_table=str(execution_table))
    # TODO: CONTINUE HERE
    # Start from the leafs of the tree, then move up.
    # To do this, make a recursive execution, and pass the execution table.


def satisfaction_set(formula: BooleanFormula, variables_list=None):
    # Retrieve the computed results
    if variables_list is None:
        variables_list = formula.list_atomic_variables()
    variables_number = len(variables_list)
    arguments_number = formula.arity
    argument_vectors = [None] * arguments_number
    log.debug(arguments_number=arguments_number)
    for argument_index in range(0, arguments_number):
        argument = formula.arguments[argument_index]
        log.debug(argument=argument, argument_index=argument_index)
        if isinstance(argument, BooleanFormula):
            # The argument is a phi.
            # Recursively compute that phi.
            vector = compute_formula(argument, variables_list=variables_list)
            log.debug(t='phi', vector=vector)
            argument_vectors[argument_index] = vector
        elif isinstance(argument, BooleanAtomicVariable):
            # The argument is an atomic proposition.
            # We want to retrieve its values from the corresponding bit combinations column.
            # But we need the vector to be relative to variables_list.
            # Thus we must first find the position of this atomic variable,
            # in the variables_list.
            atomic_variable_index = variables_list.index(argument)
            vector = get_boolean_combinations_column(variables_number, atomic_variable_index)
            log.debug(t='atomic variable', vector=vector)
            argument_vectors[argument_index] = vector
        else:
            log.error('Unexpected type', argument=argument, t=type(argument))
    log.info(argument_vectors=argument_vectors)
    output_vector = None
    match formula.arity:
        case 0: output_vector = formula.symbol.algorithm(vector_size = 2 ** variables_number)
        case 1: output_vector = formula.symbol.algorithm(argument_vectors[0])
        case 2: output_vector = formula.symbol.algorithm(argument_vectors[0], argument_vectors[1])
        case _: log.error('Arity > 2 are not yet supported, sorry')
    log.info(output_vector=output_vector)
    return output_vector


psi_test = psi3
log.info(formula=psi_test, vars=psi_test.list_atomic_variables())
compute_formula(psi_test, variables_list = None)
