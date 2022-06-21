import dataclasses
import numpy as np
import sympy as sym
import output
import utils
import math
import dtmc


@dataclasses.dataclass
class CTMC:
    """CTMC (Continuous-Time Markov Chain)

    Args:
        S (np.array): S is a finite set of states
        R (np.matrix): A transition rate matrix (warning: these are not probabilities)
        AP (np.array): The set of atomic properties
        L (Callable): S → 2^{AP}, is a labeling function that assigns a set L(s) ∈ s^{AP} to any state

    """

    S: np.array
    R: np.matrix
    AP: np.array
    L: object


def ctmc_latexify(m):
    return f"""\\left( S\\colon={output.tex(utils.numpy_vector_verticalize(m.s))}, R\\colon={output.tex(m.R)}, \\mathrm{{AP}}\\colon={output.tex(utils.numpy_vector_verticalize(m.sat_a))}, L \\right)"""


def ctmc_output_latex_math(m):
    output.output_math(ctmc_latexify(m))


def test_ctmc_01():
    S = np.array(['S1', 'S2', 'S3'])
    R = np.array([[14.0, 7.5, 0.5], [0.9, 0.1, 0.0], [0.0, 0.1, 0.9]])
    AP = np.array(['Red', 'Green', 'Blue'])

    def L(s_index):
        if s_index == 0:
            return np.array(['Blue', 'Green'])
        elif s_index == 1:
            return np.array(['Orange'])
        elif s_index == 2:
            return np.array(['Blue', 'Orange'])

    M = CTMC(S, R, AP, L)
    ctmc_output_latex_math(M)


test_ctmc_01()


def CTMC_Get_Q(M):
    """ Derive the infinitesimal generator Q from the transition matrix P

    Parameters
    ------------
        M: CTMC
            The Continuous-Time Markoc Chain model
    Return
    ------------
        Q: numpy.matrix (float dtype)
            The infinitesimal generator (aka transition rate matrix)
    """

    # output_function_title()

    Q = np.copy(M.R)
    row_sums = Q.sum(axis=1)
    # print(row_sums)
    diag = np.eye(len(M.S))
    # print(diag)
    diag2 = np.multiply(row_sums, diag)
    # print(diag2)
    Q = np.subtract(Q, diag2)
    output.output_math(f'Q = {output.tex(Q)}')
    return Q


def test_CTMC_Get_Q():
    S = np.array(['idle 0', 'busy 1', 'sleep 2'])
    R = np.matrix([[0, 4, 1], [10, 0, 0], [0, 4, 0]])
    AP = None
    L = None

    M = CTMC(S, R, AP, L)
    CTMC_Get_Q(M)

    S = np.array(['0', '1', '2', '3'])
    R = np.matrix([
        [0, 2, 2, 0],
        [2, 0, 0, 0],
        [2, 2, 0, 2],
        [0, 2, 0, 0]])
    AP = None
    L = None

    M = CTMC(S, R, AP, L)
    CTMC_Get_Q(M)


test_CTMC_Get_Q()


def CTMC_Get_E(M):
    """Get E(S)

    Based on the transition rate matrix it is possible to express a number
    of other means to describe the behavior of the CTMC.
    The total rate at which any transition outgoing from state s is taken,
    is denoted:
    E(s) = ∑_{s ∈ S, s≠s'} R(s,s').
    But with this function we compute it for all s ∈ S.

    Parameters
    ------------
        M: CTMC
            The CTMC model.

    Return
    ------------
        ES: numpy.matrix (float dtype)
            A vector of total rates
    """

    # output_function_title()

    ES1 = np.copy(M.R)

    # Remove all transition rates R(s,s') where s = s'
    Id_inverse = utils.inverse_binary_array(np.eye(len(M.S)))
    ES2 = np.multiply(ES1, Id_inverse)
    ES3 = ES2.sum(axis=1)
    output.output_math(
        f'E \\left( {output.tex(utils.numpy_vector_verticalize(M.S))} \\right) = \\sum_{{s \\in S, s \\neq s^{{\\prime}} }} R(s, s^{{\\prime}}) = \\sum_{{s \\in S}} \\left( {output.tex(ES1)} \\cdot {output.tex(Id_inverse)} \\right) = {output.tex(utils.numpy_vector_verticalize(ES3))}')
    return ES3


