import typing
import type_library as tl
import binary_algebra as ba
import set_algebra as sa
import logging


class KripkeStructure:
    def __init__(self, s, i, tm, ap, lm):
        # Initialize properties from inside __init__
        self._s = None
        self._i = None
        self._tm = None
        self._ap = None
        self._lm = None
        # Call properties to assure consistency
        self.s = s
        self.i = i
        self.tm = tm
        self.ap = ap
        self.lm = lm

    @property
    def s(self):
        """The state set"""
        return self._s

    @s.setter
    def s(self, x):
        x = tl.coerce_set(x)
        self._s = x

    @property
    def i(self):
        """The initial set that is a subset of the state set"""
        return self._i

    @i.setter
    def i(self, x):
        x = tl.coerce_subset(x, self.s)
        self._i = x

    @property
    def tm(self):
        """The transition square matrix"""
        return self._tm

    @tm.setter
    def tm(self, x):
        x = tl.coerce_binary_square_matrix(x)
        self._tm = x

    @property
    def ap(self):
        """The atomic property set"""
        return self._ap

    @ap.setter
    def ap(self, x):
        x = tl.coerce_set(x)
        self._ap = x

    @property
    def lm(self):
        """The labeling function mapping matrix"""
        return self._lm

    @lm.setter
    def lm(self, x):
        x = tl.coerce_binary_matrix(x)
        self._lm = x


KripkeStructureInput = typing.TypeVar(
    'KripkeStructureInput',
    KripkeStructure,
    dict)


def coerce_kripke_structure(m: KripkeStructureInput) -> KripkeStructure:
    if isinstance(m, KripkeStructure):
        return m
    elif isinstance(m, dict):
        s = m.get('s', None)
        i = m.get('i', None)
        tm = m.get('tm', None)
        ap = m.get('ap', None)
        lm = m.get('lm', None)
        coerced_m = KripkeStructure(s, i, tm, ap, lm)
        logging.debug(f'Coerce {m}[{type(m)}] to Kripke structure {coerced_m}')
        return coerced_m
    else:
        raise ValueError


def to_text(o: object) -> str:
    if isinstance(o, KripkeStructure):
        return f'({o.s}, {o.i}, {o.tm}, {o.ap}, {o.lm})'
    else:
        raise NotImplementedError


def sat_tt(m: KripkeStructure, s_prime: tl.SetOrIVInput = None, output_type: (type, typing.TypeVar) = tl.Set) -> tl.SetOrIV:
    """Get the satisfaction set of the state formula Sat(tt)

    Formally:
    Let M be a Kripke Structure model with states S.
    Conditional: Let S' be a subset of S.
    Let tt be the tautological truth state formula.
    Let Sat(tt) = {s ∈ S' ⊆ S}.

    :param m: The Kripke structure model M.
    :param s_prime: (conditional) The subset S' ⊆ S. Note that if s_prime is None, it is assumed that all states are considered and NOT no states (the empty set).
    :param output_type: (conditional) Set or IncidenceVector. Default equals Set.
    :return: The satisfaction set. If output_format is IncidenceVector, then the returned incidence vector is relative to the set S of the model, and not S'.
    """

    m = coerce_kripke_structure(m)
    if s_prime is not None:
        s_prime = tl.coerce_subset_or_iv(s_prime, m.s)
    output_type = tl.coerce_set_or_iv_type(output_type)

    # Get the size of the incidence vector
    s_cardinality = sa.set_cardinality(m.s)

    # Prepare an incidence vector of that size with all ones
    sat_iv = ba.get_one_binary_vector(s_cardinality)

    if s_prime is not None:
        # Work internally with incidence vectors
        s_prime_iv = sa.get_incidence_vector(s_prime, m.s)
        # Limit the result to the requested set
        sat_iv = ba.get_minima(sat_iv, s_prime_iv)

    # Note that if s' is None,
    # it is assumed that we consider all states
    # and NOT no states (the empty set).

    if output_type == tl.Set:
        return sa.get_set(sat_iv, m.s)
    else:
        return sat_iv


