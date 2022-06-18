# IMPORTS

# PEP 563 – Postponed Evaluation of Annotations
# Source: https://peps.python.org/pep-0563/
from __future__ import annotations

import array
# import collections.abc as abc
import typing
# import dataclasses
import array
import numpy as np
import logging
import collections.abc as abc
import nptyping as npt
import math
import itertools

# CLASSES AND VARIABLE TYPES
# Reference: https://peps.python.org/pep-0484/

BinaryMatrix = npt.NDArray[npt.Shape["*,*"], npt.Bool]

BinaryMatrixInput = typing.TypeVar(
    'BinaryMatrixInput',
    abc.Iterable,
    BinaryMatrix,
    np.ndarray)

BinaryValue = typing.NewType('BinaryValue', bool)

BinaryValueInput = typing.TypeVar(
    'BinaryValueInput',
    BinaryValue,
    bool,
    int
)

BinaryVector = npt.NDArray[npt.Shape["*"], npt.Bool]

BinaryVectorInput = typing.TypeVar(
    'BinaryVectorInput',
    abc.Iterable,
    BinaryVector,
    np.ndarray)

IncidenceVector = npt.NDArray[npt.Shape["*"], npt.Bool]

IncidenceVectorInput = typing.TypeVar(
    'IncidenceVectorInput',
    abc.Iterable,
    BinaryVector,
    IncidenceVector,
    np.ndarray)

Set = typing.List[str] #npt.NDArray[npt.Shape["*"], npt.Str0]

SetInput = typing.TypeVar(
    'SetInput',
    abc.Iterable,
    typing.List[str],
    Set)

Supported = typing.TypeVar(
    'Supported',
    BinaryVectorInput,
    IncidenceVectorInput,
    SetInput)


# UTILITY FUNCTIONS

def flatten(x: abc.Iterable[abc.Any]) -> abc.List[abc.Any]:
    """Flatten an iterable"""

    if isinstance(x, abc.Iterable):
        flat_x = []
        for y in x:
            if isinstance(y, abc.Iterable):
                # Recursive call
                # We cannot call directly extend to support n-depth structures
                flat_x.extend(flatten(y))
            else:
                flat_x.append(y)
        return flat_x
    else:
        # The assumption is that x is a scalar
        # and because the function caller expects an iterable
        # we can return a list
        return [x]


# OBJECT TYPING, DATA VALIDATION AND TYPE COERCION FUNCTIONS

def coerce_binary_matrix(x: BinaryMatrixInput) -> BinaryMatrix:
    if isinstance(x, BinaryMatrix):
        return x
    else:
        x2 = coerce_binary_vector(x)
        square_side = math.sqrt(len(x2))
        if int(square_side) != square_side:
            raise IndexError(f'x is not a square')
        square_side = int(square_side)
        x2 = np.reshape(x2, (square_side, square_side))
        logging.debug(f'coerce_binary_matrix({x}[{type(x)}]) -> {x2}')
        return x2


def coerce_binary_value(x: BinaryValueInput) -> BinaryValue:
    if isinstance(x, bool):
        return x
    elif isinstance(x, int) and 0 <= x <= 1:
        return bool(x)
    else:
        # I find python's coercion of boolean values too aggressive
        x2 = min(max(int(x), 0), 1)
        logging.debug(f'coerce_binary_value({x}[{type(x)}]) -> {x2}')
        return x2


def coerce_binary_vector(x: BinaryVectorInput) -> BinaryVector:
    if isinstance(x, (BinaryVector, IncidenceVector)):
        return x
    elif isinstance(x, abc.Iterable):
        coerced_x = flatten(x)
        coerced_x = np.asarray(coerced_x, dtype=bool)
        logging.debug(f'coerce_binary_vector({x}[{type(x)}]) -> {coerced_x}')
        return coerced_x
    else:
        raise NotImplementedError


def coerce_incidence_vector(x: IncidenceVectorInput) -> IncidenceVector:
    if isinstance(x, (BinaryVector, IncidenceVector)):
        return x
    elif isinstance(x, abc.Iterable):
        coerced_x = flatten(x)
        coerced_x = np.asarray(coerced_x, dtype=bool)
        logging.debug(f'coerce_binary_vector({x}[{type(x)}]) -> {coerced_x}')
        return coerced_x
    else:
        raise NotImplementedError


def coerce_set(x: SetInput) -> Set:
    """Assure the Set type for x.

    Note: a coerced set is always sorted. This simplifies the usage of incidence vectors with consistent index positions.

    :param x:
    :return:
    """
    if isinstance(x, abc.Iterable):
        if all(isinstance(y, str) for y in x):
            return x
    coerced_x = flatten(x)
    coerced_x = [str(e) for e in coerced_x]
    coerced_x = sorted(coerced_x)
    logging.debug(f'coerce_set({x}[{type(x)}]) -> {coerced_x}')
    return coerced_x


def coerce_specialized(x: object) -> Supported:
    if isinstance(x, (BinaryVector, BinaryMatrix)):
        return x
    else:
        # object is not of recognizable specialized type
        # in consequence we must make an arbitrage
        if isinstance(x, abc.Iterable):
            if all(isinstance(y, bool) for y in x):
                # Note that BinaryVector is equivalent to IncidenceVector
                return coerce_binary_vector(x)
            elif all(isinstance(y, int) for y in x):
                # Note that BinaryVector is equivalent to IncidenceVector
                return coerce_binary_vector(x)
            elif all(isinstance(y, str) for y in x):
                return coerce_set(x)
            raise NotImplementedError('Unsupported iterable')
        else:
            raise NotImplementedError('Unsupported type')


# OPERATORS

def equals(x: object, y: object) -> bool:
    x = coerce_specialized(x)
    y = coerce_specialized(y)
    if isinstance(x, np.ndarray) and isinstance(y, np.ndarray):
        # Provide generic support for BinaryVector, IncidenceVector, BinaryMatrix, etc., etc.
        return np.array_equal(x, y)
    if isinstance(x, abc.Iterable):
        if all(isinstance(z, str) for z in x):
            # This is a Set
            return x == y
        else:
            raise TypeError('Iterable of unsupported type')
    else:
        raise TypeError('Unsupported type')


def inverse(x: BinaryVector) -> BinaryVector:
    x = coerce_binary_vector(x)
    x = np.logical_not(x)
    x = coerce_binary_vector(x)
    return x


def get_zero_binary_vector(size: int) -> BinaryVector:
    return np.zeros(size, dtype=bool)


def get_one_binary_vector(size: int) -> BinaryVector:
    return np.ones(size, dtype=bool)


def get_set_from_range(n: int, prefix: str = 'e', index_start: int = 0):
    """Generate a set of n elements, prefixed and numbered"""
    s = []
    for i in range(index_start, index_start + n):
        s.append(f'{prefix}{i}')
    s = coerce_set(s)
    return s


def get_state_set(n: int, prefix: str = 's', index_start: int = 0):
    return get_set_from_range(n, prefix, index_start)


def get_incidence_vector(subset: Set, superset: Set) -> IncidenceVector:
    """Given a subset S' ⊆ S, return the corresponding incidence vector"""
    iv = get_zero_binary_vector(len(superset))
    for e in subset:
        e_index = superset.index(e)
        iv[e_index] = True
    return iv

class KripkeStructure()