import warnings
import mstr
import state
from _trashcan import binary_vector, binary_array, atom, const, output
import collections
import transition_matrix
import abc


class LTS:
    """LTS (Labeling Transition System)"""

    def __init__(
            self,
            s: state.StateSet,
            t: transition_matrix.TransitionMatrix,
            a: atom.AtomSet,
            lf: binary_array.BinaryArray):
        """Initialize an LTS instance

        :param s: (StateSet) S: A finite set of states
        :param t: (BinaryMatrix) The LTS transition matrix T
        :param a: (LabelSet) The LTS atom set A (aka atomic properties or atomic propositions AP)
        :param lf: (BinaryArray) The map of the LTS labeling function L
        :return:
        """
        self.s = state.StateSet(s)
        self.t = transition_matrix.TransitionMatrix(t)
        self.a = atom.AtomSet(a)
        self.lf = binary_array.BinaryArray(lf)

    def __repr__(self):
        return self.to_multistring()

    def __str__(self):
        return self.to_multistring()

    def check_a_from_s(self, s: state.State, a: atom.Atom) -> bool:
        return a in self.get_a_from_s(s)

    def check_consistency(self) -> bool:
        if not self.s.check_consistency():
            warnings.warn('CONSISTENCY ERROR: State space is inconsistent: not self.s.check_consistency()')
            return False
        if not self.t.check_consistency():
            warnings.warn('CONSISTENCY ERROR: Transition matrix is inconsistent: not self.t.check_consistency()')
            return False
        if not self.a.check_consistency():
            warnings.warn('CONSISTENCY ERROR: Atom set is inconsistent: not self.a.check_consistency()')
            return False
        if not self.lf.check_consistency():
            warnings.warn(
                'CONSISTENCY ERROR: Labeling function''s mapping array is inconsistent: not self.l.check_consistency()')
            return False
        if not (self.s.get_dimension_1() == self.t.get_dimension_1_length()):
            warnings.warn('not (self.S.get_dimension_1_length() == self.T.get_dimension_1_length())')
            return False
        if not (self.s.get_dimension_1() == self.t.get_dimension_2_length()):
            warnings.warn('not (self.S.get_dimension_1_length() == self.T.get_dimension_1_length())')
            return False
        if not (self.a.get_dimension_1() == self.lf.get_dimension_1_length()):
            warnings.warn('not (self.AP.get_dimension_1() == self.L.get_dimension_1_length())')
            return False
        if not (self.s.get_dimension_1() == self.lf.get_dimension_2_length()):
            warnings.warn('not (self.S.get_dimension_1() == self.L.get_dimension_2_length())')
            return False
        return True

    def check_s_from_a(self, a: atom.Atom, s: state.State) -> bool:
        return s in self.get_s_set_from_a(a)

    def get_s_iv_from_a(self, a: atom.Atom) -> state.IV:
        """Return the state incidence vector from a label, a label index, a label subset or a label incidence vector"""
        if a is None:
            # Return an empty incidence vector
            return state.IV(size=len(self.s))
        elif isinstance(a, int):
            # By index
            index = a
            return state.IV(self.lf[index, :])
        elif isinstance(a, str):
            # By key (supports MultiString as well)
            key = a
            index = self.a.index(key)
            return state.IV(self.lf[index, :])
        elif isinstance(a, state.IV):
            # By incidence vector
            index = a
            return state.IV(self.lf[index, :])
        elif isinstance(a, collections.Iterable):
            index = self.a.get_incidence_vector(a)
            return state.IV(self.lf[index, :])
        else:
            raise TypeError('Unsupported type')

    def get_s_set_from_a(self, a: atom.Atom) -> state.StateSet:
        """Return the state set from an atom, an atom index, an atom subset or an atom incidence vector"""
        return self.s.get_set(self.get_s_iv_from_a(a))

    def get_s_immediate_successors_subset(self, s: state.State) -> state.StateSet:
        """Return the set of the immediate successors of s

        Return the subset of the immediate successors of s from the transition matrix t.
        Note that s itself is not included unless it is its own successor.
        """
        s_index = self.s.index(s)
        iv = self.t.get_immediate_successors_iv(s_index)
        subset = self.s.get_set(iv)
        return subset

    def get_s_path_set(self, s: state.State) -> state.StateSet:
        """Return the set of states in Path(s), i.e. {Path(s)}

        Path(s) is infinite.
        By definition, the set of states in Path(s), noted {Path(s)}, is finite and is a subset of S.

        :param s: The state s
        :return: {Path(s)}
        """

        # Get the index position of s in S
        s_index = self.s.index(s)

        # Compute the incidence vector of {Path(s)} from the transition matrix
        s_path_set_iv = self.t.get_s_path_set_iv(s_index)

        # Convert the incidence matrix to a set of states
        s_path_set = self.s.get_set(s_path_set_iv)

        output.output2(const.DETAILED, mstr.MStr(f'{{Path({s})}} = ',
                                                 f'\\left{{\\text{{Path}}({s})\\right}} = ') + s_path_set.to_mstr())
        return s_path_set

    def get_a_iv_from_s(self, s: state.State):
        """Return the label incidence vector from a state, a state index, a state subset or a state incidence vector"""
        if s is None:
            # Return an empty incidence vector
            return state.IV(size=len(self.a))
        elif isinstance(s, int):
            # By index
            index = s
            return state.IV(self.lf[:, index])
        elif isinstance(s, str):
            # By key (supports MultiString as well)
            key = s
            index = self.s.index(key)
            return state.IV(self.lf[:, index])
        elif isinstance(s, state.IV):
            # By incidence vector
            index = s
            return state.IV(self.lf[:, index])
        elif isinstance(s, collections.Iterable):
            index = self.s.get_iv(s)
            return state.IV(self.lf[:, index])
        else:
            raise TypeError('Unsupported type')

    def get_a_from_s(self, s: state.State) -> atom.AtomSet:
        """Return the atom subset from a state, a state index, a state subset or a state incidence vector"""
        return self.a.get_subset(self.get_a_iv_from_s(s))

    def to_latex_math(self):
        return f'\\left( S\\colon={self.s.to_latex_math_v()}, T\\colon={self.t.to_latex_math()}, A\\colon={self.a.to_latex_math_v()}, L\\colon={self.lf.to_latex_math()} \\right) '

    def to_unicode(self):
        return f'( {self.s.to_unicode()}, \n{self.t.to_unicode()}, \n{self.a.to_unicode()}, \n{self.lf.to_unicode()})'

    def to_multistring(self):
        return mstr.MStr(self.to_unicode(), self.to_latex_math())

    def output(self):
        output.output(self.to_multistring())