def get_labels_from_state(m: KripkeStructureInput, s: tl.StateInput,
                          output_type: (type, typing.TypeVar) = tl.Set) -> (tl.AtomicPropertySet, tl.IncidenceVector):
    """Given a Kripke structure M (m), and a state s ∈ S, return the set of labels (aka atomic properties) attached to that state.

    :param output_type:
    :param m: The Kripke structure M
    :param s: A state s
    :return:
    """
    m = coerce_kripke_structure(m)
    s = tl.coerce_state(s, m.s)
    output_type = tl.coerce_set_or_iv_type(output_type)

    # Get the index position of s
    s_index = m.s.index(s)

    # Get the s_index column from the label mapping matrix
    # This corresponds to the label incidence vector
    label_iv = m.lm[:, s_index]
    # Superfluous coercion
    label_iv = tl.coerce_incidence_vector(label_iv, m.ap)

    if output_type == tl.Set:
        label_set = sa.get_set(label_iv, m.ap)
        logging.debug(f'L({s}) = {label_set}')
        return label_set
    else:
        logging.debug(f'L({s}) = {label_iv}')
        return label_iv


def get_states_from_label(
        m: KripkeStructureInput,
        s_prime: (tl.StateSetInput, None),
        label: tl.AtomicPropertyInput,
        output_type: (type, typing.TypeVar) = tl.Set) \
        -> (tl.StateSet, tl.IncidenceVector):
    """Return the states linked to a label

    Given a Kripke structure M (m),
    (conditionally) given a subset S' of S,
    given a label (aka atomic property) ∈ AP,
    return the subset of states S'' ⊆ S (or S') that are attached to that label.

    :param m: The Kripke structure M
    :param s_prime: None to exhaustively analyse M, or a subset of S to limit the analysis otherwise.
    :param label: The label (aka atomic property) ap
    :param output_type: Set or IncidenceVector depending on the desired output
    :return: The subset S'' ⊆ S
    """
    m = coerce_kripke_structure(m)
    if s_prime is None:
        # Exhaustive analysis of M
        s_prime = m.s
    else:
        # Limited analysis of M to a subset S' ⊆ S
        s_prime = tl.coerce_state_subset(s_prime, m.s)
    s_prime_iv = sa.get_incidence_vector(s_prime, m.s)
    label = tl.coerce_atomic_property(label, m.ap)
    output_type = tl.coerce_set_or_iv_type(output_type)

    # Get the index label a
    a_index = m.ap.index(label)

    # Get the a_index row from the label mapping matrix
    # This corresponds to the state incidence vector
    # This is equivalent to Sat(S)
    labeled_states_iv = m.lm[a_index, :]

    # Take the element-wise min of S' and Sat(S),
    # which is equivalent to the set intersection.
    s_prime_prime_iv = ba.get_minima(s_prime_iv, labeled_states_iv)

    # Superfluous coercion
    s_prime_prime_iv = tl.coerce_incidence_vector(s_prime_prime_iv, m.s)

    if output_type == tl.Set:
        s_prime_prime_subset = sa.get_set(s_prime_prime_iv, m.s)
        logging.debug(f'States({label}) = {s_prime_prime_subset}')
        return s_prime_prime_subset
    else:
        logging.debug(f'States({label}) = {s_prime_prime_iv}')
        return s_prime_prime_iv


def sat_a(m: KripkeStructure, s_prime: tl.SetOrIVInput, label: tl.AtomicPropertyInput,
          output_type: (type, typing.TypeVar) = tl.Set) -> tl.SetOrIV:
    """Get the satisfaction set of the state formula Sat(a)

    Formally:
    Let M be an LTS model with states S.
    Conditional: Let S' be a subset of S.
    Let a be a label (aka atomic property).
    Let L(s) be the set of labels (aka atomic properties) attached to s.
    Let Sat(a) = {s_i ∈ S' ⊆ S | a ∈ L(s_i)}

    :param m: The Kripke structure model M.
    :param s_prime: (conditional) The subset S' ⊆ S. Note that if s_prime is None, it is assumed that all states are considered and NOT no states (the empty set).
    :param label: The label (aka atomic property).
    :param output_type: (conditional) Set or IncidenceVector. Default equals Set.
    :return: The satisfaction set. If output_format is IncidenceVector, then the returned incidence vector is relative to the set S of the model, and not S'.

    """
    # These are synonymous
    # Coercion takes place in the child method
    sat_a_result = get_states_from_label(m, s_prime, label, output_type)
    logging.debug(f'Sat({label}) = {sat_a_result}')
    return sat_a_result


