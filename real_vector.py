from dataclasses import dataclass
import numpy as np
import output
import binary_vector


@dataclass
class RealVector:
    """A real vector"""
    _NPV: np.array

    def to_latex_math_h(self):
        """Return a LaTeX horizontal vector representation"""
        content = np.array2string(self.to_float_numpy_array(), precision=output.DEFAULT_PRECISION, separator=' && ')
        content = content.replace('[', '')
        content = content.replace(']', '')
        latex = f'\\begin{{bmatrix}} {content} \\end{{bmatrix}}'
        return latex

    def to_latex_math_v(self):
        """Return a LaTeX vertical vector representation"""
        content = np.array2string(self.to_float_numpy_array(), precision=output.DEFAULT_PRECISION, separator=' \\\\ ')
        content = content.replace('[', '')
        content = content.replace(']', '')
        latex = f'\\begin{{bmatrix}} {content} \\end{{bmatrix}}'
        return latex

    def __init__(self, v):
        if isinstance(v, RealVector):
            self._NPV = np.copy(v._NPV)
        elif isinstance(v, binary_vector.BinaryVector):
            self._NPV = v.to_float_numpy_array()
        else:
            self._NPV = np.array(v, dtype=float).flatten()

    def __eq__(self, v2):
        return np.array_equal(self.to_float_numpy_array(), v2.to_float_numpy_array(), equal_nan=False)

    def __repr__(self):
        return str(self.to_float_numpy_array())

    def to_bool_numpy_array(self):
        """Return a copy as a Numpy.Array of dtype bool"""
        return np.array(self._NPV, dtype=bool)

    def to_float_numpy_array(self):
        """Return a copy as a Numpy.Array of dtype float"""
        return np.array(self._NPV, dtype=float)

    def to_int_numpy_array(self):
        """Return a copy as a Numpy.Array of dtype int"""
        return np.array(self._NPV, dtype=int)

    def copy(self):
        """Return a copy of itself"""
        return RealVector(self._NPV)


def test_real_vector():
    V = RealVector([1, 0.7777, 1, 0.17])
    output.output_math(V.to_latex_math_h())
    output.output_math(V.to_latex_math_v())
    print(V.to_bool_numpy_array())
    print(V.to_int_numpy_array())
    print(V.to_float_numpy_array())
    V2 = V.copy()
    print(V == V2)
    print(RealVector(V2))


test_real_vector()