class StateFormula(abc.ABC):
    @abc.abstractmethod
    def compute(self, m: LTS, s: state.StateInput = None) -> state.StateOutput:
        """Get the incidence vector of the satisfaction set

        Apply the state formula to the LTS model,
        or conditionally to a single state or a subset of states,
        and return the incidence vector of the resulting satisfaction set.

        The returned incidence vector is always relative to the complete set of model states.

        Formally:
        Let M be an LTS model with states S.
        Let S' be a subset of S.
        Let 𝛷 be the state formula.
        Let Sat(𝛷) be the satisfaction set of 𝛷 limited to S'.
        Let IV(Sat(𝛷)) be the incidence vector of Sat(𝛷) relative to S.

        :param m: The LTS model M
        :param s: (conditional) The subset of states S'
        :return: The incidence vector IV(Sat(𝛷))
        """
        pass

    @abc.abstractmethod
    def compute(self, m: LTS, s: state.StateInput = None) -> state.StateSet:
        """Get the satisfaction set

        Apply the state formula to the LTS model,
        or conditionally to a single state or a subset of states,
        and return the satisfaction set.

        Formally:
        Let M be an LTS model with states S.
        Let S' be a subset of S.
        Let 𝛷 be the state formula.
        Let Sat(𝛷) be the satisfaction set of 𝛷 limited to S'.

        :param m: The LTS model M
        :param s: (conditional) The subset of states S'
        :return: The satisfaction set Sat(𝛷)
        """
        pass