def test_CTMC_Get_E():
    M = CTMC(
        S=np.array(['s1', 's2', 's3']),
        R=np.matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
        AP=np.array(['green', 'red', 'blue']),
        L=None)
    CTMC_Get_E(M=M)


test_CTMC_Get_E()


def ctmc_get_uniformization_lambda(m):
    """ Compute the Poisson process uniformization factor λ for uniformization.

    Parameters
    ------------
        m: CTMC
            The Continuous-Time Markoc Chain model

    """
    # output_function_title()
    e = CTMC_Get_E(m)
    l = max(e)
    output.output_math(f'λ = \\max{{E(S)}} = \\max{{{output.tex(e)}}} = {l}')
    return l


def cmtc_get_uniformization_p(M):
    """ Derive the one-step transition matrix P for uniformization

    This is the first step when using the uniformization method:
    P = I + (Q / λ)
    Q = λ(P − I)

    Parameters
    ------------
        M: CTMC
            The Continuous-Time Markoc Chain model

    Return
    ------------
        P: numpy.matrix (float dtype)
            The one-step transition matrix P for uniformization
    """

    # output_function_title()

    l = ctmc_get_uniformization_lambda(M)
    Q = CTMC_Get_Q(M)
    I = np.eye(len(M.S))
    P = np.add(I, np.divide(Q, l))
    output.output_math(f'P_{{\\text{{uniform}}}} = {output.tex(I)} + \\frac{{{output.tex(Q)}}}{{{l}}} = {output.tex(P)}')
    return P


def Test_CTMC_Get_Uniformization_P():
    M = CTMC(
        S=np.array(['S0', 'S1']),
        R=np.matrix([[0, 3], [2, 0]]),
        AP=None,
        L=None)

    cmtc_get_uniformization_p(M)


Test_CTMC_Get_Uniformization_P()


def ctmc_get_uniformization_psi(λ, t, n):
    """
    ψ(λt; n) = e^{−λ * t} * ((λt)^n) / n!    , with n ∈ ℕ
    """
    # output_function_title()
    poisson_proba = math.exp(-λ * t) * math.pow(λ * t, n) / math.factorial(n)
    # output.output_math(f'ψ\\left(\\lambda\\cdot t, n\\right) = \\mathrm{{e}}^{{-\\lambda\\cdot t}} \\cdot \\frac{{\\left(\\lambda\\cdot t\\right)^n}}{{n!}} = ψ\\left({λ}\\cdot{t}, {n}\\right) = \\mathrm{{e}}^{{-{λ}\\cdot{t}}} \\cdot \\frac{{\\left({λ}\\cdot{t}\\right)^{n}}}{{{n}!}} = {poisson_proba}')
    return poisson_proba


def test_ctmc_get_uniformization_psi():
    ctmc_get_uniformization_psi(λ=2, t=1, n=3)


test_ctmc_get_uniformization_psi()


def ctmc_get_uniformization_ke(l, t, e):
    """
    Compute 1 - ∑_{n=0}^{kε} ψ(λt; n) until ≤ ε
    Then stop and return kε
    """
    # output_function_title()
    running_sum = 0
    loop = True
    n = 0
    output.output_math(f'\\epsilon \\colon= {e}')
    while loop:
        running_sum = running_sum + ctmc_get_uniformization_psi(l, t, n)
        if 1 - running_sum <= e:
            output.output_math(f'1 - \\sum_{{n=0}}^{{{n}}} ψ({l},{t},{n}) = {1 - running_sum}')
            output.output_math(f'{1 - running_sum} \\leq {e}')
            loop = False
        else:
            n = n + 1
    output.output_math(f'k_{{\\epsilon}} = {n}')
    return n


def test_ctmc_get_uniformization_ke():
    ctmc_get_uniformization_ke(l=2, t=1, e=10 ** -4)


test_ctmc_get_uniformization_ke()


