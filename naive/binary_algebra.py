import naive.type_library as tl
import numpy as np


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
    return tl.coerce_binary_vector(np.zeros(size, dtype=bool))


def get_zero_binary_matrix(rows: int, columns) -> tl.BinaryMatrix:
    return tl.coerce_binary_matrix(np.zeros((rows, columns), dtype=bool))


def get_one_binary_vector(size: int) -> tl.BinaryVector:
    return tl.coerce_binary_vector(np.ones(size, dtype=bool))


def textify_binary_vector(v: tl.BinaryVectorInput) -> str:
    if v is None:
        return 'undefined'  # We interpret None as undefined
    elif len(v) == 0:
        return '[]'  # The empty set
    else:
        v = tl.coerce_binary_vector(v)
        v = np.array(v, dtype=int)
        v = np.array2string(v, precision=0, separator=' ')
        return v


def textify_binary_matrix(m: tl.BinaryMatrixInput) -> str:
    if m is None:
        return 'undefined'  # We interpret None as undefined
    elif len(m) == 0:
        return '[]'  # The empty set
    else:
        m = tl.coerce_binary_matrix(m)
        m = np.array(m, dtype=int)
        m = np.array2string(m, precision=0, separator=' ')
        return m


def print_binary_vector(v: tl.BinaryVectorInput):
    print(textify_binary_vector(v))


def print_binary_matrix(m: tl.BinaryMatrixInput):
    print(textify_binary_matrix(m))
