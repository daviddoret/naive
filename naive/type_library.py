"""Everything related to pythonic types

TODO: Add description

"""

# PEP 563 – Postponed Evaluation of Annotations
# Reference: https://peps.python.org/pep-0563/
from __future__ import annotations

import typing
import numpy as np
import collections.abc as abc
import nptyping as npt
import logging
import math

# Types and pseudo-types
# Reference: https://peps.python.org/pep-0484/


BinaryValue = typing.NewType(
    'BinaryValue',
    bool)
"""A NewType equivalent to :math:`\mathbb{B}`

Under the hood, it is a :py:class:`bool`."""

BinaryValueInput = typing.TypeVar(
    'BinaryValueInput',
    BinaryValue,
    bool,
    int
)
"""A TypeVar that represent types commonly accepted as equivalent to :py:data:`BinaryValue`.

Main usages:

* Flexible hinting of functions and methods arguments.

* Implicit identification of object types.

Commonly accepted types:

* :py:data:`BinaryValue`.

* :py:class:`bool`.

* :py:class:`int` (mapping: x=0 is equivalent to False, x>0 is equivalent to True).

"""

BinaryMatrix = npt.NDArray[npt.Shape["*,*"], npt.Bool]
"""A python type that is equivalent to a **binary matrix** mathematical object.

A **binary matrix** is a rectangular array of binary values, called the elements of the matrix. The horizontal and vertical lines of elements in a matrix are called rows and columns, respectively. (Source: `Wikipedia <https://en.wikipedia.org/wiki/Matrix_(mathematics)>`_).

Under the hood, **BinaryMatrix** is a type alias for a Numpy n-dimensional array (i.e. `NDArray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_) of rectangular shape, and bool dtype.

"""

BinaryMatrixInput = typing.TypeVar(
    'BinaryMatrixInput',
    abc.Iterable,
    BinaryMatrix,
    np.ndarray)
"""A TypeVar that represent types commonly accepted as equivalent to :py:data:`BinaryMatrix`.

Main usages:

* Flexible hinting of functions and methods arguments.

* Implicit identification of object types.

Commonly accepted types:

* :py:class:`abc.Iterable`.

* :py:data:`BinaryMatrix`

* :py:class:`np.ndarray`.

"""

BinarySquareMatrix = npt.NDArray[npt.Shape["*,*"], npt.Bool]
"""A :py:data:`BinaryMatrix` with the same number of rows and columns.


"""

BinarySquareMatrixInput = typing.TypeVar(
    'BinarySquareMatrixInput',
    abc.Iterable,
    BinarySquareMatrix,
    np.ndarray)
"""A TypeVar that represent types commonly accepted as equivalent to :py:data:`BinarySquareMatrix`.

Main usages:

* Flexible hinting of functions and methods arguments.

* Implicit identification of object types.

Commonly accepted types:

* :py:class:`abc.Iterable`.

* :py:data:`BinarySquareMatrix`

* :py:class:`np.ndarray`.

"""


def textify_binary_vector(v: BinaryVectorInput) -> str:
    if v is None:
        return 'undefined'  # We interpret None as undefined
    elif len(v) == 0:
        return '∅'  # The empty set
    elif not isinstance(v, BinaryVector):
        v = coerce_binary_vector(v)
    v = np.array(v, dtype=int)
    v = np.array2string(v, precision=0, separator=' ')
    return v


def binary_vector_equal(v: BinaryVectorInput, w: BinaryVectorInput) -> bool:
    """Check if two binary vectors are equal.

    Formally:

    .. math::
        \\begin{align*}
        & \\text{Let } v \\text{ be a binary vector with elements } (v_1, v_2, \\cdots, v_n) & \\\\
        & \\text{Let } w \\text{ be a binary vector with elements }  (w_1, w_2, \\cdots, w_m) & \\\\
        & v = w \\iff ((|v| = |w|) \\land (\\forall i \\in [1, |v|], v_i = w_i))
        \\end{align*}

    Sample 1:

        .. exec_code::
            :filename: binary_vector_equal_sample_1.py

    Sample 2:

        .. exec_code::
            :filename: binary_vector_equal_sample_2.py

    """
    if v is None and w is None:
        # The special case undefined = undefined is defined as True
        # This is debatable
        # The fragile rationale of this decision is consistency with Python's None == None
        return True
    elif v is None or w is None:
        # Undefined is incomparable
        return False
    else:
        v = coerce_binary_vector(v)
        w = coerce_binary_vector(w)
        if len(v) == 0 and len(w) == 0:
            # The special case ∅ = ∅ is defined as True
            # This is debatable
            return True
        else:
            return np.array_equal(v, w)