class ZeroaryStateFormula(StateFormula, abc.ABC):
    pass


class UnaryStateFormula(StateFormula, abc.ABC):
    pass


class BinaryStateFormula(StateFormula, abc.ABC):
    pass


def tt(m: LTS, s: state.StateInput = None, output_type: type = state.StateSet) -> state.StateOutput:
    """Get the satisfaction set of the tt state formula

    Apply the state formula tt to the LTS model,
    or conditionally to a single state or a subset of states,
    and return the satisfaction set.

    Formally:
    Let M be an LTS model with states S.
    Let S' be a subset of S.
    Let tt be the tautological truth state formula.
    Let Sat(tt) be the satisfaction set of tt in S'.

    In short:
    {s ∈ S' ⊆ S | ∀ s ∈ S', s ⊨ tt}

    :param m: The LTS model M
    :param s: (conditional) The subset S' ⊆ S'
    :param output_type: (conditional) StateSet or IV with a default of StateSet
    :return: The satisfaction set
    """

    # Get the size of the incidence vector
    size = m.s.get_dimension_1()

    # Prepare an incidence vector with all ones
    sat_iv = state.IV(size=size, value=1)

    if s is not None:
        # Convert the flexible s parameter to an incidence vector
        s_iv = m.s.get_iv(s)
        # Limit the result to the requested set
        sat_iv = binary_vector.get_minima(sat_iv, s_iv)

    return sat_iv


class TT(ZeroaryStateFormula):
    """The tt symbol"""

    def compute(self, m: LTS, s: state.StateInput = None, output_type: type = None) -> state.StateOutput:
        return tt(m, s)

    def to_latex_math(self):
        return f'\\mathrm{{tt}}'

    def to_unicode(self):
        return f'tt'

    def to_multistring(self):
        return mstr.MStr(self.to_unicode(), self.to_latex_math())


def a(self, m: LTS, s: state.StateInput = None) -> state.StateOutput:
    """Get the satisfaction set of the a state formula

    Apply the state formula a to the LTS model,
    or conditionally to a single state or a subset of states,
    and return the incidence vector of the resulting satisfaction set.

    The returned incidence vector is always relative to the complete set of model states.

    Formally:
    Let M be an LTS model with states S.
    Let S' be a subset of S.
    Let tt be the tautological truth state formula.
    Let Sat(tt) be the satisfaction set of tt in S'.

    In short:
    {s ∈ S' ⊆ S | ∀ s ∈ S', s ⊨ tt}

    Output type:
    This function returns an incidence vector if the s input parameter is index-based,
    and a StateSet otherwise:
    CATEGORY:       INPUT TYPE:     OUTPUT TYPE:
    index-based     int             IV
    index-based     IV              IV
    key-based       str             StateSet
    key-based       State           StateSet
    key-based       StateSet        StateSet

    :param m: The LTS model M
    :param s: (conditional) The subset S' ⊆ S'
    :return: The satisfaction set
    """


