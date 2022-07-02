"""Everything related to pythonic types

TODO: Add description

Bibliography:
    * Types and pseudo-types: https://peps.python.org/pep-0484/

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
from .binary_value import BinaryValue
from .binary_value import BinaryValueInput
from .clean_math_variable import clean_math_variable
from .coerce import coerce
from .coercion_error import CoercionError
from .coercion_warning import CoercionWarning
from .natural_number_0 import NaturalNumber0
from .subscript import subscript
from .superscript import superscript


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


def textify_bv(v: BinaryVectorInput) -> str:
    if v is None:
        return 'undefined'  # We interpret None as undefined
    elif len(v) == 0:
        return u'\u2205'  # The empty set
    elif not isinstance(v, BinaryVector):
        v = coerce_binary_vector(v)
    v = np.array(v, dtype=int)
    v = np.array2string(v, precision=0, separator=' ')
    return v


def bv_equal_bv(v: BinaryVectorInput, w: BinaryVectorInput) -> bool:
    """Check if two binary vectors are equal.

    Formally:

    .. math::
        \\begin{align}
        & \\text{Let } v \\text{ be a binary vector with elements } (v_1, v_2, \\cdots, v_n) & \\\\
        & \\text{Let } w \\text{ be a binary vector with elements }  (w_1, w_2, \\cdots, w_m) & \\\\
        & v = w \\iff ((|v| = |w|) \\land (\\forall i \\in [1, |v|], v_i = w_i))
        \\end{align}

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
            # The special case [] = [] is defined as True
            # This is debatable
            return True
        else:
            return np.array_equal(v, w)


class BinaryVector(np.ndarray):
    """A row vector of binary values.

    Todos:
        * Rename to row binary vector, respectively column binary vector. Or add direction as an attribute.

    Sources:
        * https://numpy.org/doc/stable/user/basics.subclassing.html
    """

    def __new__(cls, o=None, /, *, size=None, default_value=None):
        """Instantiate a new BinaryVector.

        Under the hood, this method uses the Numpy view method to subtype NDArray.

        Args:
            o (object): A source object from which to infer the vector.
            size (int): (Conditional) The size of the vector. Warning: if **o** comprises more elements than **size**, the superfluous elements are truncated with a warning.
            default_value (bool, int): (Conditional) If elements must be populated to reach size, the default value of these new elements.
        """
        # This method's signature raises a "not compatible to __init__" warning.
        # I couldn't yet find a way to solve it.
        # TODO: Find a cleaner technical solution.
        if o is None:
            # When no source object is passed to the constructor,
            # or alternatively if o=None is passed to the constructor,
            # this is interpreted as "I want an empty set, please".
            o = []
        o = flatten(o)  # Incidentally assure that isinstance(obj) == list.
        if size is not None:
            missing_elements = size - len(o)
            default_value = bool(default_value)
            o.extend([default_value] * missing_elements)
            if len(o) > size:
                # This situation only arises if o was too large from the very beginning
                logging.warning(f'')
                o = o[: size]
        o = np.asarray(o, dtype=bool)
        o = np.asarray(o).view(cls)  # Re-type the instance
        return o

    def __str__(self):
        return textify_bv(self)

    def __eq__(self, obj):
        return bv_equal_bv(self, obj)


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


def coerce_element2(e: ElementInput) -> (Element, None):
    """Coerce an object **e** to type Element.

    If **e** is None, return None.
    If **e** is of type Element, return e.
    Else cast e to type Element.

    :param e: The raw element **e**.
    :return: The canonically typed element **e**.
    """
    if e is None:
        return None
    elif isinstance(e, Element):
        return e
    else:
        coerced_e = Element(e)
        logging.debug(f'{e}[{type(e)}] coerced to {coerced_e}[{type(coerced_e)}]')
        return coerced_e


def textify_fs(s: SetInput) -> str:
    if s is None:
        return 'undefined'  # We interpret None as undefined
    elif len(s) == 0:
        return u'\u2205'  # The empty set
    elif not isinstance(s, FiniteSet):
        s = coerce_set(s)
    t = ', '.join(s)
    t = f'{{{t}}}'
    return t


