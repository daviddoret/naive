import naive.type_library as tl
import numpy as np


def equals(x: tl.BinaryVectorInput, y: tl.BinaryVectorInput) -> bool:
    """Check if two binary vectors are equal.

    """
    x = tl.coerce_binary_vector(x)
    y = tl.coerce_binary_vector(y)
    return np.array_equal(x, y)


def get_logical_not(v: tl.BinaryVectorInput) -> tl.BinaryVector:
    """Return the element-wise inverse (or logical not) of a binary vector.

    If the binary vector is the incidence vector of a set,
    this is equivalent to the or set operation:
    min(IV(s), IV(t)) ≡ s ∩ t
    """

    v = tl.coerce_binary_vector(v)
    v_inverse = np.logical_not(v)

    return tl.coerce_binary_vector(v_inverse)


def get_minima(v1: tl.BinaryVectorInput, v2: tl.BinaryVectorInput) -> tl.BinaryVector:
    """Return the element-wise minima of a binary vector with regard to another binary vector

    If the binary vector is the incidence vector of a set,
    this is equivalent to the set intersection operation:
    min(IV(s), IV(t)) ≡ s ∩ t

    :param v1:
    :param v2:
    :return:
    """

    v1 = tl.coerce_binary_vector(v1)
    v2 = tl.coerce_binary_vector(v2)

    # Populate the values of the resulting vector
    # as the element-wise min of both vectors
    return tl.coerce_binary_vector(np.minimum(v1, v2))


def get_maxima(v1: tl.BinaryVectorInput, v2: tl.BinaryVectorInput) -> tl.BinaryVector:
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


def get_zero_binary_vector(size: int) -> tl.BinaryVector:
    return np.zeros(size, dtype=bool)


def get_one_binary_vector(size: int) -> tl.BinaryVector:
    return np.ones(size, dtype=bool)