class A(UnaryStateFormula):
    """s ⊨ a : iif a ∈ L(s)"""

    def __init__(self, a: atom.Atom):
        self.a = atom.Atom(a)

    def compute(self, m: LTS) -> state.StateOutput:
        """Get the incidence vector of the satisfaction set

        Apply the state formula to the LTS model,
        or conditionally to a single state or a subset of states,
        and return the incidence vector of the resulting satisfaction set.

        The returned incidence vector is always relative to the complete set of model states.

        Formally:
        Let M be an LTS model with states S.
        Let S' be a subset of S.
        Let 𝛷 be the state formula.
        Let Sat(𝛷) be the satisfaction set of 𝛷 limited to S'.
        Let IV(Sat(𝛷)) be the incidence vector of Sat(𝛷) relative to S.

        :param m: The LTS model M
        :param s: (conditional) The subset of states S'
        :return: The incidence vector IV(Sat(𝛷))
        """
        # Get the state incidence vector for that atom
        sat_iv = m.get_s_iv_from_a(self.a)
        return sat_iv

    def compute(self, m: LTS) -> state.StateSet:
        """Get the satisfaction set

        Apply the state formula to the LTS model,
        or conditionally to a single state or a subset of states,
        and return the satisfaction set.

        Formally:
        Let M be an LTS model with states S.
        Let S' be a subset of S.
        Let 𝛷 be the state formula.
        Let Sat(𝛷) be the satisfaction set of 𝛷 limited to S'.

        :param m: The LTS model M
        :param s: (conditional) The subset of states S'
        :return: The satisfaction set Sat(𝛷)
        """
        # Get the incidence vector of that atom
        sat_iv = self.compute(m)
        # Convert the incidence vector to a set
        sat_set = m.s.get_set(sat_iv)
        return sat_set

    def to_latex_math(self):
        return f'\\text{{{self.a.latex_math}}}'

    def to_unicode(self):
        return f'{self.a.unicode}'

    def to_multistring(self):
        return mstr.MStr(self.to_unicode(), self.to_latex_math())


class Not(StateFormula):
    def __init__(self, phi: StateFormula):
        self.phi = phi

    def compute(self, m: LTS) -> state.IV:
        """Get the incidence vector of the satisfaction set

        Apply the state formula to the LTS model,
        or conditionally to a single state or a subset of states,
        and return the incidence vector of the resulting satisfaction set.

        The returned incidence vector is always relative to the complete set of model states.

        Formally:
        Let M be an LTS model with states S.
        Let S' be a subset of S.
        Let 𝛷 be the state formula.
        Let Sat(𝛷) be the satisfaction set of 𝛷 limited to S'.
        Let IV(Sat(𝛷)) be the incidence vector of Sat(𝛷) relative to S.

        :param m: The LTS model M
        :param s: (conditional) The subset of states S'
        :return: The incidence vector IV(Sat(𝛷))
        """
        # Get the satisfaction incidence vector of phi.
        phi_sat_iv = self.phi.compute(m)
        # Compute the complement of that incidence vector.
        # The complement or difference set operation,
        # is equivalent to the inverse operation on an incidence vector of a set:
        # {e ∈ {0,1}|e = 0 if Se ∈ S, 1 otherwise} ≡ S∁
        sat_iv = phi_sat_iv.get_inverse()
        return sat_iv

    def compute(self, m: LTS) -> state.StateSet:
        """Get the satisfaction set

        Apply the state formula to the LTS model,
        or conditionally to a single state or a subset of states,
        and return the satisfaction set.

        Formally:
        Let M be an LTS model with states S.
        Let S' be a subset of S.
        Let 𝛷 be the state formula.
        Let Sat(𝛷) be the satisfaction set of 𝛷 limited to S'.

        :param m: The LTS model M
        :param s: (conditional) The subset of states S'
        :return: The satisfaction set Sat(𝛷)
        """
        # Get the incidence vector of that atom
        sat_iv = self.compute(m)
        # Convert the incidence vector to a set
        sat_set = m.s.get_set(sat_iv)
        return sat_set

    def to_latex_math(self):
        return f'\\lnot \\left( {self.phi.to_latex_math()} \\right)'

    def to_unicode(self):
        return f'¬({self.phi.to_unicode()})'

    def to_multistring(self):
        return mstr.MStr(self.to_unicode(), self.to_latex_math())