def sat_not_phi(m: KripkeStructure, s_prime: tl.SetOrIVInput, sat_phi: tl.SetOrIVInput,
                output_type: (type, typing.TypeVar) = tl.Set) -> tl.SetOrIV:
    """Get the satisfaction set of the state formula Sat(¬Φ)

    Formally:
    Let M be an LTS model with states S.
    Conditional: Let S' be a subset of S.
    Let Φ be a state formula.
    Lemma: Sat(¬Φ) = S ∖ Sat(Φ).
    Let Sat(a) = {s_i ∈ S' ⊆ S | s_i ∉ Sat(Φ)}

    :param m: The Kripke structure model M.
    :param s_prime: (conditional) The subset S' ⊆ S. Note that if s_prime is None, it is assumed that all states are considered and NOT no states (the empty set).
    :param sat_phi: The satisfaction set Sat(Φ).
    :param output_type: (conditional) Set or IncidenceVector. Default equals Set.
    :return: The satisfaction set. If output_format is IncidenceVector, then the returned incidence vector is relative to the set S of the model, and not S'.
    """
    # These are synonymous
    m = coerce_kripke_structure(m)
    if s_prime is None:
        # Exhaustive analysis of M
        s_prime = m.s
    else:
        # Limited analysis of M to a subset S' ⊆ S
        s_prime = tl.coerce_subset_or_iv(s_prime, m.s)
    sat_phi = tl.coerce_subset_or_iv(sat_phi, m.s)

    # Convert variables to incidence vectors
    s_prime_iv = sa.get_incidence_vector(s_prime, m.s)
    sat_phi_iv = sa.get_incidence_vector(sat_phi, m.s)

    not_sat_phi_iv = sa.get_logical_not(sat_phi_iv)
    min_not_sat_phi_iv = ba.get_minima(s_prime_iv, not_sat_phi_iv)

    # Superfluous coercion
    min_not_sat_phi_iv = tl.coerce_incidence_vector(min_not_sat_phi_iv, m.s)

    if output_type == tl.Set:
        min_not_sat_phi_subset = sa.get_set(min_not_sat_phi_iv, m.s)
        logging.debug(f'Sat(¬{sat_phi}) = {min_not_sat_phi_subset}')
        return min_not_sat_phi_subset
    else:
        logging.debug(f'Sat(¬{sat_phi}) = {min_not_sat_phi_iv}')
        return min_not_sat_phi_iv


def sat_phi_or_psi(m: KripkeStructure, s_prime: tl.SetOrIVInput, sat_phi: tl.SetOrIVInput,
                   sat_psi: tl.SetOrIVInput, output_type: (type, typing.TypeVar) = tl.Set) -> tl.SetOrIV:
    """Get the satisfaction set of the state formula Sat(Φ ∨ Ψ)

    Formally:
    Let M be a Kripke structure's model with states S.
    Conditional: Let S' be a subset of S.
    Let Φ be a state formula.
    Let Ψ be a state formula.
    Lemma: Sat (Φ ∨ Ψ) = Sat (Φ) ∪ Sat (Ψ).
    Let Sat(Φ ∨ Ψ) = {s_i ∈ S' ⊆ S | s_i ∉ {Sat(Φ) ∪ Sat (Ψ)} }
    Let max(v1, v2) be the element-wise max operation
    For incidence vectors: max is equivalent to ∪ on sets
    Hence, Sat(Φ ∨ Ψ) ~ max(IV(Φ), IV(Ψ).

    :param m: The Kripke structure model M.
    :param s_prime: (conditional) The subset S' ⊆ S. Note that if s_prime is None, it is assumed that all states are considered and NOT no states (the empty set).
    :param sat_phi: The satisfaction set Sat(Φ).
    :param sat_psi: The satisfaction set Sat(Ψ).
    :param output_type: (conditional) Set or IncidenceVector. Default equals Set.
    :return: The satisfaction set. If output_format is IncidenceVector, then the returned incidence vector is relative to the set S of the model, and not S'.
    """
    # These are synonymous
    m = coerce_kripke_structure(m)
    if s_prime is None:
        # Exhaustive analysis of M
        s_prime = m.s
    else:
        # Limited analysis of M to a subset S' ⊆ S
        s_prime = tl.coerce_subset_or_iv(s_prime, m.s)
    sat_phi = tl.coerce_subset_or_iv(sat_phi, m.s)
    sat_psi = tl.coerce_subset_or_iv(sat_psi, m.s)

    # Convert variables to incidence vectors
    s_prime_iv = sa.get_incidence_vector(s_prime, m.s)
    sat_phi_iv = sa.get_incidence_vector(sat_phi, m.s)
    sat_psi_iv = sa.get_incidence_vector(sat_psi, m.s)

    # Get the element-wise maxima that is equivalent to the union set operation
    phi_or_psi_iv = ba.get_maxima(sat_phi_iv, sat_psi_iv)

    # Reduce the result to S'
    phi_or_psi_iv = ba.get_minima(phi_or_psi_iv, s_prime_iv)

    # Superfluous coercion
    phi_or_psi_iv = tl.coerce_incidence_vector(phi_or_psi_iv, m.s)

    if output_type == tl.Set:
        phi_or_psi_subset = sa.get_set(phi_or_psi_iv, m.s)
        logging.debug(f'Sat({sat_phi} ∨ {sat_psi}) = {phi_or_psi_subset}')
        return phi_or_psi_subset
    else:
        logging.debug(f'Sat({sat_phi} ∨ {sat_psi}) = {phi_or_psi_iv}')
        return phi_or_psi_iv


