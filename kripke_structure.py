"""
.. module:: kripke_structure
   :platform: Unix, Windows
   :synopsis: A useful module indeed.
"""

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
import dataclasses

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
    IndexPositionInput,
)

State = Element
StateInput = typing.TypeVar(
    'StateInput',
    State,
    Element,
    ElementInput
)

AtomicProperty = str
AtomicPropertyInput = typing.TypeVar(
    'AtomicPropertyInput',
    AtomicProperty,
    ElementInput
)

SetInput = typing.TypeVar(
    'SetInput',
    abc.Iterable,
    typing.List[str],
    Set)

SetOrIV = typing.TypeVar(
    'SetOrIV',
    BinaryVector,
    IncidenceVector,
    Set)

SetOrIVInput = typing.TypeVar(
    'SetOrIVInput',
    BinaryVectorInput,
    IncidenceVectorInput,
    SetInput)


# IS INSTANCE FUNCTIONS

def is_instance(o: object, t: (type, typing.TypeVar)) -> bool:
    """Check if an arbitrary object o is of type or TypeVar t

    The native isinstance function does not support parametrized generics.
    Hence, we need a wrapper function to extend type checking.

    :param o: Any object
    :param t: A type or TypeVar
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
    elif t in (IncidenceVector, IncidenceVectorInput):
        if isinstance(o, abc.Iterable):
            if all(isinstance(y, bool) for y in o):
                return True
            if all(isinstance(y, int) for y in o):
                return True
        return False
    else:
        raise NotImplementedError(f'is_instance: Could not determine if {o}[{type(o)}] is of type {t}')


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
    if not isinstance(coerced_x, np.ndarray):
        try:
            coerced_x = np.asarray(coerced_x, dtype=bool)
        except ValueError as e:
            # If x is not bi-dimensional,
            # numpy raises the following error (which is expected):
            # ValueError: setting an array element with a sequence.
            # The requested array has an inhomogeneous shape after 1 dimensions.
            # The detected shape was (2,) + inhomogeneous part.
            raise ValueError(
                f'A binary matrix is bi-dimensional by definition. Please assure that {x}[{type(x)}] has an homogeneous shapre.')
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
    if isinstance(x, IncidenceVector):
        if s is None:
            # If the base set is not provided,
            # we assume it is the caller's intention
            # to not check the consistency of
            # the incidence vector with its base set.
            logging.warning('Skip subset test')
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


def coerce_subset_or_iv(x: object, s: SetInput) -> SetOrIV:
    if isinstance(x, IncidenceVector):
        return coerce_incidence_vector(x, s)
    elif is_instance(x, Set):
        return coerce_subset(x, s)
    else:
        # object is not of recognizable specialized type
        # in consequence we must make an arbitrage
        if isinstance(x, abc.Iterable):
            if all(isinstance(y, bool) for y in x):
                # Note that BinaryVector is equivalent to IncidenceVector
                return coerce_incidence_vector(x, s)
            elif all(isinstance(y, int) for y in x):
                # Note that BinaryVector is equivalent to IncidenceVector
                return coerce_incidence_vector(x, s)
            elif all(isinstance(y, str) for y in x):
                return coerce_set(x)
            raise NotImplementedError('Unsupported iterable')
        else:
            raise NotImplementedError('Unsupported type')


def coerce_atomic_property_set(ap: AtomicPropertySetInput):
    return coerce_set(ap)


def coerce_state_set(s: StateSetInput):
    return coerce_set(s)


def coerce_state_subset(s_prime_flexible: StateSetInput, s_flexible: StateInput):
    s_flexible = coerce_set(s_flexible)
    if is_instance(s_prime_flexible, StateSetInput):
        return coerce_subset(s_prime_flexible, s_flexible)
    elif is_instance(s_prime_flexible, IncidenceVectorInput):
        return coerce_incidence_vector(s_prime_flexible, s_flexible)
    else:
        raise NotImplementedError(f'coerce_state_subset: Unknown type: {s_prime_flexible}[{type(s_prime_flexible)}]')


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
        if e in s:
            return e
        else:
            logging.error(f'Element {e} is not an element of set {s}')
            raise ValueError(f'Element {e} is not an element of set {s}')
    elif isinstance(e, IndexPosition):
        if s is None:
            logging.error(f'Element {e} passed by index but set s is None')
            raise ValueError(f'Element {e} passed by index but set s is None')
        elif 0 <= IndexPosition < len(s):
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


def coerce_set_or_iv_type(python_type):
    if python_type == IncidenceVector:
        return python_type
    else:

        return Set


# OPERATORS

def equals(x: object, y: object, s: Set = None) -> bool:
    x = coerce_subset_or_iv(x, s)
    y = coerce_subset_or_iv(y, s)
    if isinstance(x, np.ndarray) and isinstance(y, np.ndarray):
        # Provide generic support for BinaryVector, IncidenceVector, BinaryMatrix, etc., etc.
        return np.array_equal(x, y)
    if is_instance(x, Set):
        return x == y
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


def get_set(s_prime: SetOrIVInput, s: Set) -> Set:
    """Given a subset S' ⊆ S or its incidence vector, return the corresponding subset"""
    s_prime = coerce_subset_or_iv(s_prime, s)
    s = coerce_set(s)
    if isinstance(s_prime, IncidenceVector):
        iv = coerce_incidence_vector(s_prime, s)
        s_prime_idx = np.flatnonzero(iv)
        s_prime_set = [str(s[i]) for i in s_prime_idx]
        s_prime_set = coerce_subset(s_prime_set, s)
        return s_prime_set
    elif is_instance(s_prime, Set):
        # s' is already a set
        # coerce it and push it back
        s_prime_set = coerce_subset(s_prime, s)
        return s_prime_set
    else:
        raise TypeError('Something weird happened, a bug is hiding')


