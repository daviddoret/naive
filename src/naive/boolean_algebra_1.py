from __future__ import annotations
import typing
from _class_well_known_domain import WellKnownDomain
from _class_function import Function, FunctionBaseName
from _class_formula import Formula, OPERATOR, FUNCTION
from _class_atomic_variable import AtomicVariable
from _class_set import Set
import glyphs
import keywords
import log
from _function_flatten import flatten
from _function_coerce import coerce
from src.naive import Variable, CoercibleVariableBaseName, VariableIndexes, VariableExponent

_truth_initialized = False
_falsum_initialized = False


def falsum_algorithm(vector_size:int = 1) -> BooleanConstant:
    """The falsum boolean function.

    Returns:
        BooleanConstant: The boolean falsum.
    """
    global falsum
    return [falsum] * vector_size


def truth_algorithm(vector_size:int = 1) -> BooleanConstant:
    """The truth boolean function.

    Returns:
        BooleanConstant: The boolean truth.
    """
    global truth
    return [truth] * vector_size


def negation_algorithm(v: typing.List[BooleanConstant]) -> typing.List[BooleanConstant]:
    """The negation boolean function.

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


def conjunction_algorithm(v1: typing.List[BooleanConstant], v2: typing.List[BooleanConstant]) -> typing.List[BooleanConstant]:
    """The conjunction boolean function.

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


