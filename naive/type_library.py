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
"""A TypeVar that represent types commonly accepted as equivalent to :py:data:`BinaryValue`

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
"""A type alias for binary matrix flexible input parameters"""


def flatten(x: abc.Iterable[typing.Any]) -> typing.List[typing.Any]:
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
