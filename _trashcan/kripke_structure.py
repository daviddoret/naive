"""
.. module:: kripke_structure_types
   :platform: Unix, Windows
   :synopsis: Everything related to Kripke structure pythonic types
"""

# IMPORTS

# PEP 563 – Postponed Evaluation of Annotations
# Source: https://peps.python.org/pep-0563/
from __future__ import annotations

# import array
# import collections.abc as abc
import typing
# import dataclasses
# import array
import numpy as np
import logging
import collections.abc as abc
import nptyping as npt
import math

# import itertools
# import dataclasses




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
    elif t in (BinaryVector, BinaryVectorInput, IncidenceVector, IncidenceVectorInput, IndexPosition, IndexPositionInput):
        if isinstance(o, abc.Iterable):
            if all(isinstance(y, bool) for y in o):
                return True
            if all(isinstance(y, int) for y in o):
                return True
        return False
    else:
        raise NotImplementedError(f'is_instance: Could not determine if {o}[{type(o)}] is of type {t}')


# UTILITY FUNCTIONS




# OBJECT TYPING, DATA VALIDATION AND TYPE COERCION FUNCTIONS



def set_cardinality(s: SetOrIVInput) -> int:
    """Return the cardinality of a set *S*.

    Formally:

    .. math::
        \\begin{align*}
        & \\text{Let } S \\text{ be a set} & \\\\
        & \\mathit{set\\_cardinality}\\left(S\\right) \\colon= \\mathrm{card}(S) \\colon= |S|
        \\end{align*}

    Note: if a numeric vector is passed to the function, returns the number of elements in the vector, i.e. the *set cardinality* of the vector, and not the *vector cardinality*.

    :param s: The set *S*.
    :return: The cardinality of the set *S*.
    :rtype: int
    """
    if is_instance(s, SetInput):
        return len(s)
    elif is_instance(s, BinaryVectorInput):
        return len(s)
    elif is_instance(s, np.ndarray):
        # TODO: Check it is 1 dimensional
        return len(s)
    else:
        raise NotImplementedError(f'set_cardinality: Set {s} is of unsupported type {type(s)}')


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


def coerce_subset_or_iv(x: SetOrIVInput, s: SetInput) -> SetOrIV:
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


# OPERATORS

def equals(x: SetOrIVInput, y: SetOrIVInput, s: Set = None) -> bool:
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
        iv = get_zero_binary_vector(set_cardinality(s))
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


def get_maxima(v1: BinaryVector, v2: BinaryVector) -> BinaryVector:
    """Return the element-wise maxima of a binary vector with regard to another binary vector

    If the binary vector is the incidence vector of a set,
    this is equivalent to the set union operation:
    max(IV(s), IV(t)) ≡ s ∪ t
    """

    v1 = coerce_binary_vector(v1)
    v2 = coerce_binary_vector(v2)

    # Populate the values of the resulting vector
    # as the element-wise min of both vectors
    return coerce_binary_vector(np.maximum(v1, v2))


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
    :param s_prime: (conditional) The subset S' ⊆ S. Note that if s_prime is None, it is assumed that all states are considered and NOT no states (the empty set).
    :param output_type: (conditional) Set or IncidenceVector. Default equals Set.
    :return: The satisfaction set. If output_format is IncidenceVector, then the returned incidence vector is relative to the set S of the model, and not S'.
    """

    m = coerce_kripke_structure(m)
    if s_prime is not None:
        s_prime = coerce_subset_or_iv(s_prime, m.s)
    output_type = coerce_set_or_iv_type(output_type)

    # Get the size of the incidence vector
    s_cardinality = set_cardinality(m.s)

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
                          output_type: (type, typing.TypeVar) = Set) -> (AtomicPropertySet, IncidenceVector):
    """Given a Kripke structure M (m), and a state s ∈ S, return the set of labels (aka atomic properties) attached to that state.

    :param output_type:
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
        s_prime: (StateSetInput, None),
        label: AtomicPropertyInput,
        output_type: (type, typing.TypeVar) = Set) \
        -> (StateSet, IncidenceVector):
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
    :param s_prime: (conditional) The subset S' ⊆ S. Note that if s_prime is None, it is assumed that all states are considered and NOT no states (the empty set).
    :param label: The label (aka atomic property).
    :param output_type: (conditional) Set or IncidenceVector. Default equals Set.
    :return: The satisfaction set. If output_format is IncidenceVector, then the returned incidence vector is relative to the set S of the model, and not S'.

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
    :param s_prime: (conditional) The subset S' ⊆ S. Note that if s_prime is None, it is assumed that all states are considered and NOT no states (the empty set).
    :param sat_phi: The satisfaction set Sat(Φ).
    :param output_type: (conditional) Set or IncidenceVector. Default equals Set.
    :return: The satisfaction set. If output_format is IncidenceVector, then the returned incidence vector is relative to the set S of the model, and not S'.
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


