from __future__ import annotations
import typing
from _class_well_known_domain import WellKnownDomain
from _class_function import Function, FunctionBaseName
from _class_set import Set
import glyphs
import keywords
import log
from _function_coerce import coerce

_truth_initialized = False
_falsum_initialized = False


def falsum_algorithm() -> BooleanValue:
    """The falsum boolean function.

    Returns:
        BooleanValue: The boolean falsum.
    """
    global falsum
    return falsum


def truth_algorithm() -> BooleanValue:
    """The truth boolean function.

    Returns:
        BooleanValue: The boolean truth.
    """
    global truth
    return truth


def negation_algorithm(x: BooleanValue) -> BooleanValue:
    """The negation boolean function.

    Args:
        x (BooleanValue): A boolean value.

    Returns:
        BooleanValue: The negation of **x**.
    """
    global truth
    global falsum
    x = coerce(x, BooleanValue)
    if x == truth:
        return falsum
    else:
        return truth


def conjunction_algorithm(x1: BooleanValue, x2: BooleanValue) -> BooleanValue:
    """The conjunction boolean function.

    Args:
        x1 (BooleanValue): A boolean value.
        x2 (BooleanValue): A boolean value.

    Returns:
        BooleanValue: The conjunction of **x1** and **x2**.
    """
    global truth
    global falsum
    x1 = coerce(x1, BooleanValue)
    x2 = coerce(x2, BooleanValue)
    if x1 == truth and x2 == truth:
        return truth
    else:
        return falsum


def disjunction_algorithm(x1: BooleanValue, x2: BooleanValue) -> BooleanValue:
    """The disjunction boolean function.

    Args:
        x1 (BooleanValue): A boolean value.
        x2 (BooleanValue): A boolean value.

    Returns:
        BooleanValue: The disjunction of **x1** and **x2**.
    """
    global truth
    global falsum
    x1 = coerce(x1, BooleanValue)
    x2 = coerce(x2, BooleanValue)
    if x1 == truth or x2 == truth:
        return truth
    else:
        return falsum


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

    @property
    def conjunction(self):
        global conjunction
        return conjunction

    @property
    def disjunction(self):
        global disjunction
        return disjunction

    @property
    def falsum(self):
        global falsum
        return falsum

    @property
    def negation(self):
        global negation
        return negation

    @property
    def truth(self):
        global truth
        return truth


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
        """BooleanValue: The falsum boolean value."""
        global falsum
        return falsum

    @property
    def truth(self):
        """BooleanValue: The truth boolean value."""
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


class BooleanValue(BooleanFunction):
    def __new__(cls,
                source=None,
                **kwargs):
        global truth
        global _truth_initialized
        global falsum
        global _falsum_initialized
        log.debug('__new__', source=source)
        # We can't call coerce in __new__,
        # because it would then recall the constructor,
        # ending up in an infinite loop.
        # But BooleanValue must support conversion during coercion.
        # A solution is to implement singletons.
        if source is not None:
            if isinstance(source, bool):
                if source and _truth_initialized:
                    # __init__ logic must be bypassed,
                    # because the instance has already been initialized.
                    # This is managed in __init__.
                    log.debug('Reuse truth singleton')
                    return truth
                elif not source and _falsum_initialized:
                    # __init__ logic must be bypassed,
                    # because the instance has already been initialized.
                    # This is managed in __init__.
                    log.debug('Reuse falsum singleton')
                    return falsum
                else:
                    log.error('Instanciation of BooleanValue with object argument is only allowed once singletons are initialized.')
        return super().__new__(cls)

    def __init__(
            self,
            source = None,
            pythonic_value: bool = None,
            algorithm: typing.Callable = None,
            base_name: FunctionBaseName = None,
            **kwargs):
        """Initializes a Boolean value."""
        global _falsum_initialized
        global _truth_initialized
        log.debug('__init__', source=source, pythonic_value=pythonic_value, base_name=base_name, kwargs=kwargs)
        if source is not None:
            log.debug('Bypassing __init__ logic on singletons')
        else:
            log.debug('Singleton initialization')
            arity = 0
            domain = None  # TODO: Question: use a representation of the empty set instead?
            if pythonic_value is None:
                log.error(f'Argument pythonic_value is mandatory.')
            self._pythonic_value = pythonic_value
            if pythonic_value:
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
        """Provides support for implicit and explicit (i.e. ``bool(x)``) conversions to **bool**.

        Returns:
            bool: the canonic mapping of :class:`BooleanValue` with the pythonic **bool** type.
        """
        return self._pythonic_value

    def __int__(self):
        """Canonical conversion with **int**."""
        if self._pythonic_value:
            return int(1)
        else:
            return int(0)

    def __eq__(self, other: CoercibleBooleanValue) -> bool:
        """Provides support for mathematical equality.

        All python objects are implicitly convertible to bool,
        but we want the equality operator to rather approach mathematical equality.
        Hence, we explicitly convert **other** to **BooleanValue** which issues warnings and raises exceptions as necessary.

        Args:
            other(CoercibleBooleanValue): A compatible boolean object.

        Returns:
            bool: The truth value of the equality operator.
        """
        other = coerce(other, BooleanValue)  # Assure an exception is raised if the type is not supported.
        result = self._pythonic_value == bool(other)  # Explicit conversion is superfluous but clearer
        return result


CoercibleBooleanValue = typing.TypeVar(
    'CoercibleBooleanValue',
    BooleanValue,
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
    base_name=glyphs.logical_conjunction)

land = conjunction
"""An alias for **conjunction**. 'and' being a reserved word in python, the name 'land' is used instead."""

disjunction = BooleanFunction(
    arity=2,
    domain=b_2,
    algorithm=disjunction_algorithm,
    base_name=glyphs.logical_disjunction)

lor = disjunction
"""An alias for **disjunction**. 'or' being a reserved word in python, the name 'lor' is used instead."""



negation = BooleanFunction(
    arity=1,
    domain=b,
    algorithm=negation_algorithm,
    base_name=glyphs.logical_negation)
"""The negation boolean function.

Args:
    x (BooleanValue): A boolean value.

Returns:
    BooleanValue: The negation of **x**.
"""

lnot = negation
"""An alias for **negation**. 'not' being a reserved word in python, the name 'lnot' is used instead."""

truth = BooleanValue(
    pythonic_value=True,
    algorithm=truth_algorithm,
    base_name=glyphs.logical_truth)
"""The truth boolean function.

Args:
    N/A

Returns:
    BooleanValue: The boolean truth.
"""

t = truth
"""An shorthand alias for **truth**."""

falsum = BooleanValue(
    pythonic_value=False,
    algorithm=falsum_algorithm,
    base_name=glyphs.logical_falsum)
"""The falsum boolean function.

Args:
    N/A

Returns:
    BooleanValue: The boolean falsum.
"""

f = falsum
"""An shorthand alias for **falsum**."""
