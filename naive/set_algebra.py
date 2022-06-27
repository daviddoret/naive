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
import naive.type_library as tl
import naive.binary_algebra as ba


# import itertools
# import dataclasses


# IS INSTANCE FUNCTIONS

# UTILITY FUNCTIONS


# OBJECT TYPING, DATA VALIDATION AND TYPE COERCION FUNCTIONS


def equal(s: tl.SetInput, t: tl.SetInput) -> bool:
    """Check if two sets S and T are equal.

    Formally:

    .. math::
        \\begin{align*}
        & \\text{Let } S \\text{ be a set with elements } (s_1, s_2, \\cdots, s_n) & \\\\
        & \\text{Let } T \\text{ be a set with elements }  (t_1, t_2, \\cdots, t_m) & \\\\
        & S = T \\iff ((|S| = |T|) \\land (\\forall e \\in S, e \\in T) \\land (\\forall e \\in T, e \\in S))
        \\end{align*}

    :param s: The set S.
    :param t: The set T.
    :return: True if S and T are equal, False otherwise.
    """

    s = tl.coerce_set(s)  # Assure uniqueness and canonical ordering
    t = tl.coerce_set(t)  # Assure uniqueness and canonical ordering
    return s == t


def set_cardinality(s: tl.SetOrIVInput) -> int:
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
    if tl.is_instance(s, tl.SetInput):
        return len(s)
    elif tl.is_instance(s, tl.BinaryVectorInput):
        return len(s)
    elif tl.is_instance(s, np.ndarray):
        # TODO: Check it is 1 dimensional
        return len(s)
    else:
        raise NotImplementedError(f'set_cardinality: Set {s} is of unsupported type {type(s)}')


# OPERATORS

def equals(x: tl.SetOrIVInput, y: tl.SetOrIVInput, s: tl.Set = None) -> bool:
    x = tl.coerce_subset_or_iv(x, s)
    y = tl.coerce_subset_or_iv(y, s)
    if isinstance(x, np.ndarray) and isinstance(y, np.ndarray):
        # Provide generic support for BinaryVector, IncidenceVector, BinaryMatrix, etc., etc.
        return np.array_equal(x, y)
    if tl.is_instance(x, tl.Set):
        return x == y
    else:
        raise TypeError('Unsupported type')


def get_set_from_range(n: int, prefix: str = 'e', index_start: int = 0):
    """Generate a set of n elements, prefixed and numbered with 0 padding"""
    s = []
    width = len(str(n))
    for i in range(index_start, index_start + n):
        # Apply 0 padding to assure natural ordering
        s.append(f'{prefix}{str(i).zfill(width)}')
    s = tl.coerce_set(s)
    return s


def get_state_set(n: int, prefix: str = 's', index_start: int = 0):
    return get_set_from_range(n, prefix, index_start)


def get_set(s_prime: tl.SetOrIVInput, s: tl.Set) -> tl.Set:
    """Given a subset S' ⊆ S or its incidence vector, return the corresponding subset"""
    s_prime = tl.coerce_subset_or_iv(s_prime, s)
    s = tl.coerce_set(s)
    if isinstance(s_prime, tl.IncidenceVector):
        iv = tl.coerce_incidence_vector(s_prime, s)
        s_prime_idx = np.flatnonzero(iv)
        s_prime_set = [str(s[i]) for i in s_prime_idx]
        s_prime_set = tl.coerce_subset(s_prime_set, s)
        return s_prime_set
    elif tl.is_instance(s_prime, tl.Set):
        # s' is already a set
        # coerce it and push it back
        s_prime_set = tl.coerce_subset(s_prime, s)
        return s_prime_set
    else:
        raise TypeError('Something weird happened, a bug is hiding')


def get_incidence_vector(s_prime: tl.SetOrIVInput, s: tl.Set) -> tl.IncidenceVector:
    """Given a subset S' ⊆ S or its incidence vector, return the corresponding incidence vector"""
    s_prime = tl.coerce_subset_or_iv(s_prime, s)
    s = tl.coerce_set(s)
    if isinstance(s_prime, tl.IncidenceVector):
        # s' is already an incidence vector
        # coerce it and push it back
        iv = tl.coerce_incidence_vector(s_prime, s)
        return iv
    elif tl.is_instance(s_prime, tl.Set):
        iv = ba.get_zero_binary_vector(set_cardinality(s))
        for e in s_prime:
            e_index = s.index(e)
            iv[e_index] = True
        iv = tl.coerce_incidence_vector(iv, s)
        return iv
    else:
        raise TypeError('Something weird happened, a bug is hiding')


def set_element_values_from_iterable(target, source: abc.Iterable):
    # TODO: Add some type checking here as well
    for i, e in enumerate(source):
        target[i] = e
