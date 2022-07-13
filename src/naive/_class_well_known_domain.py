from _class_variable import Variable
from _class_variable_base_name import VariableBaseName
from _class_variable_indexes import VariableIndexes
from _class_set import Set


class WellKnownDomain(Variable, Set):
    """A predefined variable that represents a well-known mathematical domain or codomain.

    Sample use cases:
        * Function domain
        * Operator domain
        * Set domain
        * Variable domain

    Todo:
        * Implement domain generators, e.g. for B^1, B^2, B^3, etc.
        * Implement subset / superset relations between domains, e.g. B^5 subset of B^n.
        * Inherit from Set.
    """
    def __init__(self, base: VariableBaseName, indexes: (None, VariableIndexes) = None, *args, **kwargs):
        super().__init__(base, indexes, *args, **kwargs)