def ctmc_get_uniformization_transient_proba(m, pi0, t, e):
    """ Derive the transient probability distribution of M at t=1 using uniformization

    V(1) = π(0) ∑_{n=0}^{∞} ( ψ(λ⋅t; n) ⋅ P^n )

    Parameters
    ------------
        m: CTMC
            The Continuous-Time Markoc Chain model
        pi0: Numpy.Array (dtype=float)
            The initial distribution
        t: float
            The time
        e: float
            The desired precision, e.g. 10^-4

    Return
    ------------
        P: numpy.matrix (float dtype)
            The transient probability for t=1 using the uniformization method
    """

    # output_function_title()
    ctmc_output_latex_math(m)
    output.output_math(f'Π0 \\colon= {output.tex(pi0)}')
    output.output_math(f't \\colon= {t}')
    output.output_math(f'ε \\colon= {e}')

    P = cmtc_get_uniformization_p(m)
    output.output_math(f'P = {output.tex(P)}')

    Q = CTMC_Get_Q(m)  # Just for information

    l = ctmc_get_uniformization_lambda(m)
    output.output_math(f'λ = {l}')
    ke = ctmc_get_uniformization_ke(l, t, e)
    output.output_math(f'kε = {ke}')

    running_sum = 0
    for n in range(0, ke + 1):
        psi = ctmc_get_uniformization_psi(l, t, n)
        Pn = np.linalg.matrix_power(P, n)
        term = np.matmul(np.multiply(psi, pi0), Pn)
        running_sum = running_sum + term
    output.output_math(f'n \\colon= {n} \\; \\colon \\; {psi}⋅{output.tex(pi0)}⋅{output.tex(Pn)} = {term}')

    V1 = running_sum
    output.output_math(f'V1 = {output.tex(V1)}')
    return V1


def Test_CTMC_Get_Uniformization_Transient_Proba_1():
    output.output_function_title()

    M = CTMC(
        S=np.array(['S0', 'S1']),
        R=np.matrix([[0, 3], [2, 0]]),
        AP=None,
        L=None)
    pi0 = np.array([1, 0], dtype=float)
    t = 1
    e = 10 ** -4

    ctmc_get_uniformization_transient_proba(M, pi0, t, e)


# Test_CTMC_Get_Uniformization_Transient_Proba_1()

def Test_CTMC_Get_Uniformization_Transient_Proba_2():
    output.output_function_title()

    M = CTMC(
        S=np.array(['S0', 'S1', 'S2']),
        R=np.matrix([
            [0, 2, 2],
            [1, 0, 1],
            [6, 0, 0]]),
        AP=None,
        L=None)
    Π0 = np.array([1, 0, 0], dtype=float)
    t = 0.2
    ε = 10 ** -4

    ctmc_get_uniformization_transient_proba(M, Π0, t, ε)


Test_CTMC_Get_Uniformization_Transient_Proba_2()


def CTMC_Get_P(M, t):
    """Get the probability to leave non-absorbing state s in S in [0, t]

    P(s) = 1 - e^{-E(s) . t}

    Parameters
    ------------
        M: CTMC
            The CTMC model

    Return
    ------------
        P: numpy.matrix (float dtype)
            The probability to leave non-absorbing s in [0, t]
            :param t:
    """

    output.output_function_title()

    ES = CTMC_Get_E(M)
    PS = 1 - np.exp(- ES * t)
    output.output_math(
        f'P_M \\left( {output.tex(utils.numpy_vector_verticalize(M.s))} \\right) = 1 - \\mathrm{{e}}^{{{output.tex(utils.numpy_vector_verticalize(ES))} \\cdot {t}}} = {output.tex(utils.numpy_vector_verticalize(PS))}')

    return PS


def test_CTMC_Get_P():
    M = CTMC(
        S=np.array(['s1', 's2', 's3']),
        R=np.matrix([[13, 2, 3], [.1, .2, .01], [7, 8, 9]], dtype=float),
        AP=np.array(['green', 'red', 'blue']),
        L=None)
    p = CTMC_Get_P(M=M, t=5)
    print(p)


test_CTMC_Get_P()


def CTMC_Get_Embedded_DTMC(M):
    """Get the embedded DTMC from a CTMC

    N(s, s') = R(s, s') / E(s)

    Parameters
    ------------
        M: CTMC
            The CTMC model

    Return
    ------------
        M: DTMC
            The embedded DTMC
    """

    output.output_function_title()

    ES = CTMC_Get_E(M)
    # Extend ES to cover the full matrix
    ES = np.tile(ES, len(M.S))
    ES = np.reshape(ES, M.R.shape)
    ES = np.swapaxes(ES, 0, 1)
    # Now we can divide element-wise
    P = np.divide(M.R, ES)
    output.output_math(f'{output.tex(P)} = \\frac{{{output.tex(M.R)}}}{{{output.tex(ES)}}}')

    # copy the straight-forward properties
    S = np.copy(M.S)
    AP = np.copy(M.AP)
    L = None

    # Construct the DTMCs
    M = dtmc.DTMC(S, P, AP, L)

    return M


