import dataclasses
import numpy as np
import output
import mstr


@dataclasses.dataclass
class BinaryVector:
    """A (small) finite binary vector"""
    _bool_numpy_array: np.array

    def __init__(self, source_object=None, size: int = None, value=None):
        # Assure expected typing

        if isinstance(source_object, BinaryVector):
            self._bool_numpy_array = source_object.to_bool_numpy_array()
        if size is not None and isinstance(size, int):
            if value is None:
                # By default, return a vector of zeroes
                value = False
            if value:
                self._bool_numpy_array = np.ones((size), dtype=bool)
            else:
                self._bool_numpy_array = np.zeros((size), dtype=bool)
        else:
            self._bool_numpy_array = np.array(source_object, dtype=bool).flatten()

    def __eq__(self, other_object):
        if not isinstance(other_object, BinaryVector):
            other_object = BinaryVector(other_object)
        # print(f'{self} == {other_object}')
        return np.array_equal(self.to_bool_numpy_array(), other_object.to_bool_numpy_array(), equal_nan=False)

    def __getitem__(self, index):
        return self._bool_numpy_array[index]

    def __repr__(self):
        return self.to_multistring()

    def __setitem__(self, index, b):
        self._bool_numpy_array[index] = bool(b)

    def __str__(self):
        return self.to_multistring()

    def check_masking(self, other_vector):
        """Check if this vector masks another vector with its 1s

        If this vector has a 1 for every 1 in the other vector, we can say that this vector 'masks' the other vector.
        Note that this vector may have supplementary 1s.
        Note that all vectors masks themselves."""

        # Retrieve the vector of maximal values
        max_vector = self.get_maximum(other_vector)

        # Compare the result with the present vector.
        # If no additional 1 appeared, the current vector masks the other vector.
        result = (self == max_vector)
        return result

    def copy(self):
        """Return a copy of itself"""
        return BinaryVector(self._bool_numpy_array)

    def get_inverse(self):
        """Return the inverse of the binary vector

        Every True (or 1) becomes a False (or 0).
        Every False (or 0) becomes a True (or 1).

        If the binary vector is the incidence vector of a set,
        this is equivalent to the complement or difference set operation:
        {e ∈ {0,1}|e = 0 if Se ∈ S, 1 otherwise} ≡ S∁
        """
        return BinaryVector(np.invert(self._bool_numpy_array))

    def get_maximum(self, other_vector):
        """Return the element-wise maximum of this set with another set

        If the binary vector is the incidence vector of a set,
        this is equivalent to the or set operation:
        max(IV(s), IV(t)) ≡ s ∪ t
        """
        if not isinstance(other_vector, BinaryVector):
            other_vector = BinaryVector(other_vector)
        return BinaryVector(np.maximum(self._bool_numpy_array, other_vector.to_bool_numpy_array()))

    def get_dimension_1_length(self):
        return self._bool_numpy_array.shape[0]

    def set_values_from_iterable(self, source_object):
        for i, e in enumerate(source_object):
            self[i] = e

    def to_bool_numpy_array(self):
        """Return a copy as a Numpy.Array of dtype bool"""
        return np.array(self._bool_numpy_array, dtype=bool)

    def to_float_numpy_array(self):
        """Return a copy as a Numpy.Array of dtype float"""
        return np.array(self._bool_numpy_array, dtype=float)

    def to_int_numpy_array(self):
        """Return a copy as a Numpy.Array of dtype int"""
        return np.array(self._bool_numpy_array, dtype=int)

    def to_latex_math(self):
        return self.to_latex_math_h()

    def to_latex_math_h(self):
        """Return a LaTeX horizontal vector representation"""
        content = np.array2string(self.to_int_numpy_array(), precision=0, separator=' && ')
        content = content.replace('[', '')
        content = content.replace(']', '')
        latex = f'\\begin{{bmatrix}} {content} \\end{{bmatrix}}'
        return latex

    def to_latex_math_v(self):
        """Return a LaTeX vertical vector representation"""
        content = np.array2string(self.to_int_numpy_array(), precision=0, separator=' \\\\ ')
        content = content.replace('[', '')
        content = content.replace(']', '')
        latex = f'\\begin{{bmatrix}} {content} \\end{{bmatrix}}'
        return latex

    def to_unicode(self):
        """Return a LaTeX vertical vector representation"""
        output_value = np.array2string(self.to_int_numpy_array(), precision=0, separator=', ')
        output_value = output_value.replace('[', '')
        output_value = output_value.replace(']', '')
        output_value = f'{{ {output_value} }}'
        return output_value

    def to_multistring(self):
        return mstr.MStr(self.to_unicode(), self.to_latex_math())

    def output(self):
        output.output(self.to_multistring())


def get_minima(vector_1: BinaryVector, vector_2: BinaryVector) -> BinaryVector:
    """Return the element-wise minimum of this set with another set

    If the binary vector is the incidence vector of a set,
    this is equivalent to the or set operation:
    min(IV(s), IV(t)) ≡ s ∩ t
    """

    # Assure expected types
    # Note that BinaryVector and subclasses such as IV are all supported
    if not isinstance(vector_1, BinaryVector):
        vector_1 = BinaryVector(vector_1)
    if not isinstance(vector_2, BinaryVector):
        vector_2 = BinaryVector(vector_2)
    # The output will be based on a copy of v1
    # to assure that the type of the output is identical to the type of v2,
    # which may be a subclass of BinaryVector such as IV
    output = vector_1.copy()

    # Populate the values of the resulting vector
    # as the element-wise min of both vectors
    output.set_values_from_iterable(np.minimum(vector_1.to_bool_numpy_array(), vector_2.to_bool_numpy_array()))

    return output