class BinaryVector(np.ndarray):
    """A row vector of binary values.

    TODO: Rename to row binary vector, respectively column binary vector. Or add direction as an attribute.

    Sources:
    https://numpy.org/doc/stable/user/basics.subclassing.html
    """

    def __new__(cls, obj=None, /, *, size=None, default_value=None):
        if obj is None and size is None:
            return None
        elif obj is not None:
            obj = flatten(obj)
        elif size is not None:
            default_value = bool(default_value)
            obj = [default_value] * size
        obj = np.asarray(obj, dtype=bool)
        obj = np.asarray(obj).view(cls)  # Re-type the instance
        return obj

    def __str__(self):
        return textify_binary_vector(self)

    def __eq__(self, obj):
        return binary_vector_equal(self, obj)


"""A shortcut alias for the BinaryVector class."""
BV = BinaryVector


BinaryVectorInput = typing.TypeVar(
    'BinaryVectorInput',
    abc.Iterable,
    BinaryVector,
    np.ndarray)

IncidenceVector = npt.NDArray[npt.Shape["*"], npt.Bool]
"""An incidence vector.

An incidence vector is a binary vector used to index elements in a set.
"""

IncidenceVectorInput = typing.TypeVar(
    'IncidenceVectorInput',
    abc.Iterable,
    BinaryVector,
    IncidenceVector,
    np.ndarray)



def coerce_element2(e: tl.ElementInput) -> tl.Element:
    if e is None:
        return None
    elif isinstance(e, tl.Element):
        return e
    else:
        coerced_e = tl.Element(e)
        logging.debug(f'Coerce {e}[{type(e)}] to {coerced_e}[{type(coerced_e)}]')
        return coerced_e


def textify_set(s: tl.SetInput) -> str:
    if s is None:
        return 'undefined'  # We interpret None as undefined
    elif len(s) == 0:
        return '∅'  # The empty set
    elif not isinstance(s, Set):
        s = tl.coerce_set(s)
    t = ', '.join(s)
    t = f'{{{t}}}'
    return t


def set_equal(s: tl.SetInput, t: tl.SetInput) -> bool:
    """Check if two finite sets **s** and **t** are equal.

    Formally:

    .. math::
        \\begin{align*}
        & \\text{Let } s \\text{ be a finite set with elements } (s_1, s_2, \\cdots, s_n) & \\\\
        & \\text{Let } t \\text{ be a finite set with elements }  (t_1, t_2, \\cdots, t_m) & \\\\
        & s = t \\iff ((|s| = |t|) \\land (\\forall i \\in [1, |s|], s_i = t_i))
        \\end{align*}

    Sample 1:

        .. exec_code::
            :filename: set_sample_1.py

    Sample 2:

        .. exec_code::
            :filename: set_sample_2.py

    """
    if s is None and t is None:
        # The special case undefined = undefined is defined as True
        # This is debatable
        # The fragile rationale of this decision is consistency with Python's None == None
        return True
    elif s is None or t is None:
        # Undefined is incomparable
        return False
    else:
        s = tl.coerce_set(s)
        t = tl.coerce_set(t)
        if len(s) == 0 and len(t) == 0:
            # The special case ∅ = ∅ is defined as True
            # This is debatable
            return True
        else:
            return np.array_equal(v, w)


class Set(list):
    """A finite set.

    Bibliography:
        - https://stackoverflow.com/questions/4868291/how-to-subclass-array-array-and-have-its-derived-constructor-take-no-parameters
    """

    def __init__(self, *args):
        super().__init__()
        self.append(args)

    def __str__(self):
        return textify_set(self)

    def __eq__(self, obj):
        return set_equal(self, obj)

    def append(self, obj: (ElementInput, SetInput)):
        # Flatten if necessary
        obj = flatten(obj)
        # Assure all elements are unique values
        obj = set(obj)
        # But do not use the python set type that is unordered
        # and use list instead to assure index positions of elements
        obj = list(obj)
        # Assure elements are ordered to simplify the usage of incidence vectors
        obj = sorted(obj)
        for e in obj:
            if e not in self:
                # Assure all elements are of type Element
                e = coerce_element2(e)
                super().append(e)