def Test_CTMC_Get_Embedded_DTMC_1():
    output.output_function_title()
    M = CTMC(
        S=np.array(['0', '1', '2', '3']),
        R=np.matrix([
            [0, 2, 2, 0],
            [2, 0, 0, 0],
            [2, 2, 0, 2],
            [0, 2, 0, 0]]),
        AP=None,
        L=None)
    ctmc_output_latex_math(M)

    # P must be equal to
    #   0   1/2 1/2   0,
    #   1     0   0   0,
    # 1/3   1/3   0 1/3,
    #   0    1    0   0
    M_DTMC = CTMC_Get_Embedded_DTMC(M)
    dtmc.DTMC_Output_Math(M_DTMC)


# Test_CTMC_Get_Embedded_DTMC_1()

def Test_CTMC_Get_Embedded_DTMC_2():
    output.output_function_title()
    M = CTMC(
        S=np.array(['a1', 'a2', 'a3']),
        R=np.matrix([
            [0, 2, 2],
            [1, 0, 1],
            [6, 0, 0]]),
        AP=None,
        L=None)
    ctmc_output_latex_math(M)
    CTMC_Get_Q(M)

    M_DTMC = CTMC_Get_Embedded_DTMC(M)
    dtmc.DTMC_Output_Math(M_DTMC)


Test_CTMC_Get_Embedded_DTMC_2()


def CTMC_Get_SteadyStateProbDistrib(M):
    """ Return the steady-state probability distribution of a CTMC if it exists.

    Parameters
    ------------
        M: CTMC
            The CTMC model
    Return
    -----------
        iSat: numpy.array (dtype=float)
            A numeric vector corresponding to the stead-state probability distribution of M
    """

    # TODO: Add support for reducible CTMCs

    output.output_function_title()
    ctmc_output_latex_math(M)

    # Derive the square generator matrix Q
    Q = CTMC_Get_Q(M)
    output.output_math(f'Q \\; = \\; {output.tex(Q)}')

    # Solve the linear system
    output.output_math(f'\\text{{Linear system:}}')
    linear_system = []
    for column_index in range(0, len(M.S)):
        linear_equation = 0
        for s_index in range(0, len(M.S)):
            linear_equation = sym.Add(linear_equation, Q[s_index, column_index] * sym.Symbol(f'{s_index + 1}'))
        output.output_math(f'{sym.latex(linear_equation)} = 0')
        linear_system.append(sym.Eq(0, linear_equation))
    linear_equation = 0
    for s_index in range(0, len(M.S)):
        linear_equation = sym.Add(linear_equation, sym.Symbol(f'{s_index + 1}'))
    linear_system.append(sym.Eq(1, sym.Add(linear_equation)))
    ltx = sym.latex(linear_equation)
    output.output_math(f'{ltx} = 1')
    output.output_math(f'\\text{{Solution:}}')
    solution = sym.solve(linear_system, set=True)
    distrib = np.array(list(it.chain(*solution[1])))
    output.output_math(f'\\text{{distribution}} \\; = \\; {output.tex(distrib)}')
    return distrib


def test_CTMC_Get_SteadyStateProbDistrib():
    # M = CTMC(
    #    S = ['S1','S2', 'S3'],
    #    R = np.array(
    #        [[0, 17, .1],
    #        [.7, 0, .2],
    #        [.3, .3, 0]]),
    #    AP = None,
    #    L = None)
    # solution = CTMC_Get_SteadyStateProbDistrib(M)

    # M = CTMC(
    #    S = ['s1','s2', 's3'],
    #    R = np.array(
    #        [[0, 6, 0],
    #        [3, 0, 9],
    #        [3, 3, 0]]),
    #    AP = None,
    #    L = None)
    # solution = CTMC_Get_SteadyStateProbDistrib(M)

    m = CTMC(
        S=['s0', 's2'],
        R=np.array(
            [[0, 2],
             [1, 0]]),
        AP=None,
        L=None)
    solution = CTMC_Get_SteadyStateProbDistrib(m)


test_CTMC_Get_SteadyStateProbDistrib()
