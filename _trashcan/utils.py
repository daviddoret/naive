import numpy as np
from _trashcan import output
import dataclasses


@dataclasses.dataclass
class OrderedSet():
    """A utility class to mimic (small) finite ordered sets of arbitrary objects with an index.
    It may also be used to represent unordered sets for which we need an index,
    such as label spaces or state spaces, because indexes are programmatically useful,
    e.g. to populate incidence vectors."""
    _internal: dict

    def __getitem__(self, item):
        return self._ordered_dictionary[item]

    def __init__(self, *args: object, **kwargs: object):
        self._ordered_dictionary = collections.OrderedDict()
        if len(args) == 1:
            first_parameter = args[0]
            if isinstance(first_parameter, int):
                self.generate_from_range(*args)
            elif isinstance(first_parameter, collections.Iterable):
                self.generate_from_iterable(*args)
        elif 'source_object' in kwargs is not None:
            # Label "range" constructor
            self.generate_from_iterable(**kwargs)
        elif 'index_end' in kwargs is not None:
            # Label "range" constructor
            self.generate_from_range(**kwargs)

    def __iter__(self):
        return self._ordered_dictionary.__iter__()

    def __len__(self):
        return self.get_size()

    def __next__(self):
        return self._ordered_dictionary.__next__()

    def __repr__(self):
        return self.to_string()

def numpy_vector_verticalize(v):
    v_np = np.array(v)
    v_flat = v_np.flatten()
    V_vertical = v_flat[:, None]
    return V_vertical


# output_math( f'{output.tex(numpy_vector_verticalize([1,2,3]))}')
# print(numpy_vector_verticalize([1,2,3]).shape)

def numpy_vectory_horizontalize(v):
    v_np = np.array(v)
    v_flat = v_np.flatten()
    return v_flat


# output_math( f'{output.tex(numpy_vectory_horizontalize([1,2,3]))}')
# print(numpy_vectory_horizontalize([1,2,3]).shape)

def get_indicator_numeric(A):
    """ Return the indicator (or incidence) array (or matrix, or vector) of a stochastic or more generally numerical array (or matrix, or vector)

    All array components whose value = 0 are kept as is.
    All array components whose value <> 0 are set to 1.
    Therefore, if the source array A contains probabilities (0 <= x <= 1), the resulting array contains 1 for all non-zero probabilities.

    References
    ------------
        - https://en.wikipedia.org/wiki/Indicator_vector

    Parameters
    ------------
        A: numpy.array (any dtype)
            A numerical n-dimensional array (or matrix, or vector)
    Return
    ------------
        I: numpy.array (dtype=int)
            A numerical n-dimensional array (or matrix, or vector)
    """
    npA = np.array(A)
    I = np.array(npA != 0, dtype=int)

    # output.output_math(f'I({output.tex(A)}) = {output.tex(I)}')

    return I


def test_get_indicator_numeric():
    get_indicator_numeric([0, 1 / 3, .3])


test_get_indicator_numeric()


def get_identity_matrix(size):
    return np.identity(size)


def inverse_binary_array(A):
    # Substitute all 0s with 1s and 1s with 0s.
    # TODO: Validation checks for only 0s and 1s.
    A_inverse = np.absolute(np.subtract(A, 1))
    # output.output_math(tex(A_inverse))
    return A_inverse


def test_inverse_binary_array():
    inverse_binary_array([1.0, 0, 0, 0, 1, 1])


test_inverse_binary_array()


def I_set_complement(IS1):
    """ Return the indicator vector of the complement of a set: S1^C

    Parameters
    ------------
        IS1: numpy.array (dtype=int)
            The indicator vector of the set S1
    Return
    -----------
        IS2: numpy.array (dtype=int)
            The indicator vector of the complement of set S1
    """

    IS2 = np.array(np.logical_not(IS1), dtype=int)
    output.output_math(f'{output.tex(IS1)}^{{C}} = {output.tex(IS2)}')
    return IS2


def test_I_set_complement():
    IS1 = np.array([1, 0, 1, 0, 1])
    I_set_complement(IS1)


test_I_set_complement()


def I_set_union(IS1, IS2):
    """ Return the indicator vector of the union of two sets: S1 U S2

    Parameters
    ------------
        IS1: numpy.array (dtype=int)
            The indicator vector of the set S1
        IS2: numpy.array (dtype=int)
            The indicator vector of the set S2
    Return
    -----------
        IS3: numpy.array (dtype=int)
            The indicator vector of the union of sets S1 and S2
    """

    IS3 = np.maximum(IS1, IS2)
    output.output_math(f'{output.tex(IS1)} \\cup {output.tex(IS2)} = {output.tex(IS3)}')
    return IS3


def test_I_set_union():
    IS1 = np.array([1, 0, 1, 0, 1])
    IS2 = np.array([1, 1, 0, 0, 1])
    I_set_union(IS1, IS2)


test_I_set_union()


def I_set_difference(IS1, IS2):
    """ Return the indicator vector of the set difference of two sets: S1 \ S2

    Parameters
    ------------
        IS1: numpy.array (dtype=int)
            The indicator vector of the set S1
        IS2: numpy.array (dtype=int)
            The indicator vector of the set S2
    Return
    -----------
        IS3: numpy.array (dtype=int)
            The indicator vector of the set difference of sets S1 and S2
    """

    IS3 = np.array(np.maximum(np.subtract(IS1, IS2), np.zeros(len(IS1))), dtype=int)
    output.output_math(f'{output.tex(IS1)} \\setminus {output.tex(IS2)} = {output.tex(IS3)}')
    return IS3


def test_I_set_difference():
    IS1 = np.array([1, 0, 1, 0, 1])
    IS2 = np.array([1, 1, 0, 0, 1])
    I_set_difference(IS1, IS2)


test_I_set_difference()