"""An alias for Finite Set"""
FS = Set


SetInput = typing.TypeVar(
    'SetInput',
    abc.Iterable,
    Set,
    typing.List[str]
)

AtomicPropertySet = Set
AtomicPropertySetInput = SetInput

StateSet = Set
StateSetInput = SetInput

IndexPosition = int
IndexPositionInput = typing.TypeVar(
    'IndexPositionInput',
    IndexPosition,
    int
)

Element = str
ElementInput = typing.TypeVar(
    'ElementInput',
    Element,
    int,
    str,
)

State = Element
StateInput = typing.TypeVar(
    'StateInput',
    Element,
    int,
    State,
    str
)

AtomicProperty = str
AtomicPropertyInput = typing.TypeVar(
    'AtomicPropertyInput',
    AtomicProperty,
    Element,
    int,
    str
)

SetOrIV = typing.TypeVar(
    'SetOrIV',
    BinaryVector,
    IncidenceVector,
    Set)

SetOrIVInput = typing.TypeVar(
    'SetOrIVInput',
    abc.Iterable,
    BinaryVector,
    np.ndarray,
    Set,
    typing.List[str]
)


def flatten(x: object) -> typing.List[typing.Any]:
    """Flatten an iterable object.

    This utility function converts embedded lists or multidimensional objects to vectors.

    If x is already a flat list, returns a new list instance with the same elements.

    If x is not iterable, returns an iterable version of x, that is: [x].

    If x is None, returns an empty list, that is [].

    Args:
        x (object): Any object but preferably an iterable object of type: abc.Iterable[typing.Any].

    Returns:
         A flat list.

    """
    if isinstance(x, abc.Iterable):
        flat_x = []
        for y in x:
            # Recursive call for sub-structures
            # except strings that are understood as atomic
            if isinstance(y, abc.Iterable) and not isinstance(y, str):
                # We cannot call directly extend to support n-depth structures
                flat_x.extend(flatten(y))
            else:
                flat_x.append(y)
        return flat_x
    if x is None:
        return []
    else:
        # The assumption is that x is a scalar
        # and because the function caller expects an iterable
        # we can return a list
        return [x]


def coerce_binary_value(x: BinaryValueInput) -> BinaryValue:
    """Coerce an object of a compatible Python type to the **BinaryValue** type.

    :param x: A Python object of a compatible type.
    :return: An object of type BinaryValue.
    :rtype: BinaryValue
    """
    if isinstance(x, bool):
        return BinaryValue(x)
    elif isinstance(x, int) and 0 <= x <= 1:
        coerced_x = BinaryValue(bool(x))
        logging.debug(f'coerce_binary_value({x}[{type(x)}]) -> {coerced_x}')
        return BinaryValue(coerced_x)
    else:
        raise TypeError(f'coerce_binary_value: {x} is of unsupported type {type(x)}')


def coerce_binary_matrix(x: BinaryMatrixInput) -> BinaryMatrix:
    """YYY

    :param x:
    :return:
    """
    if isinstance(x, BinaryMatrix):
        if len(x.shape) == 2:
            # Good, it is a bi-dimensional array
            return x
    coerced_x = x
    if not isinstance(coerced_x, np.ndarray):
        try:
            coerced_x = np.asarray(coerced_x, dtype=bool)
        except ValueError as e:
            # If x is not bi-dimensional,
            # numpy raises the following error (which is expected):
            # ValueError: setting an array element with a sequence.
            # The requested array has an inhomogeneous shape after 1 dimensions.
            # The detected shape was (2,) + inhomogeneous part.
            complementary_message = f'A binary matrix is bi-dimensional by definition. Please assure that {x}[{type(x)}] has an homogeneous shape.'
            e.args = f'{complementary_message}. The original exception was: {e.args}'
            raise e
    if len(coerced_x.shape) == 2:
        # It is bi-dimensional,
        # but d-type was probably wrong
        coerced_x = np.asarray(coerced_x).astype(bool)
    else:
        # Dimension was incorrect,
        # we must assume the intention was to flatten it
        logging.warning(f'Incorrect dimension coerced to 1 dimension')
        coerced_x = coerce_binary_vector(coerced_x)
    logging.warning(f'Coerce {x}[{type(x)}] to binary matrix {coerced_x}')
    return coerced_x


