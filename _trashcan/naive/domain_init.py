from src.naive import DomainSet
from src.naive import notation


domains = DomainSet()
domains.append('b', notation.BINARY_NUMBER_DOMAIN_NOTATION)
domains.append('n0', notation.NATURAL_NUMBER_0_DOMAIN_NOTATION)
domains.append('n1', notation.NATURAL_NUMBER_1_DOMAIN_NOTATION)
domains.append('n_tuple', notation.N_TUPLE_DOMAIN_NOTATION)