class Or(StateFormula):
    def __init__(self, phi: StateFormula, psi: StateFormula):
        self.phi = phi
        self.psi = psi

    def compute(self, m: LTS) -> state.IV:
        """Get the incidence vector of the satisfaction set

        Apply the state formula to the LTS model,
        or conditionally to a single state or a subset of states,
        and return the incidence vector of the resulting satisfaction set.

        The returned incidence vector is always relative to the complete set of model states.

        Formally:
        Let M be an LTS model with states S.
        Let S' be a subset of S.
        Let 𝛷 be the state formula.
        Let Sat(𝛷) be the satisfaction set of 𝛷 limited to S'.
        Let IV(Sat(𝛷)) be the incidence vector of Sat(𝛷) relative to S.

        :param m: The LTS model M
        :param s: (conditional) The subset of states S'
        :return: The incidence vector IV(Sat(𝛷))
        """
        # Get the satisfaction incidence vectors of phi and psi.
        phi_sat_iv = self.phi.compute(m)
        psi_sat_iv = self.psi.compute(m)
        # Compute the union of the sets represented by these incidence vectors.
        # For an incidence vector of a set,
        # the max operation is equivalent to set union operation:
        # max(IV(s), IV(t)) ≡ s ∪ t
        sat_iv = phi_sat_iv.get_maximum(psi_sat_iv)
        return sat_iv

    def compute(self, m: LTS) -> state.StateSet:
        """Get the satisfaction set

        Apply the state formula to the LTS model,
        or conditionally to a single state or a subset of states,
        and return the satisfaction set.

        Formally:
        Let M be an LTS model with states S.
        Let S' be a subset of S.
        Let 𝛷 be the state formula.
        Let Sat(𝛷) be the satisfaction set of 𝛷 limited to S'.

        :param m: The LTS model M
        :param s: (conditional) The subset of states S'
        :return: The satisfaction set Sat(𝛷)
        """
        # Get the incidence vector of that atom
        sat_iv = self.compute(m)
        # Convert the incidence vector to a set
        sat_set = m.s.get_set(sat_iv)
        return sat_set

    def to_latex_math(self):
        return f'\\left( {self.phi.to_latex_math()} \\right) \\lor \\left( {self.psi.to_latex_math()} \\right)'

    def to_unicode(self):
        return f'({self.phi.to_unicode()}) ∨ ({self.psi.to_unicode()})'

    def to_multistring(self):
        return mstr.MStr(self.to_unicode(), self.to_latex_math())


class And(StateFormula):
    def __init__(self, phi: StateFormula, psi: StateFormula):
        self.phi = phi
        self.psi = psi

    def compute(self, m: LTS) -> state.IV:
        """Get the incidence vector of the satisfaction set

        Apply the state formula to the LTS model,
        or conditionally to a single state or a subset of states,
        and return the incidence vector of the resulting satisfaction set.

        The returned incidence vector is always relative to the complete set of model states.

        Formally:
        Let M be an LTS model with states S.
        Let S' be a subset of S.
        Let 𝛷 be the state formula.
        Let Sat(𝛷) be the satisfaction set of 𝛷 limited to S'.
        Let IV(Sat(𝛷)) be the incidence vector of Sat(𝛷) relative to S.

        :param m: The LTS model M
        :param s: (conditional) The subset of states S'
        :return: The incidence vector IV(Sat(𝛷))
        """
        # Get the satisfaction incidence vectors of phi and psi
        phi_sat_iv = self.phi.compute(m)
        psi_sat_iv = self.psi.compute(m)
        # Compute the intersection of the sets represented by these incidence vectors.
        # For an incidence vector of a set,
        # the min operation is equivalent to set union operation:
        # min(IV(s), IV(t)) ≡ s ∩ t
        sat_iv = binary_vector.get_minima(phi_sat_iv, psi_sat_iv)
        return sat_iv

    def compute(self, m: LTS) -> state.StateSet:
        """Get the satisfaction set

        Apply the state formula to the LTS model,
        or conditionally to a single state or a subset of states,
        and return the satisfaction set.

        Formally:
        Let M be an LTS model with states S.
        Let S' be a subset of S.
        Let 𝛷 be the state formula.
        Let Sat(𝛷) be the satisfaction set of 𝛷 limited to S'.

        :param m: The LTS model M
        :param s: (conditional) The subset of states S'
        :return: The satisfaction set Sat(𝛷)
        """
        # Get the incidence vector of that atom
        sat_iv = self.compute(m)
        # Convert the incidence vector to a set
        sat_set = m.s.get_set(sat_iv)
        return sat_set

    def to_latex_math(self):
        return f'\\left( {self.phi.to_latex_math()} \\right) \\land \\left( {self.psi.to_latex_math()} \\right)'

    def to_unicode(self):
        return f'({self.phi.to_unicode()}) ∧ ({self.psi.to_unicode()})'

    def to_multistring(self):
        return mstr.MStr(self.to_unicode(), self.to_latex_math())


