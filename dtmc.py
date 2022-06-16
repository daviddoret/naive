import dataclasses
import numpy as np
import sympy as sym

import atom
import output
import state
import stochastic_matrix
import utils
import fractions
import warnings
import itertools


def dtmc_i_until_bounded_transient_analysis(s, m, o, p, i_phi, k, i_psi):
    """ Return the indicator vector of Sat(P{o}{p}(Φ U≤{k} Ψ))

    Parameters
    ------------
        s: vector (type=string)
            The state labels
        m: numpy.matrix
            The DTMC
        o: string
            The probability operator
        p: float
            The probability threshold
        i_phi: numpy.matrix (dtype=int)
            An indicator vector of states satisfying Φ
        k: int
            The number of steps (0 <= k <= n)
        i_psi: numpy.matrix (dtype=int)
            An indicator vector of states satisfying Ψ
    Return
    -----------
        iSat: numpy.array (dtype=int)
            An indicator vector of Sat(P{op}{p}(Φ U≤{k} Ψ))
    """

    output.output_math(f'S \; \colon= \; {output.tex(s)}')
    output.output_math(f'M \; \colon= \; {output.tex(m)}')

    # Compute M'
    M_prime = np.copy(m)
    for s_index in range(0, len(s)):
        absorbing_vector = np.zeros(len(s))
        absorbing_vector[s_index] = 1
        if i_psi[s_index]:
            # Making all the Ψ-states absorbing, i.e., removing all outgoing transitions and adding a self loop with probability 1.
            M_prime[s_index] = absorbing_vector
            output.output_markdown(f'Make ${s[s_index]}$ absorbing because ${s[s_index]} \\models \\Psi$')
        if not (i_phi[s_index] or i_psi[s_index]):
            # Making all the states that are not Φ-states or Ψ-states, ¬ (Φ ∨ Ψ)-states absorbing.
            M_prime[s_index] = absorbing_vector
            print(f'Make {s[s_index]} absorbing because {s[s_index]} ⊨ ¬(Φ ∨ Ψ)')
            print('')
    output.output_math(f'M'' \\; \\colon= \\; {output.tex(M_prime)}')

    # Raise the reduced DTMC to the power k
    P_k = np.linalg.matrix_power(M_prime, k)
    print(f'P^k:')
    print(P_k)
    print(f'')

    Q = np.zeros((len(s), len(s)))
    # Compute v1 v2 . . . vn−1 vn ·Pk (where k is the until bound) n times and alter the vector v in the following way: 1 0 . . . 0 0, 0 1 . . . 0 0, . . ., 0 0 . . . 1 0, 0 0 . . . 0 1
    for i in range(0, len(s)):
        V = np.zeros((len(s)))
        V[i] = 1
        # print(f'{i}, {V}')
        Q_vector = np.matmul(V, P_k)
        # print(Q)
        Q[i] = Q_vector
    print(f'Q:')
    print(Q)
    print(f'')

    iSat = np.zeros(len(s), dtype=int)

    # For all i with si ∈ Sat (Ψ):
    for i in range(0, len(s)):
        if (i_psi[i]):
            for j in range(0, len(s)):
                # if qji matches the probability bound p then sj ∈ Sat PEp ΦU ≤kΨ :
                qji = Q[j, i]
                qji_fraction = fractions.Fraction(Q[j, i]).limit_denominator(100)
                if o == '<=' and qji <= p:
                    print(f'q{j + 1},{i + 1} = {qji_fraction}, {qji:.3f} ≤ {p}, Sat')
                    iSat[j] = 1
                elif o == '<' and qji < p:
                    print(f'q{j + 1},{i + 1} = {qji_fraction}, {qji:.3f} < {p}, Sat')
                    iSat[j] = 1
                elif o == '>=' and qji >= p:
                    print(f'q{j + 1},{i + 1} = {qji_fraction}, {qji:.3f} ≥ {p}, Sat')
                    iSat[j] = 1
                elif o == '>' and qji > p:
                    print(f'q{j + 1},{i + 1} = {qji_fraction}, {qji:.3f} > {p}, Sat')
                    iSat[j] = 1
                else:
                    print(f'q{j + 1},{i + 1} = {qji_fraction}, {qji:.3f}')

    print(f'')
    output.output_math(
        rf"""\text{{iSat}} \Bigg( \; \mathcal{{P}}_{{{o}{p}}} \Big( \; \Phi \; \mathcal{{U}}_{{\leq{k}}} \; \Psi \Big) \; \Bigg) \; = \; {iSat}""")

    return iSat