def disjunction_algorithm(v1: BooleanConstant, v2: BooleanConstant) -> BooleanConstant:
    """The disjunction boolean function.

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



class BooleanSymbol:
    """A symbol of the Boolean Algebra 1 formal language."""
    # TODO: Complete implementation. Should be necessary to implement BooleanFormula.
    pass


class BooleanAtomicVariable(AtomicVariable):
    """The Boolean atomic variable class.

    Definition:
    A Boolean atomic variable class is a boolean proposition,
    that is by definition either true or false,
    and that cannot be decomposed into subformula.
    One way to understand it is to see it as an unknown boolean variable.
    """
    # TODO: Implement contexts. This should not be linked to BA1 but rather transversal.
    def __init__(
            self,
            base_name: CoercibleVariableBaseName = None,
            indexes: VariableIndexes = None,
            exponent: VariableExponent = None,
            **kwargs):
        # TODO: Add a scope/context property and force it to B or B^n ?
        super().__init__(
            base_name=base_name,
            indexes=indexes,
            exponent=exponent,
            **kwargs)


V = BooleanAtomicVariable


class BooleanFormula(Formula):
    """A Boolean logic phi.

    *Formulas are syntactically correct expressions in a formalized language defined over a signature,
    a set of variables, and a logics. In this way, formulas are quite similar to terms.
    Since predicates and logics symbols are included in their inductive definition,
    they represent truth values instead of sort values, however.*
    -- https://encyclopediaofmath.org/wiki/Formula

    In Boolean Algebra 1, we must support:
    - BooleanAtomicProposition, i.e. an unknown value "external" to BA1
    - BooleanFormulaVariables asssigned to other BooleanFormula
    - Truth and Falsum
    - Negation
    - Conjunction and Disjunction

    Bibliography:
        * https://encyclopediaofmath.org/wiki/Formula
    """

    def __init__(
            self,
            symbol,
            arguments,
            **kwargs):
        self._symbol = symbol
        # TODO: Check that all arguments are also of type BooleanFormula
        # TODO: Check that the right number of arguments are provided for that symbol
        self._arguments = arguments
        super().__init__(symbol, arguments, **kwargs)



def get_boolean_combinations(n):
    """
    Bibliography:
        * https://stackoverflow.com/questions/9945720/python-extracting-bits-from-a-byte
    """
    return [[(truth if (integer_value & 1 << bit_position != 0) else falsum) for bit_position in range(0,n)] for integer_value in range(0,2 ** n)]



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


def satisfaction_set(
        formula: BooleanFormula
):
    """Return the satisfaction set of a Boolean phi.

    Taking the list of atomic variables from the phi,
    the satisfaction set is the list of all combinations of variable values,
    such that the phi is true."""
    # TODO: Implement function from satisfaction_index
    pass


def satisfaction_index(phi: BooleanFormula, variables_list=None):
    """Compute the **satisfaction index** (:math:`\text{sat}_I`) of a Boolean formula (:math:`\phi`).

    Alias:
    **sat_i**

    Definition:
    Let :math:`\phi` be a Boolean formula.
    :math:`\text{sat}_I \colon= ` the truth value of :math:`\phi` in all possible worlds.

    Args:
        phi (BooleanFormula): The Boolean formula :math:`\phi` .
    """
    # Retrieve the computed results
    if variables_list is None:
        variables_list = phi.list_atomic_variables()
    variables_number = len(variables_list)
    arguments_number = phi.arity
    argument_vectors = [None] * arguments_number
    log.debug(arguments_number=arguments_number)
    for argument_index in range(0, arguments_number):
        argument = phi.arguments[argument_index]
        log.debug(argument=argument, argument_index=argument_index)
        if isinstance(argument, BooleanFormula):
            # The argument is a phi.
            # Recursively compute the satisfaction set of that phi.
            vector = satisfaction_index(argument, variables_list=variables_list)
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
    match phi.arity:
        case 0: output_vector = phi.symbol.algorithm(vector_size =2 ** variables_number)
        case 1: output_vector = phi.symbol.algorithm(argument_vectors[0])
        case 2: output_vector = phi.symbol.algorithm(argument_vectors[0], argument_vectors[1])
        case _: log.error('Arity > 2 are not yet supported, sorry')
    log.info(output_vector=output_vector)
    return output_vector


sat_i = satisfaction_set
"""A shorthand alias for **satisfaction_set**."""

class BooleanAlgebra:
    """A fundamental Boolean algebra composed of (⊥,⊤,¬,∧,∨).

    *The corresponding abstraction of P(X) is called Boolean algebra. Specifically, a Boolean Algebra is a non-empty
    set A, together with two binary operations ∧ and ∨ (on A), a unary operation ', and two distinguished elements 0
    and 1, satisfying the following axioms...* :cite:p:`2009:Halmos`.

    """

    # TODO: Create a generic formal language structure and inherit from it.
    # TODO: Considering making it a singleton but... we must support inheritance.
    def __init__(self):
        # TODO: Populate a functions dictionary.
        pass


class BooleanDomain(WellKnownDomain):
    # TODO: Enrich the Set class as a python dictionary and adapt this class.
    """A Boolean domain is a set consisting of exactly two elements whose interpretations include false and true.

    Bibliography:
        * https://en.wikipedia.org/wiki/Boolean_domain
    """

    def __init__(self, **kwargs):
        """Initializes a Boolean domain."""
        kwargs[keywords.variable_base_name] = glyphs.mathbb_b_uppercase
        kwargs[keywords.variable_exponent] = None
        kwargs[keywords.variable_indexes] = None
        kwargs[keywords.set_dimensions] = 1
        super().__init__(**kwargs)

    @property
    def falsum(self):
        """BooleanConstant: The falsum boolean value."""
        global falsum
        return falsum

    @property
    def truth(self):
        """BooleanConstant: The truth boolean value."""
        global truth
        return truth


class BooleanFunction(Function):

    def __init__(
            self,
            arity: int,
            domain: Set,
            algorithm: typing.Callable,
            base_name: FunctionBaseName,
            **kwargs):
        """Initializes a function."""
        global boolean_domain

        indexes = None
        codomain = boolean_domain

        super().__init__(
            arity=arity,
            domain=domain,
            codomain=codomain,
            algorithm=algorithm,
            base_name=base_name,
            indexes=indexes,
            **kwargs
        )


class BooleanConstant(BooleanFunction):
    def __new__(cls,
                source=None,
                **kwargs):
        global truth
        global _truth_initialized
        global falsum
        global _falsum_initialized
        # We can't call coerce in __new__,
        # because it would then recall the constructor,
        # ending up in an infinite loop.
        # But BooleanConstant must support conversion during coercion.
        # A solution is to implement singletons.
        if source is not None:
            if isinstance(source, bool):
                if source and _truth_initialized:
                    # __init__ logic must be bypassed,
                    # because the instance has already been initialized.
                    # This is managed in __init__.
                    return truth
                elif not source and _falsum_initialized:
                    # __init__ logic must be bypassed,
                    # because the instance has already been initialized.
                    # This is managed in __init__.
                    return falsum
                else:
                    log.error(
                        'Instanciation of BooleanConstant with object argument is only allowed once singletons are initialized.')
        return super().__new__(cls)

    def __init__(
            self,
            source=None,
            inner_bool_value: bool = None,
            algorithm: typing.Callable = None,
            base_name: FunctionBaseName = None,
            **kwargs):
        """Initializes a Boolean value."""
        global _falsum_initialized
        global _truth_initialized
        if not hasattr(self, '_inner_bool_value'):
            # TODO: I needed to add this to prevent the following warning from Sphinx auto-documentation:
            #  WARNING: error while formatting signature for naive.boolean_algebra_1.falsum:
            #  Handler <function record_typehints at 0x000002AADAEBC5E0>
            #  for event 'autodoc-process-signature' threw an exception
            #  (exception: 'BooleanConstant' object has no attribute '_inner_bool_value')
            #  I guess Sphinx instanciates an object but I don't understand why and
            #  how to manage singletons in this situation.
            self._inner_bool_value = None
        if source is None:
            # Singleton constructor
            arity = 0
            domain = None  # TODO: Question: use a representation of the empty set instead?
            if inner_bool_value is None:
                log.error(f'Argument pythonic_value is mandatory.')
            self._inner_bool_value = inner_bool_value
            if inner_bool_value:
                _truth_initialized = True
            else:
                _falsum_initialized = True
            super().__init__(
                arity=arity,
                domain=domain,
                algorithm=algorithm,
                base_name=base_name,
                **kwargs)

    def __bool__(self):
        """Provides support for implicit and explicit (i.e. ``bool(v)``) conversions to **bool**.

        Returns:
            bool: the canonic mapping of :class:`BooleanConstant` with the pythonic **bool** type.
        """
        return self._inner_bool_value

    def __int__(self):
        """Canonical conversion with **int**."""
        if self._inner_bool_value:
            return int(1)
        else:
            return int(0)

    def __eq__(self, other: CoercibleBooleanConstant) -> bool:
        """Provides support for mathematical equality.

        All python objects are implicitly convertible to bool,
        but we want the equality operator to rather approach mathematical equality.
        Hence, we explicitly convert **other** to **BooleanConstant** which issues warnings and raises exceptions as necessary.

        Args:
            other(CoercibleBooleanConstant): A compatible boolean object.

        Returns:
            bool: The truth value of the equality operator.
        """
        other = coerce(other, BooleanConstant)  # Assure an exception is raised if the type is not supported.
        result = self._inner_bool_value == bool(other)  # Explicit conversion is superfluous but clearer
        return result


CoercibleBooleanConstant = typing.TypeVar(
    'CoercibleBooleanConstant',
    BooleanConstant,
    bool,
    int,
    str  # TODO Implement coercion of well known representations.
)
"""Supported types for coercion to class :class:`BinaryValue`."""

boolean_algebra = BooleanAlgebra()

boolean_domain = BooleanDomain()
"""The Boolean domain is the set consisting of exactly two elements whose interpretations include false and true.