def sat_phi_and_psi(m: KripkeStructure, s_prime: tl.SetOrIVInput, sat_phi: tl.SetOrIVInput,
                    sat_psi: tl.SetOrIVInput, output_type: (type, typing.TypeVar) = tl.Set) -> tl.SetOrIV:
    """Get the satisfaction set of the state formula Sat(Φ ∧ Ψ)

    Formally:
    Let M be a Kripke structure's model with states S.
    Conditional: Let S' be a subset of S.
    Let Φ be a state formula.
    Let Ψ be a state formula.
    Lemma: Sat (Φ ∧ Ψ) = Sat (Φ) ∩ Sat (Ψ).
    Let Sat(Φ ∨ Ψ) = {s_i ∈ S' ⊆ S | s_i ∉ {Sat(Φ) ∩ Sat (Ψ)} }
    Let min(v1, v2) be the element-wise min operation
    For incidence vectors: min is equivalent to ∩ on sets
    Hence, Sat(Φ ∨ Ψ) ~ min(IV(Φ), IV(Ψ).

    :param m: The Kripke structure model M.
    :param s_prime: (conditional) The subset S' ⊆ S. Note that if s_prime is None, it is assumed that all states are considered and NOT no states (the empty set).
    :param sat_phi: The satisfaction set Sat(Φ).
    :param sat_psi: The satisfaction set Sat(Ψ).
    :param output_type: (conditional) Set or IncidenceVector. Default equals Set.
    :return: The satisfaction set. If output_format is IncidenceVector, then the returned incidence vector is relative to the set S of the model, and not S'.
    """
    # These are synonymous
    m = coerce_kripke_structure(m)
    if s_prime is None:
        # Exhaustive analysis of M
        s_prime = m.s
    else:
        # Limited analysis of M to a subset S' ⊆ S
        s_prime = tl.coerce_subset_or_iv(s_prime, m.s)
    sat_phi = tl.coerce_subset_or_iv(sat_phi, m.s)
    sat_psi = tl.coerce_subset_or_iv(sat_psi, m.s)

    # Convert variables to incidence vectors
    s_prime_iv = sa.get_incidence_vector(s_prime, m.s)
    sat_phi_iv = sa.get_incidence_vector(sat_phi, m.s)
    sat_psi_iv = sa.get_incidence_vector(sat_psi, m.s)

    # Get the element-wise minima that is equivalent to the union set operation
    phi_and_psi_iv = ba.get_minima(sat_phi_iv, sat_psi_iv)

    # Reduce the result to S'
    phi_and_psi_iv = ba.get_minima(phi_and_psi_iv, s_prime_iv)

    # Superfluous coercion
    phi_and_psi_iv = tl.coerce_incidence_vector(phi_and_psi_iv, m.s)

    if output_type == tl.Set:
        phi_or_psi_subset = sa.get_set(phi_and_psi_iv, m.s)
        logging.debug(f'Sat({sat_phi} ∧ {sat_psi}) = {phi_or_psi_subset}')
        return phi_or_psi_subset
    else:
        logging.debug(f'Sat({sat_phi} ∧ {sat_psi}) = {phi_and_psi_iv}')
        return phi_and_psi_iv