def coerce_binary_square_matrix(x: BinarySquareMatrixInput) -> BinarySquareMatrix:
    """XXX

    :param x:
    :return:
    """
    if isinstance(x, BinarySquareMatrix):
        if len(x.shape) == 2 and x.shape[0] == x.shape[1]:
            # Good, it is a square matrix
            return x
    coerced_x = coerce_binary_vector(x)
    square_side = math.sqrt(len(coerced_x))
    if int(square_side) != square_side:
        raise IndexError(f'x is not a square')
    square_side = int(square_side)
    coerced_x = np.reshape(coerced_x, (square_side, square_side))
    logging.debug(f'Coerce {x}[{type(x)}] to square binary matrix {coerced_x}')
    return coerced_x


def coerce_binary_vector(x: BinaryVectorInput) -> BinaryVector:
    """YYY

    :param x:
    :return:
    """
    if isinstance(x, (BinaryVector, IncidenceVector)):
        return x
    elif x is None:
        logging.warning(f'coerce_binary_vector({x})')
        return None
    else:
        coerced_x = BinaryVector(x)
        logging.debug(f'coerce_binary_vector({x}[{type(x)}]) -> {coerced_x}')
        return coerced_x


def coerce_incidence_vector(x: IncidenceVectorInput, s: Set = None) -> IncidenceVector:
    if s is not None:
        s = coerce_set(s)
    if isinstance(x, IncidenceVector):
        if s is None:
            # If the base set is not provided,
            # we assume it is the caller's intention
            # to not check the consistency of
            # the incidence vector with its base set.
            logging.warning('Skip subset test')
            return x
        elif len(x) == len(s):
            return x
        else:
            raise ValueError(f'Incidence vector {x} has inconsistent cardinality with set {s}')
    elif isinstance(x, abc.Iterable):
        coerced_x = flatten(x)
        coerced_x = np.asarray(coerced_x, dtype=bool)
        logging.debug(f'Coerce incidence vector {x}[{type(x)}] to {coerced_x}')
        return coerced_x
    else:
        raise NotImplementedError


def coerce_set(x: SetInput) -> Set:
    """Assure the Set type for x.

    Note: a coerced set is always sorted. This simplifies the usage of incidence vectors with consistent index positions.

    :param x:
    :return:
    """
    if is_instance(x, Set):
        return x
    coerced_x = x
    # Prevent infinite loops by checking if x is already flat
    if not all(not isinstance(y, abc.Iterable) for y in x):
        # Flatten x if necessary
        coerced_x = flatten(x)
    # Assure all elements are of type string
    coerced_x = [str(e) for e in coerced_x]
    # Assure all elements are unique values
    coerced_x = set(coerced_x)
    # But do not use the python set type that is unordered
    # and use list instead to assure index positions of elements
    coerced_x = list(coerced_x)
    # Assure elements are ordered to simplify the usage of incidence vectors
    coerced_x = sorted(coerced_x)
    logging.debug(f'Coerce {x}[{type(x)}] to set {coerced_x}')
    return coerced_x


def coerce_atomic_property_set(ap: AtomicPropertySetInput):
    return coerce_set(ap)


def coerce_state_set(s: StateSetInput):
    return coerce_set(s)