class EventuallyPhi(StateFormula):
    def __init__(self):
        pass


class AlwaysPhi(StateFormula):
    def __init__(self):
        pass


class PathFormula:
    def __init__(self):
        pass


class NextPhi(PathFormula):
    def __init__(self):
        pass


class UntilPhi(PathFormula):
    def __init__(self):
        pass


class Sat:
    def __init__(
            self,
            m: LTS,
            s: state.StateInput,
            phi: StateFormula):
        self.m = m
        self.s_iv = m.s.get_iv(s)
        self.phi = phi

    def __repr__(self):
        return self.to_multistring()

    def __str__(self):
        return self.to_multistring()

    def check_s(self):
        """Check if

        :return:
        """
        # Retrieve the sat iv
        sat_iv = self.get_iv()
        # Check that all evaluated states are in the satisfaction set
        result = sat_iv.check_masking(self.s_iv)
        return result

    def get_iv(self) -> state.IV:
        """Get the incidence vector of the satisfaction set

        Apply the state formula to the LTS model,
        or conditionally to a single state or a subset of states,
        and return the incidence vector of the resulting satisfaction set.

        The returned incidence vector is always relative to the complete set of model states.

        Formally:
        Let M be an LTS model with states S.
        Let S' be a subset of S.
        Let 𝛷 be the state formula.
        Let Sat(𝛷) be the satisfaction set of 𝛷 limited to S'.
        Let IV(Sat(𝛷)) be the incidence vector of Sat(𝛷) relative to S.

        :param m: The LTS model M
        :param s: (conditional) The subset of states S'
        :return: The incidence vector IV(Sat(𝛷))
        """
        if isinstance(self.phi, StateFormula):
            return self.phi.compute(self.m)
        else:
            raise TypeError('Unsupported type')

    def get_set(self) -> state.StateSet:
        """Get the satisfaction set

        Apply the state formula to the LTS model,
        or conditionally to a single state or a subset of states,
        and return the satisfaction set.

        Formally:
        Let M be an LTS model with states S.
        Let S' be a subset of S.
        Let 𝛷 be the state formula.
        Let Sat(𝛷) be the satisfaction set of 𝛷 limited to S'.

        :param m: The LTS model M
        :param s: (conditional) The subset of states S'
        :return: The satisfaction set Sat(𝛷)
        """
        sat_iv = self.get_iv()
        sat_set = self.m.s.get_set(sat_iv)
        output.output2(const.RESULT,
                       self.to_multistring() +
                       mstr.MStr(f' = {sat_set.to_unicode()}', f' = {sat_set.to_latex_math()}'))
        return sat_set

    def to_latex_math(self):
        return f'\\text{Sat} \\left( {self.phi.to_latex_math()} \\right)'

    def to_unicode(self):
        return f'Sat({self.phi.to_unicode()})'

    def to_multistring(self):
        return mstr.MStr(self.to_unicode(), self.to_latex_math())
