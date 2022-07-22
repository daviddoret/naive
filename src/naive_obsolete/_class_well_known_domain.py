import keywords
from _class_variable import Variable
from _class_variable_base_name import VariableBaseName
from _class_variable_indexes import VariableIndexes
from _class_variable_exponent import VariableExponent
from _class_set import Set
from _function_coerce import coerce


class WellKnownDomain(Set, Variable):
    """A predefined variable that represents a well-defined set and (co)codomain.

    Sample use cases:
        * SystemFunction codomain
        * Operator codomain
        * Set codomain
        * Variable codomain

    Todo:
        * Implement codomain generators, e.g. for B^1, B^2, B^3, etc.
        * Implement subset / superset relations between domains, e.g. B^5 subset of B^n.
        * Inherit from Set.
    """

    def __init__(self, base_name: VariableBaseName, exponent: VariableExponent = None, indexes: VariableIndexes = None,
                 dimensions=None, **kwargs):
        # Type coercion.
        base_name = coerce(base_name, VariableBaseName)
        exponent = coerce(exponent, VariableExponent)
        indexes = coerce(indexes, VariableIndexes)
        dimensions = coerce(dimensions, int)

        # Update kwargs to transmit arguments to parent constructors.
        kwargs[keywords.variable_base_name] = base_name
        kwargs[keywords.variable_exponent] = exponent
        kwargs[keywords.variable_indexes] = indexes
        kwargs[keywords.set_dimensions] = dimensions

        # Bibliography:
        #   * https://stackoverflow.com/questions/9575409/calling-parent-class-init-with-multiple-inheritance-whats-the-right-way
        super().__init__(**kwargs)
        super(Set, self).__init__(**kwargs)
