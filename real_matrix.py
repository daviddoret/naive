import dataclasses

import numpy as np

import binary_matrix

import warnings

import output


@dataclasses.dataclass
class RealMatrix:
    """A real matrix

    Real numbers are mimicked by Python float which, of course, is a fundamental sin.
    """
    _float_numpy_array: np.array

    def __init__(self, source_object):
        if isinstance(source_object, RealMatrix):
            self._float_numpy_array = source_object.to_float_numpy_array()
        elif isinstance(source_object, binary_matrix.BinaryMatrix):
            self._float_numpy_array = source_object.to_float_numpy_array()
        elif isinstance(source_object, np.ndarray):
            self._float_numpy_array = np.array(np.copy(source_object), dtype=float)
        else:
            self._float_numpy_array = np.array(source_object, dtype=float)
        if not self.check_consistency():
            warnings.warn('not self.check_consistency()')

    def __eq__(self, comparable_object):
        """Element-wise equality"""
        if isinstance(comparable_object, RealMatrix):
            return np.array_equal(self.to_float_numpy_array(), comparable_object.to_float_numpy_array(),
                                  equal_nan=False)
        elif isinstance(comparable_object, np.array):
            return np.array_equal(self.to_float_numpy_array(), comparable_object, equal_nan=False)
        else:
            raise Exception(f'TODO: Add support for RealMatrix.__eq__ with type:{type(comparable_object)}')

    def __getitem__(self, index):
        return self._float_numpy_array[index]

    def __len__(self):
        return len(self._float_numpy_array)

    def __repr__(self):
        return str(self.to_float_numpy_array())

    def __setitem__(self, index, b):
        self._float_numpy_array[index] = float(b)

    def check_consistency(self):
        """Check whether the object is in a state such that it is a consistent real-matrix"""
        # Internal type check
        if not isinstance(self._float_numpy_array, np.ndarray):
            warnings.warn(f'not isinstance(self._float_numpy_array, np.array)')
            return False
        # Dimension check
        if not self._float_numpy_array.ndim == 2:
            warnings.warn(f'not self.ndim == 2')
            return False
        # Shape check
        if not (self.get_dimension_1_length() == self.get_dimension_2_length()):
            warnings.warn('not (self.get_dimension_1_length() == self.get_dimension_2_length())')
            return False
        # Ok, test passed
        return True

    def copy(self):
        """Return a copy of itself"""
        return RealMatrix(self._float_numpy_array)

    def get_dimension_1_length(self):
        return self._float_numpy_array.shape[0]

    def get_dimension_2_length(self):
        return self._float_numpy_array.shape[1]

    def to_bool_numpy_array(self):
        """Return a copy as a Numpy.Matrix of dtype bool"""
        return np.array(self._float_numpy_array, dtype=bool)

    def to_float_numpy_array(self):
        """Return a copy as a Numpy.Matrix of dtype float"""
        return np.array(self._float_numpy_array, dtype=float)

    def to_int_numpy_array(self):
        """Return a copy as a Numpy.Matrix of dtype int"""
        return np.array(self._float_numpy_array, dtype=int)

    def to_latex_math(self):
        """Return a LaTeX matrix representation"""
        content = ''
        for row_index in range(0, self._float_numpy_array.shape[0]):
            row = self.to_float_numpy_array()[row_index]
            row_latex = np.array2string(row, precision=3, separator=' && ')
            row_latex = row_latex.replace('[', '')
            row_latex = row_latex.replace(']', '')
            if row_index < self._float_numpy_array.shape[0] - 1:
                row_latex = f'{row_latex} \\\\'
            content = f'{content} {row_latex}'
        latex = f'\\begin{{bmatrix}} {content} \\end{{bmatrix}}'
        return latex

    def to_output_format(self):
        if output.OUTPUT_MODE == output.OUTPUT_LATEX_MATH:
            return self.to_latex_math()
        elif output.OUTPUT_MODE == output.OUTPUT_UNICODE:
            return self.to_unicode()
        else:
            raise NotImplementedError('Unknown output mode')

    def to_unicode(self):
        return np.array2string(self.to_float_numpy_array())

    def output(self):
        output.output(self.to_output_format())
