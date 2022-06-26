"""Everything related to pythonic types

This module blablabla

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
"""A type alias for binary matrix"""

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
"""
"""

BinaryVector = npt.NDArray[npt.Shape["*"], npt.Bool]
"""A row vector of binary values.

TODO: Rename to row binary vector, respectively column binary vector.
"""

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

Set = typing.List[str]  # npt.NDArray[npt.Shape["*"], npt.Str0]
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
        return coerced_x
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
    elif isinstance(x, abc.Iterable):
        coerced_x = flatten(x)
        coerced_x = np.asarray(coerced_x, dtype=bool)
        logging.debug(f'coerce_binary_vector({x}[{type(x)}]) -> {coerced_x}')
        return coerced_x
    else:
        raise NotImplementedError
