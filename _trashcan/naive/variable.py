from __future__ import annotations
from src.naive.variable_base_name import *
from src.naive.variable_indexes import *
from src.naive.variable_definition import *
from src.naive.coerce import *
from src.naive.domain_library import *
import src.naive.notation as notation


class Variable:
    """A mathematical variable.

    A mathematical variable is a mathematical symbol that stands for a known or unknown value.

    """

    # TODO: Implement a metaclass for domain. This leads to technical conflicts and would require further analysis.
    def __init__(
            self,
            domain: Domain,
            base_name: CoercibleVariableBaseName,
            indexes: VariableIndexes = None,
            value: VariableDefinition = None,
            scope: Variable = None):
        domain = coerce(domain, Domain)
        base_name = coerce(base_name, VariableBaseName)
        indexes = coerce(indexes, VariableIndexes)
        value = coerce(value, VariableDefinition)
        scope = coerce(scope, Variable)
        # For future development:
        # If scope is None, we cannot retrieve the default user environment
        # because it is itself a variable and we would end up in an infinite loop.
        # So we leave scope as None and manage this with logic in the scope property,
        # once initialization has been completed.
        self._domain = domain
        self._base_name = base_name
        self._indexes = indexes
        self._value = value
        # TODO: Implement a default user environment but beware of infinite loops
        self._scope = scope

    def __str__(self):
        return \
            str(self.name) + \
            ' ' + \
            notation.ELEMENT_OF_NOTATION + \
            ' ' + \
            str(self.domain) + \
            notation.DEFINITION_NOTATION + \
            str(self.value)

    def __repr__(self):
        return str(self)

    @property
    def name(self) -> str:
        """The variable name is composed of the base name concatenated with indexes if any."""
        return str(self._base_name) + (str(self._indexes) if self._indexes else '')

    @property
    def qualified_name(self) -> str:
        """The qualified variable name is composed of the recursive parent name."""
        # TODO: design flaw: we should prevent circular variable scope relationships.
        if self.scope is None:
            # This variable is a root environment.
            return self.name
        else:
            # This variable is not a root environment.
            # Continue to climb the scope hierarchy
            # until we reach the root environment.
            return self.scope.qualified_name + \
                   notation.VARIABLE_SCOPE_SEPARATOR_NOTATION + \
                   self.name

    # TODO: Re-implement variable hash but put some thought in it first.
    # def __hash__(self):
    #     """Return the hash of the variable name.
    #
    #     The hash assures the unicity of the variable name.
    #     This provides support to use variable hashes as keys in dictionaries.
    #     """
    #     hash(repr(self.fully_qualified_name))

    # TODO: Re-implement variable equality but put some thought in it first.
    # def __eq__(self, other: object) -> bool:
    #     """Two variables are equal if they have the same fully qualified name.
    #     This may be interpreted as structural equality and not value equality.
    #     The variable value is not taken into consideration.
    #
    #     :param other:
    #     :return:
    #     """

    @property
    def domain(self):
        return self._domain

    @domain.setter
    def domain(self, domain):
        self._domain = domain

    @property
    def base_name(self):
        """The variable base name.

        Mutability: Immutable

        Returns:
            VariableScope
        """
        return self._base_name

    @property
    def indexes(self):
        """The variable indexes.

        Mutability: Immutable

        Returns:
            VariableScope
        """
        return self._indexes

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def scope(self):
        """The variable scope is a set where the variable should identify itself by a unique name."""
        # TODO: If None, assign new variables to the default user environment. But beware of infinite loops!
        return self._scope

    def duplicate(self) -> Variable:
        # TODO: This is more complicated than it seems. Do we need a shallow or a deep copy? Perhaps the key is to analyse the variable scope.
        raise NotImplementedError('TODO')
