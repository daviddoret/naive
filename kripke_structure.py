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

Set = npt.NDArray[npt.Shape["*"], npt.Str0]

SetInput = typing.TypeVar(
    'SetInput',
    abc.Iterable,
    np.ndarray)

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
    if isinstance(x, Set):
        return x
    else:
        x2 = np.asarray(x, dtype=str).flatten()
        logging.debug(f'coerce_set({x}[{type(x)}]) -> {x2}')
        return x2


def coerce_specialized(x: object) -> Supported:
    if isinstance(x, (BinaryVector, BinaryMatrix, Set)):
        return x
    else:
        # object is not of specialized type
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
    else:
        raise NotImplementedError


def inverse(x: BinaryVector) -> BinaryVector:
    x = coerce_binary_vector(x)
    x = np.logical_not(x)
    x = coerce_binary_vector(x)
    return x


def get_zero_binary_vector(size: int) -> BinaryVector:
    return np.zeros(size, dtype=bool)


def get_one_binary_vector(size: int) -> BinaryVector:
    return np.ones(size, dtype=bool)


def set_to_incidence_vector(s: Set, t: Set) -> IncidenceVector:
    iv = IV(size=len(base), value=0)
    for e in s:
        e_index = base.index(e)
        iv[e_index] = 1
    return iv