def coerce_element(e: ElementInput, s: SetInput) -> Element:
    """Given element e passed with flexible input type, assure e ∈ S, and return e typed as Element"""
    # TODO: Assure support for index-based element
    s = coerce_set(s)
    if e is None:
        logging.error(f'e is None')
        raise ValueError(f'e is None')
    elif isinstance(e, Element):
        if s is None:
            logging.warning(f'Skip {e} ∈ s test because s is None')
            return e
        if e in s:
            return e
        else:
            logging.error(f'Element {e} is not an element of set {s}')
            raise ValueError(f'Element {e} is not an element of set {s}')
    elif is_instance(e, IndexPosition):
        if s is None:
            logging.error(f'Element {e} passed by index but set s is None')
            raise ValueError(f'Element {e} passed by index but set s is None')
        elif 0 <= e < len(s):
            coerced_e = s[e]
            logging.debug(f'Coerce {e}[{type(e)}] passed by index to element {coerced_e}')
        else:
            logging.error(f'Element {e}[{type(e)}] passed by index outside s boundaries')
            raise ValueError(f'Element {e}[{type(e)}] passed by index outside s boundaries')
    else:
        logging.error(f'Element {e}[{type(e)}] of unsupported type')
        raise ValueError(f'Element {e}[{type(e)}] of unsupported type')


def coerce_atomic_property(atom: AtomicPropertyInput, ap: AtomicPropertySetInput) -> AtomicProperty:
    atom = coerce_element(atom, ap)
    return atom


def coerce_state(state: StateInput, s: StateSetInput) -> State:
    state = coerce_element(state, s)
    return state


def is_instance(o: object, t: (type, typing.TypeVar)) -> bool:
    """Check if an arbitrary object **o** is of NewType, type, type alias, or TypeVar **t**.

    The native isinstance function does not support parametrized generics. Hence, we need a wrapper function to extend type checking.

    :param o: Any object
    :param t: A NewType, type, type alias, or TypeVar
    :return: A boolean
    """
    if isinstance(t, type):
        # Provide support for all standard types
        return isinstance(o, t)
    elif t in (Set, SetInput, AtomicPropertySet, AtomicPropertySetInput, StateSet, StateSetInput):
        if isinstance(o, abc.Iterable):
            if all(isinstance(y, str) for y in o):
                return True
        return False
    elif t in (
            BinaryVector, BinaryVectorInput, IncidenceVector, IncidenceVectorInput, IndexPosition, IndexPositionInput):
        if isinstance(o, abc.Iterable):
            if all(isinstance(y, bool) for y in o):
                return True
            if all(isinstance(y, int) for y in o):
                return True
        return False
    else:
        raise NotImplementedError(f'is_instance: Could not determine if {o}[{type(o)}] is of type {t}')


def coerce_subset(s_prime: Set, s: Set) -> Set:
    """Coerce s' to a subset of s.

    :param s_prime:
    :param s:
    :return:
    """
    s_prime = coerce_set(s_prime)
    if s is None:
        logging.warning('Skip the subset test')
        return s_prime
    else:
        s = coerce_set(s)
        if set(s).issuperset(set(s_prime)):
            return s_prime
        else:
            coerced_s_prime = [e for e in s_prime if e in s]
            coerced_s_prime = coerce_set(coerced_s_prime)
            logging.warning(f'Coerce {s_prime} to subset {coerced_s_prime} of set {s}')
            return coerced_s_prime


def coerce_subset_or_iv(o: SetOrIVInput, s: SetInput) -> SetOrIV:
    """Coerce an arbitrarily typed object **o** into either a properly typed subset or proper incidence vector of a set S.

    This function infers the correct type by inspecting the object **o**.

    :param o: An arbitrarily typed object.
    :param s: The set S.
    :return: A properly typed subset or incidence vector of S.
    """
    s = coerce_set(s)
    if is_instance(o, IncidenceVectorInput):
        return coerce_incidence_vector(o, s)
    elif is_instance(o, SetInput):
        return coerce_subset(o, s)
    else:
        raise NotImplementedError('Unsupported type')


def coerce_state_subset(s_prime_flexible: StateSetInput, s_flexible: StateInput):
    s_flexible = coerce_set(s_flexible)
    if is_instance(s_prime_flexible, StateSetInput):
        return coerce_subset(s_prime_flexible, s_flexible)
    elif is_instance(s_prime_flexible, IncidenceVectorInput):
        return coerce_incidence_vector(s_prime_flexible, s_flexible)
    else:
        raise NotImplementedError(f'coerce_state_subset: Unknown type: {s_prime_flexible}[{type(s_prime_flexible)}]')


def coerce_set_or_iv_type(python_type):
    if python_type == IncidenceVector:
        return python_type
    else:

        return Set
