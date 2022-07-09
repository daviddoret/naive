from _class_variable import Variable
from _class_variable_base import VariableBase
from _class_variable_indexes import VariableIndexes


class Domain(Variable):
    """A predefined variable that represents a mathematical domain.

    Sample use cases:
        * Function domain
        * Operator domain
        * Set domain
        * Variable domain

    Todo:
        * Implement domain generators, e.g. for B^1, B^2, B^3, etc.
        * Implement subset / superset relations between domains, e.g. B^5 subset of B^n.
    """
    def __init__(self, base: VariableBase, indexes: (None, VariableIndexes) = None, *args, **kwargs):
        super().__init__(base, indexes, *args, **kwargs)



