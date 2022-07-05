"""Mathematical domains management"""
import src.naive.notation as notation
# TODO: Implement domain generators, e.g. for B^1, B^2, B^3, etc.
# TODO: Implement domain / sub-domains relations, e.g. for B^5 subset of B^n.


class DomainSet:
    """A set of mathematical domains.

    Design choice:
        In order to avoid key string manipulations, set elements are accessible as attributes, e.g. domains.n0.
    """
    def append(self, key, domain):
        # TODO: Prevent the usage of underscores and common names.
        setattr(self, key, domain)


class Domain:
    """A mathematical domain.

    Sample use cases:
        * Function domain
        * Operator domain
        * Set domain
        * Variable domain
    """
    def __init__(self, unicode_notation):
        self.unicode_notation = str(unicode_notation)

    def __hash__(self):
        return hash(self.unicode_notation)

    def __str__(self) -> str:
        return self.unicode_notation


domains = DomainSet()
domains.append('b', notation.BINARY_NUMBER_DOMAIN_NOTATION)
domains.append('n0', notation.NATURAL_NUMBER_0_DOMAIN_NOTATION)
domains.append('n1', notation.NATURAL_NUMBER_1_DOMAIN_NOTATION)
domains.append('n_tuple', notation.N_TUPLE_DOMAIN_NOTATION)