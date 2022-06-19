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

BinarySquareMatrix = npt.NDArray[npt.Shape["*,*"], npt.Bool]

BinarySquareMatrixInput = typing.TypeVar(
    'BinarySquareMatrixInput',
    abc.Iterable,
    BinarySquareMatrix,
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

Set = typing.List[str]  # npt.NDArray[npt.Shape["*"], npt.Str0]

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
            # Recursive call for sub-structures
            # except strings that are understood as atomic
            if isinstance(y, abc.Iterable) and not isinstance(y, str):
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
        if len(x.shape) == 2:
            # Good, it is a bi-dimensional array
            return x
    coerced_x = x
    if isinstance(coerced_x, np.ndarray):
        if len(coerced_x.shape) == 2:
            # It is bi-dimensional,
            # but d-type was probably wrong
            coerced_x = np.asarray(coerced_x).astype(bool)
        else:
            # Dimension was incorrect,
            # we must assume the intention was to flatten it
            logging.warning(f'Incorrect dimension coerced to 1 dimension')
            coerced_x = coerce_binary_vector(coerced_x)
    elif isinstance(coerced_x, list) and len(coerced_x) == 2:
        coerced_x = np.asarray(coerced_x).astype(bool)
    else:
        logging.warning(f'Incorrect dimension coerced to 1 dimension')
        coerced_x = coerce_binary_vector(coerced_x)
    logging.debug(f'Coerce {x}[{type(x)}] to binary matrix {coerced_x}')
    return coerced_x


def coerce_binary_square_matrix(x: BinarySquareMatrixInput) -> BinarySquareMatrix:
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


def cardinality(x: object) -> int:
    """Return the cardinality of x.

    :param x:
    :return:
    """
    if isinstance(x, (BinaryVector, IncidenceVector)):
        return len(x)
    elif isinstance(x, abc.Iterable):
        if all(isinstance(y, str) for y in x):
            return len(x)
        else:
            raise TypeError
    else:
        raise TypeError


def coerce_incidence_vector(x: IncidenceVectorInput, s: Set = None) -> IncidenceVector:
    if s is not None:
        s = coerce_set(s)
    if isinstance(x, (BinaryVector, IncidenceVector)):
        if s is None:
            # If the base set is not provided,
            # we assume it is the caller's intention
            # to not check the consistency of
            # the incidence vector with its base set.
            return x
        elif cardinality(x) == cardinality(s):
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
    if isinstance(x, set):
        if all(isinstance(y, str) for y in x):
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


def coerce_subset(s_prime: Set, s: Set) -> Set:
    """Coerce s' to a subset of s.

    :param s_prime:
    :param s:
    :return:
    """
    s_prime = coerce_set(s_prime)
    s = coerce_set(s)
    if set(s).issuperset(set(s_prime)):
        return s_prime
    else:
        coerced_s_prime = [e for e in s_prime if e in s]
        coerced_s_prime = coerce_set(coerced_s_prime)
        logging.warning(f'Coerce {s_prime} to subset {coerced_s_prime} of set {s}')
        return coerced_s_prime


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
    """Generate a set of n elements, prefixed and numbered with 0 padding"""
    s = []
    width = len(str(n))
    for i in range(index_start, index_start + n):
        # Apply 0 padding to assure natural ordering
        s.append(f'{prefix}{str(i).zfill(width)}')
    s = coerce_set(s)
    return s


def get_state_set(n: int, prefix: str = 's', index_start: int = 0):
    return get_set_from_range(n, prefix, index_start)


def get_incidence_vector(s_prime: Set, s: Set) -> IncidenceVector:
    """Given a subset S' ⊆ S, return the corresponding incidence vector"""
    s_prime = coerce_set(s_prime)
    s = coerce_set(s)
    iv = get_zero_binary_vector(cardinality(s))
    for e in s_prime:
        e_index = s.index(e)
        iv[e_index] = True
    return iv


class KripkeStructure:
    def __init__(self, s, i, tm, ap, lm):
        # Set properties from inside __init__
        self._s = None
        self._i = None
        self._tm = None
        self._ap = None
        self._lm = None
        # Then call setters for consistency
        self.s = s
        self.i = i
        self.tm = tm
        self.ap = ap
        self.lf = lm

    @property
    def s(self):
        """The state set"""
        return self._s

    @s.setter
    def s(self, x):
        x = coerce_set(x)
        self._s = x

    @property
    def i(self):
        """The initial state set"""
        return self._i

    @s.setter
    def i(self, x):
        x = coerce_subset(x, self.s)
        self._i = x

    @property
    def tm(self):
        """The transition matrix"""
        return self._tm

    @s.setter
    def tm(self, x):
        x = coerce_binary_square_matrix(x)
        self._tm = x

    @property
    def ap(self):
        """The atomic property set"""
        return self._ap

    @s.setter
    def ap(self, x):
        x = coerce_set(x)
        self._ap = x

    @property
    def lm(self):
        """The labeling function mapping"""
        return self._lm

    @s.setter
    def lm(self, x):
        x = coerce_binary_matrix(x)
        self._lm = x