@dataclasses.dataclass
class DTMC:
    """DTMC (Discrete-Time Markov Chain)

    Args:
        s (np.array): S is a finite set of states
        p (np.matrix): P : S × S → [0, 1] a stochastic matrix with ∑_{s' ∈ S} P(s, s') = 1, for all s ∈ S
        ap (np.array): The set of atomic properties
        L (Callable): S → 2^{AP}, is a labeling function that assigns a set L(s) ∈ s^{AP} to any state
    """
    s: state.StateSet
    p: stochastic_matrix.StochasticMatrix
    ap: atom.AtomSet

    def __init__(self, s, p, ap):
        if not isinstance(s, state.StateSet):
            s = state.StateSet(s)
        if not isinstance(p, stochastic_matrix.StochasticMatrix):
            p = stochastic_matrix.StochasticMatrix(p)
        if not isinstance(ap, atom.AtomSet):
            ap = atom.AtomSet(ap)
        self.s = s
        self.p = p
        self.ap = ap
        self.check_consistency()

    def check_consistency(self) -> bool:
        if not self.s.check_consistency():
            warnings.warn('not self.s.check_consistency()')
            return False
        if not self.p.check_consistency():
            warnings.warn('not self.p.check_consistency()')
            return False
        if not self.ap.check_consistency():
            warnings.warn('not self.ap.check_consistency()')
            return False
        return True

    def get_steadystate_probability_distribution(self):
        """ Return the steady-state distribution of a DTMC if it exists.

        Return
        -----------
            iSat: numpy.array (dtype=float)
                A numeric vector corresponding to the stead-state probability distribution of M
        """

        # TODO: Check that the DTMC is aperiodic, irreducible, etc. i.e. it has a steady-state distrib

        if not self.check_consistency():
            raise ValueError('not self.check_consistency()')

        i = utils.get_identity_matrix(size=self.p.get_dimension_1_length())
        v = np.subtract(self.p.to_float_numpy_array(), i)
        output.output(f'v \\; \\colon= \\; {output.tex(v)}')

        # Solve the linear system
        output.output(f'\\text{{Linear system:}}')
        linear_system = []
        for column_index in range(0, self.s.get_dimension_1()):
            linear_equation = 0
            for s_index in range(0, self.s.get_dimension_1()):
                linear_equation = sym.Add(linear_equation, v[s_index, column_index] * sym.Symbol(f's_{s_index + 1}'))
            output.output(f'{sym.latex(linear_equation)} = 0')
            linear_system.append(sym.Eq(0, linear_equation))
        linear_equation = 0
        for s_index in range(0, self.s.get_dimension_1()):
            linear_equation = sym.Add(linear_equation, sym.Symbol(f's_{s_index + 1}'))
        linear_system.append(sym.Eq(1, sym.Add(linear_equation)))
        ltx = sym.latex(linear_equation)
        output.output(f'{ltx} = 1')
        output.output(f'\\text{{Solution:}}')
        solution = sym.solve(linear_system, set=True)
        probability_distribution = np.array(list(itertools.chain(*solution[1])))
        output.output(f'\\text{{distribution}} \\; = \\; {output.tex(probability_distribution)}')
        return probability_distribution

    def to_latex_math(self):
        return f'\\left( S\\colon={self.s.to_latex_math_v()}, P\\colon={output.tex(self.p)}, \\mathrm{{AP}}\\colon={self.ap.to_latex_math_v()}, L \\right)'

    def to_unicode(self):
        return f'( S:={self.s.to_unicode()}, P:={self.p.to_unicode()}, AP:={self.ap.to_unicode()}, L \\right)'

    def to_output_format(self):
        if output.OUTPUT_MODE == output.OUTPUT_LATEX_MATH:
            return self.to_latex_math()
        elif output.OUTPUT_MODE == output.OUTPUT_UNICODE:
            return self.to_unicode()
        else:
            raise NotImplementedError('Unknown output mode')

    def output(self):
        output.output(self.to_output_format())