def sat_phi_or_psi(m: KripkeStructure, s_prime: SetOrIVInput, sat_phi: SetOrIVInput,
                   sat_psi: SetOrIVInput, output_type: (type, typing.TypeVar) = Set) -> SetOrIV:
    """Get the satisfaction set of the state formula Sat(Φ ∨ Ψ)

    Formally:
    Let M be a Kripke structure's model with states S.
    Conditional: Let S' be a subset of S.
    Let Φ be a state formula.
    Let Ψ be a state formula.
    Lemma: Sat (Φ ∨ Ψ) = Sat (Φ) ∪ Sat (Ψ).
    Let Sat(Φ ∨ Ψ) = {s_i ∈ S' ⊆ S | s_i ∉ {Sat(Φ) ∪ Sat (Ψ)} }
    Let max(v1, v2) be the element-wise max operation
    For incidence vectors: max is equivalent to ∪ on sets
    Hence, Sat(Φ ∨ Ψ) ~ max(IV(Φ), IV(Ψ).

    :param m: The Kripke structure model M.
    :param s_prime: (conditional) The subset S' ⊆ S. Note that if s_prime is None, it is assumed that all states are considered and NOT no states (the empty set).
    :param sat_phi: The satisfaction set Sat(Φ).
    :param sat_psi: The satisfaction set Sat(Ψ).
    :param output_type: (conditional) Set or IncidenceVector. Default equals Set.
    :return: The satisfaction set. If output_format is IncidenceVector, then the returned incidence vector is relative to the set S of the model, and not S'.
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
    sat_psi = coerce_subset_or_iv(sat_psi, m.s)

    # Convert variables to incidence vectors
    s_prime_iv = get_incidence_vector(s_prime, m.s)
    sat_phi_iv = get_incidence_vector(sat_phi, m.s)
    sat_psi_iv = get_incidence_vector(sat_psi, m.s)

    # Get the element-wise maxima that is equivalent to the union set operation
    phi_or_psi_iv = get_maxima(sat_phi_iv, sat_psi_iv)

    # Reduce the result to S'
    phi_or_psi_iv = get_minima(phi_or_psi_iv, s_prime_iv)

    # Superfluous coercion
    phi_or_psi_iv = coerce_incidence_vector(phi_or_psi_iv, m.s)

    if output_type == Set:
        phi_or_psi_subset = get_set(phi_or_psi_iv, m.s)
        logging.debug(f'Sat({sat_phi} ∨ {sat_psi}) = {phi_or_psi_subset}')
        return phi_or_psi_subset
    else:
        logging.debug(f'Sat({sat_phi} ∨ {sat_psi}) = {phi_or_psi_iv}')
        return phi_or_psi_iv


def sat_phi_and_psi(m: KripkeStructure, s_prime: SetOrIVInput, sat_phi: SetOrIVInput,
                    sat_psi: SetOrIVInput, output_type: (type, typing.TypeVar) = Set) -> SetOrIV:
    """Get the satisfaction set of the state formula Sat(Φ ∧ Ψ)

    Formally:
    Let M be a Kripke structure's model with states S.
    Conditional: Let S' be a subset of S.
    Let Φ be a state formula.
    Let Ψ be a state formula.
    Lemma: Sat (Φ ∧ Ψ) = Sat (Φ) ∩ Sat (Ψ).
    Let Sat(Φ ∨ Ψ) = {s_i ∈ S' ⊆ S | s_i ∉ {Sat(Φ) ∩ Sat (Ψ)} }
    Let min(v1, v2) be the element-wise min operation
    For incidence vectors: min is equivalent to ∩ on sets
    Hence, Sat(Φ ∨ Ψ) ~ min(IV(Φ), IV(Ψ).

    :param m: The Kripke structure model M.
    :param s_prime: (conditional) The subset S' ⊆ S. Note that if s_prime is None, it is assumed that all states are considered and NOT no states (the empty set).
    :param sat_phi: The satisfaction set Sat(Φ).
    :param sat_psi: The satisfaction set Sat(Ψ).
    :param output_type: (conditional) Set or IncidenceVector. Default equals Set.
    :return: The satisfaction set. If output_format is IncidenceVector, then the returned incidence vector is relative to the set S of the model, and not S'.
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
    sat_psi = coerce_subset_or_iv(sat_psi, m.s)

    # Convert variables to incidence vectors
    s_prime_iv = get_incidence_vector(s_prime, m.s)
    sat_phi_iv = get_incidence_vector(sat_phi, m.s)
    sat_psi_iv = get_incidence_vector(sat_psi, m.s)

    # Get the element-wise minima that is equivalent to the union set operation
    phi_and_psi_iv = get_minima(sat_phi_iv, sat_psi_iv)

    # Reduce the result to S'
    phi_and_psi_iv = get_minima(phi_and_psi_iv, s_prime_iv)

    # Superfluous coercion
    phi_and_psi_iv = coerce_incidence_vector(phi_and_psi_iv, m.s)

    if output_type == Set:
        phi_or_psi_subset = get_set(phi_and_psi_iv, m.s)
        logging.debug(f'Sat({sat_phi} ∧ {sat_psi}) = {phi_or_psi_subset}')
        return phi_or_psi_subset
    else:
        logging.debug(f'Sat({sat_phi} ∧ {sat_psi}) = {phi_and_psi_iv}')
        return phi_and_psi_iv