def get_incidence_vector(s_prime: SetOrIVInput, s: Set) -> IncidenceVector:
    """Given a subset S' ⊆ S or its incidence vector, return the corresponding incidence vector"""
    s_prime = coerce_subset_or_iv(s_prime, s)
    s = coerce_set(s)
    if isinstance(s_prime, IncidenceVector):
        # s' is already an incidence vector
        # coerce it and push it back
        iv = coerce_incidence_vector(s_prime, s)
        return iv
    elif is_instance(s_prime, Set):
        iv = get_zero_binary_vector(cardinality(s))
        for e in s_prime:
            e_index = s.index(e)
            iv[e_index] = True
        iv = coerce_incidence_vector(iv, s)
        return iv
    else:
        raise TypeError('Something weird happened, a bug is hiding')


class KripkeStructure:
    def __init__(self, s, i, tm, ap, lm):
        # Initialize properties from inside __init__
        self._s = None
        self._i = None
        self._tm = None
        self._ap = None
        self._lm = None
        # Call properties to assure consistency
        self.s = s
        self.i = i
        self.tm = tm
        self.ap = ap
        self.lm = lm

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
        """The initial set that is a subset of the state set"""
        return self._i

    @i.setter
    def i(self, x):
        x = coerce_subset(x, self.s)
        self._i = x

    @property
    def tm(self):
        """The transition square matrix"""
        return self._tm

    @tm.setter
    def tm(self, x):
        x = coerce_binary_square_matrix(x)
        self._tm = x

    @property
    def ap(self):
        """The atomic property set"""
        return self._ap

    @ap.setter
    def ap(self, x):
        x = coerce_set(x)
        self._ap = x

    @property
    def lm(self):
        """The labeling function mapping matrix"""
        return self._lm

    @lm.setter
    def lm(self, x):
        x = coerce_binary_matrix(x)
        self._lm = x


KripkeStructureInput = typing.TypeVar(
    'KripkeStructureInput',
    KripkeStructure,
    dict)


def coerce_kripke_structure(m: KripkeStructureInput) -> KripkeStructure:
    if isinstance(m, KripkeStructure):
        return m
    elif isinstance(m, dict):
        s = m.get('s', None)
        i = m.get('i', None)
        tm = m.get('tm', None)
        ap = m.get('ap', None)
        lm = m.get('lm', None)
        coerced_m = KripkeStructure(s, i, tm, ap, lm)
        logging.debug(f'Coerce {m}[{type(m)}] to Kripke structure {coerced_m}')
        return coerced_m
    else:
        raise ValueError


def to_text(o: object) -> str:
    if isinstance(o, KripkeStructure):
        return f'({o.s}, {o.i}, {o.tm}, {o.ap}, {o.lm})'
    else:
        raise NotImplementedError


def set_element_values_from_iterable(target, source: abc.Iterable):
    # TODO: Add some type checking here as well
    for i, e in enumerate(source):
        target[i] = e