def exercise_1():
    S = ['s1', 's2', 's3', 's4']
    M = np.matrix([[0.0, 2.0 / 3.0, 1.0 / 3.0, 0.0],
                   [1.0 / 2.0, 0.0, 1.0 / 4.0, 1.0 / 4.0],
                   [0.0, 0.0, 1.0, 0.0],
                   [0.0, 0.0, 0.0, 1.0]])

    iΦ = np.array([1, 1, 0, 0])
    iΨ = np.array([0, 0, 1, 1])
    k = 3
    p = 0.4
    o = '>='

    dtmc_i_until_bounded_transient_analysis(S, M, o, p, iΦ, k, iΨ)


exercise_1()


def exercise_3():
    S = ['s1', 's2', 's3', 's4']
    M = np.matrix([[1.0 / 2.0, 0.0, 1.0 / 2.0, 0.0],
                   [8.0 / 10.0, 1.0 / 10.0, 0.0, 1.0 / 10.0],
                   [0.0, 1.0 / 4.0, 3.0 / 4.0, 0.0],
                   [0.0, 1.0, 0.0, 0.0]])

    iΦ = np.array([0.0, 1.0, 0.0, 0.0])
    iΨ = np.array([1.0, 0.0, 0.0, 0.0])
    k = 3
    p = 0.9
    o = '<'

    dtmc_i_until_bounded_transient_analysis(S, M, o, p, iΦ, k, iΨ)


exercise_3()









def DTMC_I_Until_Unbounded(S, P, o, p, IΦ, IΨ):
    """ Return the indicator vector of Sat(P{o}{p}(Φ U≤∞ Ψ))

    Parameters
    ------------
        S: vector (type=string)
            The state labels
        P: numpy.matrix
            The probability matrix of the DTMC
        o: string
            The probability operator (<, <=, >, >=)
        p: float
            The probability threshold
        IΦ: numpy.matrix (dtype=int)
            An indicator vector of states satisfying Φ
        IΨ: numpy.matrix (dtype=int)
            An indicator vector of states satisfying Ψ
    Return
    -----------
        iSat: numpy.array (dtype=int)
            An indicator vector of Sat(P{op}{p}(Φ U≤∞ Ψ))
    """

    output.output(f'## Unbounded Until')

    #DTMC_Validate_Stochastic_Matrix_Consistency(P)

    output.output(f'S \; \colon= \; {output.tex(S)}')
    output.output(f'P \; \colon= \; {output.tex(P)}')
    output.output(f'I(\Phi) \; \colon= \; {output.tex(IΦ)}')
    output.output(f'I(\Psi) \; \colon= \; {output.tex(IΨ)}')

    def get_probability_0():
        IR = np.copy(IΨ)
        IX = np.copy(IΦ)
        done = False
        while not done:
            # Build the set { s \\in \\Phi | \\exists s' \\in R.P(s,s') > 0 }
            IR_prime = np.copy(IR)
            for s_index in range(0, len(S)):
                if IX[s_index]:  # s in Φ
                    for s_prime_index in range(0, len(S)):
                        if IR_prime[s_prime_index] and P[s_index, s_prime_index] > 0:
                            IR_prime[s_index] = 1  # Add this state
                            # output.output_math(f'{S[s_index]} \\models \\Phi \\land \\exists s\\prime \\in R.P(s,s\\prime) > 0')
                            break  # We only need to prove existence
            if np.array_equal(IR, IR_prime):
                done = True
            IR = np.copy(IR_prime)
        IR = utils.I_set_complement(IR)
        return IR

    def get_probability_1():
        IR = np.copy(IS_no)
        IX = utils.I_set_difference(IΦ, IΨ)
        done = False
        while (not done):
            IR_prime = np.copy(IR)
            for s_index in range(0, len(S)):
                if IX[s_index]:  # s not in Φ \ Ψ
                    for s_prime_index in range(0, len(S)):
                        if IR_prime[s_prime_index] and P[s_index, s_prime_index] > 0:
                            IR_prime[s_index] = 1  # Add this state
                            # output.output_math(f'{S[s_index]} \\models \\Phi \\land \\exists s\\prime \\in R.P(s,s\\prime) > 0')
                            break  # We only need to prove existence
            if np.array_equal(IR, IR_prime):
                done = True
            IR = np.copy(IR_prime)
        IR = utils.I_set_complement(IR)
        return IR

    IS_no = get_probability_0()
    output.output(f'I(S^{{\\mathrm{{no}}}}) \; \colon= \; {output.tex(IS_no)}')

    IS_yes = get_probability_1()
    output.output(f'I(S^{{\\mathrm{{yes}}}}) \; \colon= \; {output.tex(IS_yes)}')

    # Solve the linear system
    output.output_math(f'\\text{{Linear system:}}')
    linear_system = []
    for s_index in range(0, len(S)):
        if IS_no[s_index]:
            linear_equation = sym.Eq(sym.Symbol(S[s_index]), 0)
            output.output_math(f'{S[s_index]} = 0')
            linear_system.append(linear_equation)
        elif IS_yes[s_index]:
            linear_equation = sym.Eq(sym.Symbol(S[s_index]), 1)
            output.output_math(f'{S[s_index]} = 1')
            linear_system.append(linear_equation)
        else:
            # given s, ∑(s' in S) of P(s,s')⋅Prob(s', φ1 U φ2)
            sum_of_p_times_probs = 0
            for s_prime_index in range(0, len(S)):
                sum_of_p_times_probs = sym.Add(sum_of_p_times_probs,
                                               P[s_index, s_prime_index] * sym.Symbol(S[s_prime_index]))
            linear_equation = sym.Eq(sym.Symbol(S[s_index]), sum_of_p_times_probs)
            output.output(f'{S[s_index]} = {sym.latex(sum_of_p_times_probs)}')
            linear_system.append(linear_equation)
    output.output(f'\\text{{Solution:}}')
    solution = sym.solve(linear_system, set=True)
    distrib = np.array(list(it.chain(*solution[1])))
    output.output(f'\\text{{distribution}} \\; = \\; {output.tex(distrib)}')

    # Final step, list the states that are within probability operator
    ISat = np.zeros(len(S), dtype=int)
    for s_index in range(0, len(S)):
        if ((o == '>' and distrib[s_index] > p) or
                (o == '>=' and distrib[s_index] >= p) or
                (o == '<' and distrib[s_index] < p) or
                (o == '<=' and distrib[s_index] <= p)):
            ISat[s_index] = 1

    output.output(
        f'I \\Bigg( \\mathrm{{Sat}} \\bigg( \\; \\mathcal{{P}}_{{{o}{p}}} \\Big( \\; \\Phi \\; \\mathcal{{U}}_{{\\leq\\infty}} \\; \\Psi \\Big) \\; \\bigg) \\; \\Bigg) \\; = \\; {ISat}')
    return ISat


