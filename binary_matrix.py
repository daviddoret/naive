import dataclasses
import numpy as np
import warnings

import binary_vector
import mstr


@dataclasses.dataclass
class BinaryMatrix:
    """A binary matrix"""
    _bool_numpy_array: np.array

    def __init__(self, source_object: object):
        if isinstance(source_object, BinaryMatrix):
            self._bool_numpy_array = np.array(np.copy(source_object._bool_numpy_array))
        else:
            self._bool_numpy_array = np.array(source_object, dtype=bool)
        self.check_consistency()

    def __eq__(self, comparable_object):
        """Element-wise equality"""
        return np.array_equal(self.to_bool_numpy_array(), comparable_object.to_bool_numpy_array(), equal_nan=False)

    def __getitem__(self, index):
        return self._bool_numpy_array[index]

    def __repr__(self):
        return self.to_multistring()

    def __setitem__(self, index, b):
        self._bool_numpy_array[index] = bool(b)

    def __str__(self):
        return self.to_multistring()

    def check_consistency(self) -> bool:
        # Internal type check
        if not isinstance(self._bool_numpy_array, np.ndarray):
            warnings.warn(f'not isinstance(self._float_numpy_array, np.array)')
            return False
        # Dimension check
        if not self._bool_numpy_array.ndim == 2:
            warnings.warn(f'not self.ndim == 2')
            return False
        # Shape check
        if not (self.get_dimension_1_length() == self.get_dimension_2_length()):
            warnings.warn('not (self.get_dimension_1_length() == self.get_dimension_2_length())')
            return False
        return True

    def copy(self):
        """Return a copy of itself"""
        return BinaryMatrix(self._bool_numpy_array)

    def get_dimension_1_length(self) -> int:
        return int(self._bool_numpy_array.shape[0])

    def get_dimension_2_length(self) -> int:
        return int(self._bool_numpy_array.shape[1])

    def get_column(self, i: int) -> binary_vector.BinaryVector:
        return binary_vector.BinaryVector(self._bool_numpy_array[:, i])

    def get_row(self, i: int) -> binary_vector.BinaryVector:
        # TODO: Correct the type hint for index
        return binary_vector.BinaryVector(self._bool_numpy_array[i, :])

    def to_bool_numpy_array(self):
        """Return a copy as a Numpy.Matrix of dtype bool"""
        return np.array(self._bool_numpy_array, dtype=bool)

    def to_int_numpy_array(self):
        """Return a copy as a Numpy.Matrix of dtype int"""
        return np.array(self._bool_numpy_array, dtype=int)

    def to_float_numpy_array(self):
        """Return a copy as a Numpy.Matrix of dtype float"""
        return np.array(self._bool_numpy_array, dtype=float)

    def to_latex_math(self) -> str:
        """Return a LaTeX matrix representation"""
        content = ''
        for row_index in range(0, self._bool_numpy_array.shape[0]):
            row = self.to_int_numpy_array()[row_index]
            row_latex = np.array2string(row, precision=3, separator=' && ')
            row_latex = row_latex.replace('[', '')
            row_latex = row_latex.replace(']', '')
            if row_index < self._bool_numpy_array.shape[0] - 1:
                row_latex = f'{row_latex} \\\\'
            content = f'{content} {row_latex}'
        latex = f'\\begin{{bmatrix}} {content} \\end{{bmatrix}}'
        return latex

    def to_unicode(self) -> str:
        return str(self.to_int_numpy_array())

    def to_multistring(self) -> mstr.MStr:
        return mstr.MStr(self.to_unicode(), self.to_latex_math())