The Boolean domain is a partially ordered set and its elements are also its bounds.

Bibliography:
    * https://en.wikipedia.org/wiki/Boolean_domain
    * https://en.wikipedia.org/wiki/Two-element_Boolean_algebra
"""

b = boolean_domain
"""A shorthand alias for the Boolean domain.

The Boolean domain is the set consisting of exactly two elements whose interpretations include false and true.

Bibliography:
    * https://en.wikipedia.org/wiki/Boolean_domain
"""

b_2 = WellKnownDomain(
    base_name=glyphs.mathbb_b_uppercase,
    exponent=2,
    indexes=None,
    dimensions=2)
"""The Boolean domain squared is the domain of all Boolean ordered pairs."""
# TODO: Implement this as a finite set with all its members.

conjunction = BooleanFunction(
    arity=2,
    domain=b_2,
    algorithm=conjunction_algorithm,
    base_name=glyphs.logical_conjunction,
    preferred_call_representation=OPERATOR)

land = conjunction
"""An alias for **conjunction**. 'and' being a reserved word in python, the name 'land' is used instead."""

disjunction = BooleanFunction(
    arity=2,
    domain=b_2,
    algorithm=disjunction_algorithm,
    base_name=glyphs.logical_disjunction,
    preferred_call_representation=OPERATOR)

lor = disjunction
"""An alias for **disjunction**. 'or' being a reserved word in python, the name 'lor' is used instead."""

negation = BooleanFunction(
    arity=1,
    domain=b,
    algorithm=negation_algorithm,
    base_name=glyphs.logical_negation,
    preferred_call_representation=OPERATOR)
"""The negation boolean function.

Args:
    v (BooleanConstant): A boolean value.

Returns:
    BooleanConstant: The negation of **v**.
"""

lnot = negation
"""An alias for **negation**. 'not' being a reserved word in python, the name 'lnot' is used instead."""

truth = BooleanConstant(
    inner_bool_value=True,
    algorithm=truth_algorithm,
    base_name=glyphs.logical_truth)
"""The truth boolean function.

Args:
    N/A

Returns:
    BooleanConstant: The boolean truth.
"""

t = truth
"""An shorthand alias for **truth**."""

falsum = BooleanConstant(
    inner_bool_value=False,
    algorithm=falsum_algorithm,
    base_name=glyphs.logical_falsum)
"""The falsum boolean function.

Args:
    N/A

Returns:
    BooleanConstant: The boolean falsum.
"""

f = falsum
"""An shorthand alias for **falsum**."""
