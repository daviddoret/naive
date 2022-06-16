import dataclasses
import binary_matrix
import atom
import state
import numpy as np


@dataclasses.dataclass
class LabelingFunction:
    """A labeling function implemented as a rectangular binary array
    where the rows correspond to the indices of the labels,
    and the columns correspond to the indices of the states."""
    BinaryMatrix: binary_matrix.BinaryMatrix
    LabelSpace: atom.AtomSet
    StateSpace: state.StateSet

    def __init__(self, LabelSpace, StateSpace):
        self.LabelSpace = LabelSpace
        self.StateSpace = StateSpace
        self.BinaryMatrix = binary_matrix.BinaryMatrix(np.array(np.zeros((LabelSpace.get_dimension_1(), StateSpace.get_dimension_1())), dtype=bool))

    def __repr__(self):
        raise Exception('Not implemented')

    def link_label_to_state(self, l, s):
        self.BinaryMatrix[self.LabelSpace.index(l), self.StateSpace.get_element_index(s)] = True

    def get_label_states(self, l):
        """Given a label l, return all states that satisfy that label"""
        raise NotImplementedError('TODO');

    def get_state_labels(self, s):
        """Given a state s, return all labels that are satisfied by that state"""
        raise NotImplementedError('TODO');

    def CheckLabel(self, l, s):
        return self.BinaryMatrix[self.LabelSpace.index(l), self.StateSpace.get_element_index(s)]

    def to_latex_math(self):
        """Return a LaTeX matrix representation"""
        # TODO: Add row headers
        content = ''
        for row_index in range(0, self._NPM.shape[0]):
            row = self.AsIntNumpyArray()[row_index]
            row_latex = np.array2string(row, precision=3, separator=' && ')
            row_latex = row_latex.replace('[', '')
            row_latex = row_latex.replace(']', '')
            if row_index < self._NPM.shape[0] - 1:
                row_latex = f'{row_latex} \\\\'
            content = f'{content} {row_latex}'
        latex = f'\\begin{{bmatrix}} {content} \\end{{bmatrix}}'
        return latex

    def unlink_label_from_state(self, l, s):
        self.BinaryMatrix[self.LabelSpace.index(l), self.StateSpace.get_element_index(s)] = False

