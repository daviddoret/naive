import lts
import state
import atom
import transition_matrix


def get_lts_sample_1():
    return lts.LTS(
        s=['Apple', 'Banana', 'Fox'],
        t=[[0, 1, 0],
           [1, 0, 1],
           [0, 1, 0]],
        a=['Animal', 'Vegetal'],
        lf=[[0, 0, 1],
            [1, 1, 0]],
    )


def get_lts_sample_2():
    return lts.LTS(
        s=state.StateSet(5),
        t=[[0, 1, 0, 0, 0],
           [0, 0, 1, 1, 0],
           [0, 0, 0, 0, 1],
           [0, 1, 1, 1, 0],
           [0, 0, 0, 0, 1]],
        a=atom.AtomSet(4),
        lf=[[1, 1, 1, 1, 0],
            [1, 1, 1, 0, 1],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0]]
    )


def get_transition_matrix_sample_1():
    return transition_matrix.TransitionMatrix([
        [0, 1, 0, 0, 0],
        [0, 0, 1, 1, 0],
        [0, 0, 0, 0, 1],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1]])
