from src.naive.variable_base_name import VariableBaseName, CoercibleVariableBaseName
from src.naive.variable_indexes import VariableIndexes, variable_no_index
from src.naive.variable_value import VariableValue, variable_unknown_value
from src.naive.coerce import coerce


class Variable:
    """A mathematical variable.

    A mathematical variable is a mathematical symbol that stands for a known or unknown value.

    todo:
        * Implement a metaclass for domain.
    """

    def __init__(self, domain: type, base_name: CoercibleVariableBaseName, indexes: VariableIndexes = variable_no_index, value: VariableValue = variable_unknown_value):
        base_name = coerce(base_name, VariableBaseName)
        self._domain = domain
        self._base_name = base_name
        self._indexes = indexes
        self._value = value

    def __str__(self):
        if not hasattr(self._domain, 'class_notation'):
            raise AttributeError('Domain is missing class_notation class attribute')
        return str(self._base_name) + str(self._indexes) + ' ∈ ' + getattr(self._domain, 'class_notation') + ' = ' + str(self._value)

    def __repr__(self):
        return str(self)

    @property
    def domain(self):
        return self._domain

    @domain.setter
    def domain(self, domain):
        self._domain = domain

    @property
    def base_name(self):
        return self._base_name

    @base_name.setter
    def base_name(self, base_name):
        self._base_name = base_name

    @property
    def indexes(self):
        return self._indexes

    @indexes.setter
    def indexes(self, indexes):
        self._indexes = indexes

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
