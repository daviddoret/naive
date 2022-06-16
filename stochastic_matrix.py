import dataclasses
import output
import real_matrix
import numpy as np
import warnings


@dataclasses.dataclass
class StochasticMatrix(real_matrix.RealMatrix):
    """A stochastic matrix

    This is a real matrix with a validate method that assures
    rows sum to 1.
    """

    def __init__(self, source):
        super().__init__(source)
        if not self.check_consistency:
            warnings.warn('not self.check_consistency()')

    def __eq__(self, m2):
        return super().__eq__(m2)

    def __repr__(self):
        return super().__repr__()

    def check_consistency(self):
        # check parent class consistency
        if not super().check_consistency():
            warnings.warn('not super().check_consistency()')
            return False
        # check all matrix elements >= 0
        if not np.min(self.to_float_numpy_array()) >= 0:
            warnings.warn('not np.min(self.to_float_numpy_array()) >= 0')
            return False
        # check all matrix elements <= 1
        if not np.max(self.to_float_numpy_array()) <= 1:
            warnings.warn('not np.max(self.to_float_numpy_array()) <= 1')
            return False
        # check the sum of every row equals 1
        if not np.all(self.to_float_numpy_array().sum(axis=1) == 1):
            warnings.warn('not np.all(self.to_float_numpy_array().sum(axis=1) == 1)')
            return False
        # pass
        return True

    def copy(self):
        """Return a copy of itself"""
        return StochasticMatrix(self)