def exercise_DTMC_I_Until_Unbounded_1():
    S = ['s0', 's1', 's2', 's3', 's4', 's5']

    P = np.matrix(
        [
            [0.0, 0.1, 0.9, 0.0, 0.0, 0.0],
            [0.4, 0.0, 0.6, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.1, 0.1, 0.5, 0.3],
            [0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.7, 0.3]
        ], dtype=float)

    Ia = np.array([0, 1, 0, 1, 0, 0], dtype=int)
    Ib = np.array([0, 0, 0, 0, 1, 1], dtype=int)
    IΦ = utils.I_set_complement(Ia)
    IΨ = np.copy(Ib)
    o = '>'
    p = 0.8

    DTMC_I_Until_Unbounded(S, P, o, p, IΦ, IΨ)


#exercise_DTMC_I_Until_Unbounded_1()


def exercise_DTMC_I_Until_Unbounded_2():
    S = ['S1', 'S2', 'S3', 'S4']

    P = np.matrix(
        [
            [0.5, 0.0, 0.5, 0.0],
            [0.8, 0.1, 0.0, 0.1],
            [0.0, 0.25, 0.75, 0.0],
            [0.0, 1.0, 0.0, 0.0]
        ], dtype=float)

    Ired = np.array([1, 0, 0, 0], dtype=int)
    Iyellow = np.array([0, 1, 0, 0], dtype=int)
    Igreen = np.array([0, 0, 1, 0], dtype=int)
    Iblack = np.array([0, 0, 0, 1], dtype=int)
    IΦ = np.copy(Iyellow)
    IΨ = np.copy(Ired)
    o = '<'
    p = 0.9

    DTMC_I_Until_Unbounded(S, P, o, p, IΦ, IΨ)


#exercise_DTMC_I_Until_Unbounded_2()