def fs_equal_fs(s: SetInput, t: SetInput) -> bool:
    """Check if two finite sets *S* (**s**) and *T* (**t**) are equal.

    Formally:

    .. math::
        \\begin{align}
        & \\text{Let } s \\text{ be a finite set with elements } (s_1, s_2, \\cdots, s_n) & \\\\
        & \\text{Let } t \\text{ be a finite set with elements }  (t_1, t_2, \\cdots, t_m) & \\\\
        & s = t \\iff ((|s| = |t|) \\land (\\forall i \\in [1, |s|], s_i = t_i))
        \\end{align}

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
        s = coerce_set(s)
        t = coerce_set(t)
        if len(s) == 0 and len(t) == 0:
            # The special case [] = [] is defined as True
            # This is debatable
            return True
        else:
            return np.array_equal(s, t)


class FiniteSet(list):
    """A finite set.

    Bibliography:
        - https://stackoverflow.com/questions/4868291/how-to-subclass-array-array-and-have-its-derived-constructor-take-no-parameters

    Usage:

        .. jupyter-execute::
            :hide-output:

            import naive.type_library as tl

        .. jupyter-execute::

            # If nothing is passed to the constructor, an empty set is returned:
            s = tl.FiniteSet()
            print(s)

        .. jupyter-execute::

            # Finite sets may be built from a series of string-equivalent objects:
            s = tl.FiniteSet(u'Platypus', 'Euler', 'Boson')
            print(s)

        .. jupyter-execute::

            # ...or iterable objects:
            s = tl.FiniteSet(['Platypus', 'Euler', 'Boson'])
            print(s)

        .. jupyter-execute::

            # FS is shorthand for FiniteSet:
            s = tl.FS(u'FS', 'FiniteSet')
            print(s)

        .. jupyter-execute::

            # Mathematical sets are unordered by definition,
            # but naive implementation is automatically ordered:
            s = tl.FiniteSet('h', 'g', 'b', 'a', 'c', 'f', 'g')
            print(s)
            # The reason for this design choice are:
            #  1) readability,
            #  2) compatibility with incidence vectors.

        .. jupyter-execute::

            # The constructor is adaptive and flattens whatever input it gets:
            s = tl.FS('a', 'b', 'c', ['d', 'e', ['f']])
            print(s)

        .. jupyter-execute::

            # The size shortcut helps create sets of canonically named elements:
            s = tl.FS(size=5)
            print(s)

        .. jupyter-execute::

            # ...with a custom prefix:
            s = tl.FS(size=3, prefix='x')
            print(s)

        .. jupyter-execute::

            # ...0-based index:
            s = tl.FS(size=3, prefix='y', init=0)
            print(s)

        .. jupyter-execute::

            # Note that spaces (" ") and commas (",") are forbidden in element names to avoid ambiguity:
            s = tl.FS('hack, the, list')
            print(s)

        .. jupyter-execute::

            # Note that indexes are voluntarily padded for easier alphanumeric ordering:
            s = tl.FS(size=12, prefix='y', init=1)
            print(s)

    """

    def __init__(self, *args, size=None, prefix=None, init=1):
        """Instantiate a new FiniteSet.

        Under the hood, this method uses the Numpy view method to subtype NDArray.

        Args:
            \*args (optional): Source (possibly iterable) objects from which to infer the vector.
            size (int, optional): (Conditional) The size of the finite set. Warning: if ** *args ** comprises more elements than **size**, the superfluous elements are truncated with a warning.
            prefix (str, optional): (Conditional) A prefix if new elements must be included in the set to reach size. Defaults to 'e'.
            init (int, optional): (Conditional) An initial value if new elements must be included in the set to reach size. Defaults to 1.
        """
        super().__init__()
        self.append(args)
        if size is not None:
            self.append_from_range(size, prefix, init)

    def __str__(self):
        return textify_fs(self)

    def __eq__(self, obj):
        return fs_equal_fs(self, obj)

    def append(self, obj: (ElementInput, SetInput)):
        """Add an element **e** to the set.

        By definition, set
        """
        if obj is not None:
            if isinstance(obj, Element):
                super().append(obj)
            else:
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

    def append_from_range(self, size: int, prefix: str, init: int):
        """Add a range of prefixed elements to the set.

        :param size:
        :param prefix:
        :param init:
        :return:
        """
        if size is None:
            size = 0
        if prefix is None:
            prefix = 'e'
        if init is None:
            init = 1
        elif init < 0:
            init = 0
        fixed_length = len(str(size))
        pad = '₀' * (fixed_length - 1)
        for i in range(init, init + size):
            element_name = f'{prefix}{(pad + subscript(str(i)))[-fixed_length:]}'
            self.append(Element(element_name))


"""An alias for Finite Set"""
FS = FiniteSet

SetInput = typing.TypeVar(
    'SetInput',
    abc.Iterable,
    FiniteSet,
    typing.List[str]
)

AtomicPropertySet = FiniteSet
AtomicPropertySetInput = SetInput

StateSet = FiniteSet
StateSetInput = SetInput

IndexPosition = int
IndexPositionInput = typing.TypeVar(
    'IndexPositionInput',
    IndexPosition,
    int
)


class Element(str):
    def __new__(cls, o: (str, None) = None, *args, **kwargs):
        o = clean_math_variable(o)
        o = str.__new__(cls, o)
        return o


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
    FiniteSet)

SetOrIVInput = typing.TypeVar(
    'SetOrIVInput',
    abc.Iterable,
    BinaryVector,
    np.ndarray,
    FiniteSet,
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


def coerce_binary_vector(x: BinaryVectorInput) -> (BinaryVector, None):
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


def coerce_incidence_vector(x: IncidenceVectorInput, s: FiniteSet = None) -> IncidenceVector:
    if s is not None:
        s = coerce_set(s)
    if isinstance(x, IncidenceVector):
        if s is None:
            # If the base set is not provided,
            # we assume it is the caller's intention
            # to not check the consistency of
            # the incidence vector with its base set.
            logging.warning(u'Skip subset test')
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


def coerce_set(x: SetInput) -> (FiniteSet, None):
    """Assure the Set type for x.

    Note: a coerced set is always sorted. This simplifies the usage of incidence vectors with consistent index positions.

    :param x:
    :return:
    """
    if x is None:
        return None
    elif is_instance(x, FiniteSet):
        return x
    coerced_x = FiniteSet(x)
    logging.debug(f'{x}[{type(x)}] coerced to {coerced_x}[{type(coerced_x)}]')
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
    elif t in (FiniteSet, SetInput, AtomicPropertySet, AtomicPropertySetInput, StateSet, StateSetInput):
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


def coerce_subset(s_prime: FiniteSet, s: FiniteSet) -> FiniteSet:
    """Coerce s' to a subset of s.

    :param s_prime:
    :param s:
    :return:
    """
    s_prime = coerce_set(s_prime)
    if s is None:
        logging.warning(u'Skip the subset test')
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
        raise NotImplementedError(u'Unsupported type')


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

        return FiniteSet