def get_minima(v1: BinaryVector, v2: BinaryVector) -> BinaryVector:
    """Return the element-wise minima of a binary vector with regard to another binary vector

    If the binary vector is the incidence vector of a set,
    this is equivalent to the set intersection operation:
    min(IV(s), IV(t)) ≡ s ∩ t
    """

    v1 = coerce_binary_vector(v1)
    v2 = coerce_binary_vector(v2)

    # Populate the values of the resulting vector
    # as the element-wise min of both vectors
    return coerce_binary_vector(np.minimum(v1, v2))


def get_logical_not(v: BinaryVector) -> BinaryVector:
    """Return the element-wise inverse (or logical not) of a binary vector.

    If the binary vector is the incidence vector of a set,
    this is equivalent to the or set operation:
    min(IV(s), IV(t)) ≡ s ∩ t
    """

    v = coerce_binary_vector(v)
    v_inverse = np.logical_not(v)

    return coerce_binary_vector(v_inverse)


def sat_tt(m: KripkeStructure, s_prime: SetOrIVInput = None, output_type: (type, typing.TypeVar) = Set) -> SetOrIV:
    """Get the satisfaction set of the state formula Sat(tt)

    Formally:
    Let M be a Kripke Structure model with states S.
    Conditional: Let S' be a subset of S.
    Let tt be the tautological truth state formula.
    Let Sat(tt) = {s ∈ S' ⊆ S}.

    :param m: The Kripke structure model M.
    :param s_prime: (conditional) The subset S' ⊆ S. Note that if s_prime is None, it is assumed that all states are
    considered and NOT no states (the empty set).
    :param output_type: (conditional) Set or IncidenceVector. Default equals Set.
    :return: The satisfaction set. If output_format is IncidenceVector, then the returned incidence vector is relative
    to the set S of the model, and not S'.
    """

    m = coerce_kripke_structure(m)
    if s_prime is not None:
        s_prime = coerce_subset_or_iv(s_prime, m.s)
    output_type = coerce_set_or_iv_type(output_type)

    # Get the size of the incidence vector
    s_cardinality = cardinality(m.s)

    # Prepare an incidence vector of that size with all ones
    sat_iv = get_one_binary_vector(s_cardinality)

    if s_prime is not None:
        # Work internally with incidence vectors
        s_prime_iv = get_incidence_vector(s_prime, m.s)
        # Limit the result to the requested set
        sat_iv = get_minima(sat_iv, s_prime_iv)

    # Note that if s' is None,
    # it is assumed that we consider all states
    # and NOT no states (the empty set).

    if output_type == Set:
        return get_set(sat_iv, m.s)
    else:
        return sat_iv


def get_labels_from_state(m: KripkeStructureInput, s: StateInput,
                          output_type: (type, typing.TypeVar) = Set) -> AtomicPropertySet:
    """Given a Kripke structure M (m), and a state s ∈ S, return the set of labels (aka atomic properties) attached to that state.

    :param m: The Kripke structure M
    :param s: A state s
    :return:
    """
    m = coerce_kripke_structure(m)
    s = coerce_state(s, m.s)
    output_type = coerce_set_or_iv_type(output_type)

    # Get the index position of s
    s_index = m.s.index(s)

    # Get the s_index column from the label mapping matrix
    # This corresponds to the label incidence vector
    label_iv = m.lm[:, s_index]
    # Superfluous coercion
    label_iv = coerce_incidence_vector(label_iv, m.ap)

    if output_type == Set:
        label_set = get_set(label_iv, m.ap)
        logging.debug(f'L({s}) = {label_set}')
        return label_set
    else:
        logging.debug(f'L({s}) = {label_iv}')
        return label_iv


def get_states_from_label(
        m: KripkeStructureInput,
        s_prime: StateSetInput,
        label: AtomicPropertyInput,
        output_type: (type, typing.TypeVar) = Set) \
        -> StateSet:
    """Return the states linked to a label

    Given a Kripke structure M (m),
    (conditionally) given a subset S' of S,
    given a label (aka atomic property) ∈ AP,
    return the subset of states S'' ⊆ S (or S') that are attached to that label.

    :param m: The Kripke structure M
    :param s_prime: None to exhaustively analyse M, or a subset of S to limit the analysis otherwise.
    :param label: The label (aka atomic property) ap
    :param output_type: Set or IncidenceVector depending on the desired output
    :return: The subset S'' ⊆ S
    """
    m = coerce_kripke_structure(m)
    if s_prime is None:
        # Exhaustive analysis of M
        s_prime = m.s
    else:
        # Limited analysis of M to a subset S' ⊆ S
        s_prime = coerce_state_subset(s_prime, m.s)
    s_prime_iv = get_incidence_vector(s_prime, m.s)
    label = coerce_atomic_property(label, m.ap)
    output_type = coerce_set_or_iv_type(output_type)

    # Get the index label a
    a_index = m.ap.index(label)

    # Get the a_index row from the label mapping matrix
    # This corresponds to the state incidence vector
    # This is equivalent to Sat(S)
    labeled_states_iv = m.lm[a_index, :]

    # Take the element-wise min of S' and Sat(S),
    # which is equivalent to the set intersection.
    s_prime_prime_iv = get_minima(s_prime_iv, labeled_states_iv)

    # Superfluous coercion
    s_prime_prime_iv = coerce_incidence_vector(s_prime_prime_iv, m.s)

    if output_type == Set:
        s_prime_prime_subset = get_set(s_prime_prime_iv, m.s)
        logging.debug(f'States({label}) = {s_prime_prime_subset}')
        return s_prime_prime_subset
    else:
        logging.debug(f'States({label}) = {s_prime_prime_iv}')
        return s_prime_prime_iv


