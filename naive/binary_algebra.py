import type_library as tl
import numpy as np


def get_minima(v1: tl.BinaryVector, v2: tl.BinaryVector) -> tl.BinaryVector:
    """Return the element-wise minima of a binary vector with regard to another binary vector

    If the binary vector is the incidence vector of a set,
    this is equivalent to the set intersection operation:
    min(IV(s), IV(t)) ≡ s ∩ t
    """

    v1 = tl.coerce_binary_vector(v1)
    v2 = tl.coerce_binary_vector(v2)

    # Populate the values of the resulting vector
    # as the element-wise min of both vectors
    return tl.coerce_binary_vector(np.minimum(v1, v2))


def get_maxima(v1: tl.BinaryVector, v2: tl.BinaryVector) -> tl.BinaryVector:
    """Return the element-wise maxima of a binary vector with regard to another binary vector

    If the binary vector is the incidence vector of a set,
    this is equivalent to the set union operation:
    max(IV(s), IV(t)) ≡ s ∪ t
    """

    v1 = tl.coerce_binary_vector(v1)
    v2 = tl.coerce_binary_vector(v2)

    # Populate the values of the resulting vector
    # as the element-wise min of both vectors
    return tl.coerce_binary_vector(np.maximum(v1, v2))