def sat_a(m: KripkeStructure, s_prime: SetOrIVInput, label: AtomicPropertyInput,
          output_type: (type, typing.TypeVar) = Set) -> SetOrIV:
    """Get the satisfaction set of the state formula Sat(a)

    Formally:
    Let M be an LTS model with states S.
    Conditional: Let S' be a subset of S.
    Let a be a label (aka atomic property).
    Let L(s) be the set of labels (aka atomic properties) attached to s.
    Let Sat(a) = {s_i ∈ S' ⊆ S | a ∈ L(s_i)}

    :param m: The Kripke structure model M.
    :param s_prime: (conditional) The subset S' ⊆ S. Note that if s_prime is None, it is assumed that all states are
    considered and NOT no states (the empty set).
    :param label: The label (aka atomic property).
    :param output_type: (conditional) Set or IncidenceVector. Default equals Set.
    :return: The satisfaction set. If output_format is IncidenceVector, then the returned incidence vector is relative
    to the set S of the model, and not S'.
    """
    # These are synonymous
    # Coercion takes place in the child method
    sat_a_result = get_states_from_label(m, s_prime, label, output_type)
    logging.debug(f'Sat({label}) = {sat_a_result}')
    return sat_a_result


def sat_not_phi(m: KripkeStructure, s_prime: SetOrIVInput, sat_phi: SetOrIVInput,
                output_type: (type, typing.TypeVar) = Set) -> SetOrIV:
    """Get the satisfaction set of the state formula Sat(¬Φ)

    Formally:
    Let M be an LTS model with states S.
    Conditional: Let S' be a subset of S.
    Let Φ be a state formula.
    Lemma: Sat(¬Φ) = S ∖ Sat(Φ).
    Let Sat(a) = {s_i ∈ S' ⊆ S | s_i ∉ Sat(Φ)}

    :param m: The Kripke structure model M.
    :param s_prime: (conditional) The subset S' ⊆ S. Note that if s_prime is None, it is assumed that all states are
    considered and NOT no states (the empty set).
    :param sat_phi: The satisfaction set Sat(Φ).
    :param output_type: (conditional) Set or IncidenceVector. Default equals Set.
    :return: The satisfaction set. If output_format is IncidenceVector, then the returned incidence vector is relative
    to the set S of the model, and not S'.
    """
    # These are synonymous
    m = coerce_kripke_structure(m)
    if s_prime is None:
        # Exhaustive analysis of M
        s_prime = m.s
    else:
        # Limited analysis of M to a subset S' ⊆ S
        s_prime = coerce_subset_or_iv(s_prime, m.s)
    sat_phi = coerce_subset_or_iv(sat_phi, m.s)

    # Convert variables to incidence vectors
    s_prime_iv = get_incidence_vector(s_prime, m.s)
    sat_phi_iv = get_incidence_vector(sat_phi, m.s)

    not_sat_phi_iv = get_logical_not(sat_phi_iv)
    min_not_sat_phi_iv = get_minima(s_prime_iv, not_sat_phi_iv)

    # Superfluous coercion
    min_not_sat_phi_iv = coerce_incidence_vector(min_not_sat_phi_iv, m.s)

    if output_type == Set:
        min_not_sat_phi_subset = get_set(min_not_sat_phi_iv, m.s)
        logging.debug(f'Sat(¬{sat_phi}) = {min_not_sat_phi_subset}')
        return min_not_sat_phi_subset
    else:
        logging.debug(f'Sat(¬{sat_phi}) = {min_not_sat_phi_iv}')
        return min_not_sat_phi_iv
